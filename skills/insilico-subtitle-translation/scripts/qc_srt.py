#!/usr/bin/env python3
"""Validate monolingual and paired subtitle files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BAD_TERMS = [
    "Shabenkov",
    "Emsilico",
    "Insilica",
    "Pandaomics",
    "dry MD",
    "Jie Wang",
]
FILLERS = [r"\buh\b", r"\bum\b", r"\bah\b", r"\ber\b", r"\bhmm\b", r"\bmhm\b", r"嗯", r"呃", r"额"]
ORPHANS = {"以", "以及", "Y", "Alex", "Wang", "Jue", "Zhavoronkov", "Insilico"}
# These are high-value subtitle units. The check is advisory: a hit asks for
# human review, while timing may occasionally justify a deliberately short cue.
PROTECTED_TERMS = [
    "Insilico Medicine",
    "MMAI Gym",
    "MMAI Gym for Science",
    "Pharma.AI",
    "PandaOmics",
    "Chemistry42",
    "Biology42",
    "Medicine42",
    "Science42",
    "post-training pipeline",
    "frontier language models",
    "large language models",
    "language model",
    "drug discovery tasks",
    "drug discovery",
    "SOTA performance",
    "1-billion-parameter dense model",
    "dense model",
    "3D molecular design",
    "2D molecular design",
    "molecular optimization",
    "de novo molecular design",
    "后训练流程",
    "正则化和训练",
    "十亿参数级稠密模型",
    "药物发现任务",
    "前沿语言模型",
    "前沿专业模型",
    "智能体工作流",
    "三维分子设计",
    "二维分子设计",
    "分子优化",
]
TIME_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> "
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)


def to_ms(match: re.Match[str], offset: int) -> int:
    h, m, s, ms = [int(match.group(offset + i)) for i in range(4)]
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def is_cjk(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff"


def visible_length(text: str) -> float:
    total = 0.0
    for char in text:
        if char.isspace():
            total += 0.5
        elif is_cjk(char):
            total += 1.0
        else:
            total += 0.6
    return round(total, 1)


def normalize_boundary_text(text: str) -> tuple[str, list[int]]:
    """Return letters/CJK text plus source offsets for split-term checks."""
    characters: list[str] = []
    offsets: list[int] = []
    for offset, char in enumerate(text):
        if char.isalnum() or is_cjk(char):
            characters.append(char.lower())
            offsets.append(offset)
    return "".join(characters), offsets


def spans_separator(text: str, term: str, separator: str) -> bool:
    """Whether an occurrence of term crosses the supplied raw-text separator."""
    normalized_text, offsets = normalize_boundary_text(text)
    normalized_term, _ = normalize_boundary_text(term)
    start = normalized_text.find(normalized_term)
    while start != -1:
        end = start + len(normalized_term)
        raw_slice = text[offsets[start]:offsets[end - 1] + 1]
        if separator in raw_slice:
            return True
        start = normalized_text.find(normalized_term, start + 1)
    return False


def layer_key(line: str) -> str:
    cjk_count = sum(1 for char in line if is_cjk(char))
    latin_count = sum(1 for char in line if char.isascii() and char.isalpha())
    return "chinese" if cjk_count > latin_count else "english"


def subtitle_layers(lines: list[str]) -> dict[str, str]:
    """Group wrapped bilingual text into separate English and Chinese layers."""
    # Standard bilingual delivery is exactly English above Chinese. This avoids
    # misclassifying a Chinese line that contains a long English brand name.
    if len(lines) == 2 and any(is_cjk(char) for char in lines[1]):
        return {"english": lines[0], "chinese": lines[1]}

    grouped: dict[str, list[str]] = {}
    for line in lines:
        grouped.setdefault(layer_key(line), []).append(line)
    return {key: "\n".join(value) for key, value in grouped.items()}


def parse_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    blocks = re.split(r"\n{2,}", raw) if raw else []
    issues: list[dict] = []
    cues: list[dict] = []
    previous_end = -1

    for expected, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3:
            issues.append({"cue": expected, "type": "incomplete_block"})
            continue
        if lines[0].strip() != str(expected):
            issues.append({
                "cue": expected,
                "type": "bad_number",
                "value": lines[0].strip(),
            })
        match = TIME_RE.fullmatch(lines[1].strip())
        if not match:
            issues.append({
                "cue": expected,
                "type": "bad_time_format",
                "value": lines[1].strip(),
            })
            continue
        start = to_ms(match, 1)
        end = to_ms(match, 5)
        if end <= start:
            issues.append({"cue": expected, "type": "non_positive_duration"})
        if start < previous_end:
            issues.append({"cue": expected, "type": "overlap"})
        previous_end = end

        text_lines = [line.strip() for line in lines[2:] if line.strip()]
        text = "\n".join(text_lines)
        cues.append({
            "index": expected,
            "start": start,
            "end": end,
            "text": text,
            "layers": subtitle_layers(text_lines),
        })

        if not text:
            issues.append({"cue": expected, "type": "empty_text"})
        if text.replace("\n", " ").strip() in ORPHANS:
            issues.append({"cue": expected, "type": "orphan_fragment", "text": text})
        for filler in FILLERS:
            if re.search(filler, text, re.IGNORECASE):
                issues.append({"cue": expected, "type": "filler", "text": text})
        for term in BAD_TERMS:
            if term in text:
                issues.append({"cue": expected, "type": "bad_term", "term": term})
        line_lengths = [visible_length(line) for line in text_lines]
        cjk_count = sum(1 for char in text if is_cjk(char))
        latin_count = sum(1 for char in text if char.isascii() and char.isalpha())
        # 25 is the layout target; allow a little room for an intact semantic
        # unit before warning, as in the approved MMAI Gym reference.
        limit = 30 if cjk_count > latin_count else 72
        for line_number, length in enumerate(line_lengths, 1):
            if length > limit:
                issues.append({
                    "cue": expected,
                    "type": "long_line",
                    "line": line_number,
                    "visible_length": length,
                    "limit": limit,
                })

    for cue in cues:
        for term in PROTECTED_TERMS:
            for layer in cue["layers"].values():
                if spans_separator(layer, term, "\n"):
                    issues.append({
                        "cue": cue["index"],
                        "type": "split_protected_term_within_cue",
                        "term": term,
                    })
                    break

    for current_cue, next_cue in zip(cues, cues[1:]):
        shared_layers = current_cue["layers"].keys() & next_cue["layers"].keys()
        for layer_name in shared_layers:
            combined = (
                current_cue["layers"][layer_name]
                + "\uffff"
                + next_cue["layers"][layer_name]
            )
            for term in PROTECTED_TERMS:
                if spans_separator(combined, term, "\uffff"):
                    issues.append({
                        "cue": current_cue["index"],
                        "next_cue": next_cue["index"],
                        "type": "split_protected_term_across_cues",
                        "term": term,
                        "layer": layer_name,
                    })

    return {
        "path": str(path.resolve()),
        "cue_count": len(blocks),
        "cues": cues,
        "issues": issues,
    }


def compare_pair(left: dict, right: dict) -> list[dict]:
    issues: list[dict] = []
    if left["cue_count"] != right["cue_count"]:
        issues.append({
            "type": "cue_count_mismatch",
            "left": left["cue_count"],
            "right": right["cue_count"],
        })
        return issues

    for left_cue, right_cue in zip(left["cues"], right["cues"]):
        if left_cue["start"] != right_cue["start"] or left_cue["end"] != right_cue["end"]:
            issues.append({
                "cue": left_cue["index"],
                "type": "timecode_mismatch",
            })
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--paired", nargs=2, metavar=("ENGLISH", "CHINESE"), type=Path)
    parser.add_argument("--bilingual", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    paths = list(args.files)
    if args.paired:
        paths.extend(args.paired)
    if args.bilingual:
        paths.append(args.bilingual)
    unique_paths = list(dict.fromkeys(paths))
    if not unique_paths:
        parser.error("provide at least one SRT file")

    results = [parse_file(path) for path in unique_paths]
    report = {"files": results, "pair_issues": []}
    if args.paired:
        by_path = {result["path"]: result for result in results}
        left = by_path[str(args.paired[0].resolve())]
        right = by_path[str(args.paired[1].resolve())]
        report["pair_issues"] = compare_pair(left, right)

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(output + "\n", encoding="utf-8")

    has_issues = bool(report["pair_issues"]) or any(item["issues"] for item in results)
    return 1 if has_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
