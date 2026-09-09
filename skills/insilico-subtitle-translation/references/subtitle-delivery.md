# Subtitle delivery rules

Use the reviewed English SRT as the semantic master. Do not translate raw ASR directly and do not use automatic Chinese translation as the official Chinese result.

- Prefer full semantic phrases and natural reading rhythm over ASR pause boundaries.
- Do not split titles from names, compound terms, project IDs, targets, hyphenated words, fixed expressions, verb-complement units, or short quantity/function-word structures. Apply this rule both between cues and within a wrapped cue.
- Do not leave a cue as a stray preposition, conjunction, name fragment, connector, or the final word of the previous sentence.
- English cue text must stay faithful to speech. Chinese may reorder syntax for readability, but cannot add entities, claims, conclusions, or evidence.
- `*_Bilingual_reviewed.srt` uses the reviewed English first and the corresponding Chinese second within each cue. Keep each language's text as a complete semantic unit; do not sacrifice term integrity merely to force source-cue parity. If the Chinese rendering needs different segmentation, resolve it into readable bilingual cues that continuously cover the matching English time span.
- Prefer one visible English line above one visible Chinese line in a bilingual cue. When either language needs wrapping, use the smallest number of lines permitted by readability and keep terms, names, and fixed expressions unbroken.
- Preserve the SRT skeleton: sequence number, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, nonempty cue text, then one blank line. Save UTF-8 text.
