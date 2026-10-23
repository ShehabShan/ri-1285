# Task queue

**Statuses:** `done`, `ready`, `in_progress`, `blocked` (dependencies not done), `needs_user`.

Take the first `ready` task whose dependencies are all `done`. When you finish a task, set to `ready` every task whose dependencies are now all `done`.

| ID | Task | Depends | Inputs | Output | Status |
|---|---|---|---|---|---|
| T01 | Scaffold the repo | — | brief | all docs, specs, queue | done |
| T02 | Model survey: list the image, video, audio and video-to-video models available through Higgsfield (and other connected generators). For each, record supported inputs (reference image, first and last frame), durations, resolution and the OLU cost per call. Recommend picks for each stage. No generation. | T01 | PIPELINE (Model policy) | `docs/MODELS.md` | ready |
| T03 | Present-day character sheet: front, three-quarter and profile views, plus full body standing. Anime style, brief's robe rules. | T02 | CHARACTER, reference image | `media/sheets/present_*.png`, CHARACTER locked table | blocked |
| T04 | Younger-self character sheet | T03 | CHARACTER, present sheet | `media/sheets/young_*.png` | blocked |
| T05 | River style frames: one empty, one with him mid-step | T03 | WORLD_AND_STYLE, present sheet | `media/sheets/river_*.png` | blocked |
| T06 | Keyframes K1, K2, K3 | T05 | KEYFRAMES, sheets | `media/keyframes/K1–K3.png` | blocked |
| T07 | Keyframes K4 (optional), K7, K8, K9 | T05 | KEYFRAMES, sheets | `media/keyframes/K4,K7–K9.png` | blocked |
| T08 | Keyframes K5, K6 (flashback) | T04 | KEYFRAMES, young sheet | `media/keyframes/K5–K6.png` | blocked |
| T09 | Segment A clip | T06 | `segments/A.md`, COMMON, K1, K2 | `media/clips/A.mp4` | blocked |
| T10 | Segment B clip | T06 | `segments/B.md`, COMMON, K2, K3 | `media/clips/B.mp4` | blocked |
| T11 | Segment C clip | T06, T07 | `segments/C.md`, COMMON, K3, K4 | `media/clips/C.mp4` | blocked |
| T12 | Segment D clip | T08 | `segments/D.md`, COMMON, K5, K6 | `media/clips/D.mp4` | blocked |
| T13 | Segment E clip | T07 | `segments/E.md`, COMMON, K7, K8 | `media/clips/E.mp4` | blocked |
| T14 | Segment F clip | T07 | `segments/F.md`, COMMON, K8, K9 | `media/clips/F.mp4` | blocked |
| T15 | Audio track: score, SFX and monologue, following the brief's AUDIO cues | T02 | brief (AUDIO) | `media/audio/*` | blocked |
| T16 | Assembly rough cut: seams, ripple dissolve, hard cut, white-out, grades, audio mix (VM + ffmpeg) | T09–T15 | PIPELINE | `media/cuts/rough_v1.mp4` | blocked |
| T17 | Consistency pass (video-to-video) | T16 | PIPELINE (Consistency pass), bible | `media/cuts/harmonised_v1.mp4` | blocked |
| T18 | Final QA against the brief's FIXED list, then export | T17 | brief, COMMON | `media/cuts/final.mp4`, QA report | blocked |

## Notes

- T09 is the first river clip. Its accepted model becomes the river lock (see PIPELINE → Model policy). T10, T11, T13 and T14 should run after T09 is accepted.
- If one top-quality clip costs more than about 40 OLU, it cannot fit a 50 OLU session. Flag it as `needs_user`.

## Open decisions (user)

| Decision | Default until answered |
|---|---|
| Audio as a separate track, mixed at assembly | Yes |
| Media storage | Commit to `media/` if ≤ 50 MB; otherwise a GitHub Release asset |