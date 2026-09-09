# Subtitle segmentation and line-wrap standard

Apply this standard after the English master is reviewed and before final SRT delivery. It is derived from the approved MMAI Gym subtitle reference and applies to English, Chinese, and bilingual output.

## Objective

Every subtitle must be understandable on the screen by itself while remaining faithful to the continuing sentence. A cue boundary or an in-cue line break must never cut a lexical item, protected term, or fixed phrase in half.

## Required sequence

1. Read the complete source sentence across all adjacent ASR cues.
2. Verify English names and technical wording against the local terminology reference and project sources.
3. Produce and lock the fluent English master.
4. Translate the complete sentence or meaning unit into Chinese.
5. Make separate English and Chinese cue plans according to meaning, timing, and reading speed.
6. Assemble bilingual cues with English above Chinese and run structural plus boundary QC.

## Boundary hierarchy

Choose the earliest suitable boundary in this order:

1. End of a complete sentence.
2. End of an independent clause or a completed coordinated clause.
3. End of a verb phrase only after its required object or complement is complete.
4. End of a complete noun phrase, list item, or modifier group.
5. A short natural pause only if it does not violate any protected-unit rule.

Never create a boundary:

- inside a company, product, platform, person, drug, target, project ID, abbreviation, number-plus-unit, or hyphenated expression;
- between a preposition and its object, a determiner and noun, an adjective and noun, a noun and its required modifier, a phrasal verb and particle, or a verb and its required object/complement;
- inside a familiar technical or fixed expression, such as `MMAI Gym for Science`, `post-training pipeline`, `frontier language models`, `drug discovery tasks`, `SOTA performance`, or `1-billion-parameter dense model`;
- inside a Chinese multi-character word, technical term, name, idiom, or fixed expression, such as `后训练流程`, `正则化和训练`, `十亿参数级稠密模型`, `药物发现任务`, `前沿语言模型`, or `智能体工作流`.

## Chinese-specific practice

- Translate for fluent Chinese first. Do not preserve English word order just because English is shown in the same bilingual cue.
- Prefer a single short Chinese display line per cue. Aim for about 25 visible Chinese characters; permit up to roughly 30 when that preserves a complete semantic unit. When timing requires a continuation, end at a completed Chinese phrase rather than after one character or halfway through a word.
- Do not create a Chinese cue solely because a short English fragment has its own cue. Merge or redistribute consecutive Chinese cues when the time coverage remains continuous and the bilingual layout stays readable.
- Omit final Chinese commas and full stops unless the project's established subtitle style needs them. Keep punctuation when it materially clarifies a list, contrast, or sentence relation.

## Reference patterns

- Keep `MMAI Gym for Science` intact rather than ending one cue with `MMAI Gym for` and starting the next with `Science`.
- Keep a full role or name unit together where duration permits, such as `Rim Shayakhmetov，是英矽智能的首席AI模型负责人`.
- Prefer complete Chinese units such as `它的开发逻辑` and `药物发现任务` over literal fragments copied from English ASR timing.
- A short continuation can be legitimate when dictated by timing; assess it in the full sentence. Do not auto-rewrite an approved timing-driven continuation solely because it is short.

## Final human pass

Read the subtitles in cue order with only the current cue visible, then read adjacent pairs. Confirm that both views preserve the sentence, names, terminology, and intended reading rhythm. Treat automated boundary warnings as review prompts, especially for short timing-driven continuations.
