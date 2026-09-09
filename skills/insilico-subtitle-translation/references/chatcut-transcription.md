# ChatCut transcription

Use ChatCut only for transcription and timing. Its automatic Chinese translation is never an official deliverable.

## Select the available ChatCut route

1. Prefer the configured remote `chatcut` MCP when its tools are available in the current task. Create or select a project, upload the supplied media, run recognition in the spoken language, and export the unedited English SRT.
2. If the remote tools are unavailable and the user explicitly asks for ChatCut Desktop, or the active environment requires it, use ChatCut Desktop to create a project, import the media, run English recognition, and export its unedited English SRT.
3. If ChatCut is unavailable, signed out, cannot accept the media, or cannot export SRT, stop at that boundary and explain the action needed. Do not silently substitute another ASR service.

## Preserve the timing source

- Treat every supplied audio or video as a fresh job unless the user explicitly provides an approved reference.
- Save the original ChatCut export without edits as `source/<base>_chatcut_raw_en.srt`.
- Create `source/`, `work/`, and `final/` in a fresh non-conflicting job directory.
- Review the exported English against the actual audio before translating. Keep the raw SRT available for audit.

## Optional write-back

Do not write reviewed captions back to ChatCut unless the user explicitly requests that action.
