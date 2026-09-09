# Insilico Subtitle Translation

A Codex skill for reviewing and translating English-Chinese SRT subtitles in Insilico Medicine-related work.

It is designed for an audio-faithful workflow:

1. Review ChatCut or ASR English against the recording and approved terminology.
2. Lock the reviewed English master before translating.
3. Translate complete meaning units into natural Simplified Chinese.
4. Re-segment English and Chinese independently for readable subtitle cues.
5. Check that names, products, fixed expressions, technical terms, and Chinese lexical units are not split across cues or visible line wraps.

## Included

- A subtitle translation and bilingual review workflow.
- Insilico terminology and approved brand-writing rules.
- A practical cue-boundary and line-wrap standard.
- `qc_srt.py`, a dependency-free SRT checker for structure, long lines, fillers, and protected terms split within or across cues.

## Use in Codex

Install this plugin from your Codex marketplace, then ask Codex to review, translate, or quality-check an SRT file. Provide the recording or an approved script whenever names, numbers, or technical claims require verification.

## Scope and limits

This plugin does not include source video, audio, or subtitle files. It does not replace listening to the recording, project-approved terminology, or human review of uncertain names, facts, and scientific claims. Brand names remain the property of their respective owners.

## License

MIT. See [LICENSE](LICENSE).
