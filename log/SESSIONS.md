# Session log

Newest entry first. See the format in `docs/SESSION_PROTOCOL.md`.

## Session 2 — 2026-10-23 — T02
- Bot: https://prompt.ql.app/project/p-5dbcae94-40af/promptql-playground/thread/eaca8889-2209-4662-b1d1-6be78488a20f (same bot as session 1)
- Did: Surveyed the Higgsfield catalog (87 models) and extracted parameters for the first/last-frame video, reference-image and video-to-video candidates. Ran cost estimates and wrote `docs/MODELS.md`.
- Cost: ~27 OLU, own work only; no generation.
- Result: done. Seedance 2.5 and GPT Image 2.5 return description-only estimates, so they are probably not submittable through PromptQL. Kling O3 4K mode returned 409 and Kling O3 video-edit's estimate returned 500. There is no audio model.
- Next: T03, an image bake-off (Qwen Image 3 edit vs Grok Image 2.0) and then the present-day sheet. It must record the OLUs actually charged per submit. T15 needs an audio decision from the user.

## Session 1 — 2026-10-23 — T01
- Bot: https://prompt.ql.app/project/p-5dbcae94-40af/promptql-playground/thread/eaca8889-2209-4662-b1d1-6be78488a20f
- Did: Scaffolded the repo. Added the brief verbatim, the reference image, the character and world bibles, the pipeline and session protocol, keyframe plan K1–K9, segment specs A–F with acceptance checklists, and the task queue T01–T18.
- Cost: own work only; no generation.
- Result: done.
- Next: T02, the model survey. The user wants the generator chosen by quality at run time, so T02 records which top-quality models are available and what each call costs in OLU.