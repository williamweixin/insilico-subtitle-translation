# Subtitle translation workflow

Use for audio transcript review, SRT translation, and bilingual subtitle delivery.

## Fidelity workflow

1. Obtain source timing/ASR from the user's supplied material or chosen transcription tool.
2. Review English against audio before translating. The reviewed English is an audio-faithful master, not a rewritten corporate script.
3. Allowed English changes: clear ASR term/name/number corrections verified by audio or reliable context; filler deletion; punctuation/capitalization; cue-boundary repair.
4. Forbidden English changes: summarizing, beautifying, changing degree words, inferring stronger efficacy/commercial claims, or silently correcting uncertain numbers.
5. Translate Chinese from the locked English master. Naturalize syntax for readability without changing the claim.
6. Build Chinese from complete reviewed-English sentences or meaning units. Chinese may merge adjacent English cues or split differently for natural reading; its cues must continuously cover the corresponding English time range, but cue counts do not have to match.

## Cue boundaries

- Read through the entire spoken sentence before translating or changing a boundary. A source cue is timing evidence, not an instruction to translate a fragment on its own.
- Build the Chinese translation from the locked full English sentence or complete meaning unit, then place cue boundaries. Do not use the location of an English source break to decide Chinese word order or Chinese segmentation.
- Prefer complete semantic phrases over raw acoustic segmentation. Break first at completed sentences, then at completed clauses, then at a natural phrase joint only when timing or reading speed requires it.
- Do not strand titles/names, prepositions, conjunctions, project IDs, hyphenated compounds, a modifier from its head noun, a verb from its object/complement, or the last word of a prior sentence.
- Do not split protected terms such as `Insilico Medicine`, `Pharma.AI`, `PandaOmics`, `Chemistry42`, names, target symbols, and project IDs.
- Keep quantity structures, function-word groups, compound terms, title/name units, phrasal verbs, and fixed expressions together. Examples include `MMAI Gym for Science`, `frontier language models`, `post-training pipeline`, `drug discovery tasks`, `SOTA performance`, `both of you`, `development candidate`, and `one and a half years ago`.
- In Chinese, do not break within a multi-character word, scientific term, name, fixed expression, or grammatical unit at either a cue boundary or a visible line break. Examples include `后训练流程`, `正则化和训练`, `十亿参数级稠密模型`, `药物发现任务`, `前沿语言模型`, and `智能体工作流`.
- Merge orphan fragments minimally; do not create an unreadably long cue.
- English normally stays within roughly 72 characters per cue.
- Chinese final delivery should use short readable blocks, normally one visible line and about 25 Chinese characters per line. A semantically complete line may extend to roughly 30 visible characters when shortening it would split a protected unit; if a second line is necessary, divide it at a completed semantic unit and never wrap through a protected term or Chinese lexical unit.
- Punctuation in final Chinese SRT follows the user's house style. Do not remove punctuation by default for non-subtitle documents.
- Do not manufacture a Chinese cue merely to mirror an English fragment. When a fragment's meaning is absorbed into an adjacent Chinese cue, merge the Chinese cue and extend it over the full consecutive source range.
- Natural Chinese reordering may add grammar required by clear context, but never add a brand, abbreviation, entity, action, degree, or conclusion absent from the audio and context.

## ChatCut English review and terminology pass

Before Chinese translation, process ChatCut output in this order:

1. Compare the English SRT with the audio or verified recording context. Correct only confirmed ASR, name, term, number, capitalization, punctuation, filler, and cue-boundary errors.
2. Search the local terminology reference and project-specific sources for every proper noun, product, platform, acronym, target, ID, and technical term that appears in the passage. Record unresolved items rather than guessing.
3. Normalize approved wording consistently in all English cues before the English master is locked. For example, preserve `MMAI Gym`, `MMAI Gym for Science`, `Insilico Medicine`, and other brand capitalization exactly.
4. Re-read the locked English without cue numbers. Repair a boundary if it splits a term, phrase, or sentence dependency, even if the original ASR pause falls there.
5. Translate only after this review. Rebuild the Chinese from full meaning units, then perform an independent Chinese segmentation pass.

Use [subtitle-segmentation.md](subtitle-segmentation.md) as the detailed operational checklist.

## Numbers and audit

- Apply verified numeric corrections consistently across English, Chinese, bilingual output, and audit records.
- If a number cannot be verified, retain it or flag it; never silently guess.
- For strict fidelity work, produce an audit when practical with: `original ASR → reviewed English → Chinese → reason`.
- Categorize English changes as: `ASR term/name correction`, `number correction confirmed by audio/context`, `filler deletion`, `punctuation/capitalization`, or `cue-boundary repair`.

## Final checks

- Scan short cues for ASR fragments rather than intentional beats.
- Check names, titles, numbers, drug stages, route/formulation terms, platform names, projects, and targets across both languages.
- Run `scripts/qc_srt.py` when available.
- QC success does not replace listening and language review.
