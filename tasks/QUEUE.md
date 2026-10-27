# Task queue — generated from production/state.json

Do not edit this view. Resume `in_progress` first; then choose the first eligible
`ready` task. Dependencies require `done`, and required input assets must be
**accepted**, current and available. Run `python3 tools/validate.py --task ID`.
T tasks make candidates; Q tasks independently review. Missing evidence = hold.

| ID | Task | Depends | Required accepted inputs | Outputs | Status |
|---|---|---|---|---|---|
| T01 | Scaffold the repo | — | — | — | done |
| T02 | Model survey (historical; estimates are not locks) | T01 | — | — | done |
| H01 | Harden fresh-session continuity, QA and assembly | T02 | — | — | done |
| S01 | Rewrite repo for sequential creation (docs/SEQUENTIAL_DESIGN.md) | H01 | — | — | ready |
| T03 | Present-day sheet bake-off and four-view master | H01, S01 | — | present_front, present_threequarter, present_profile, present_full, image_recipe | blocked |
| Q03 | Independent review: Present-day sheet bake-off and four-view master | T03 | — | present_front, present_threequarter, present_profile, present_full, image_recipe | blocked |
| T04 | Younger sheet and flashback look master | Q03 | present_front, present_threequarter | young_sheet, flashback_style | blocked |
| Q04 | Independent review: Younger sheet and flashback look master | T04 | — | young_sheet, flashback_style | blocked |
| T05 | River style and continuity master package | Q03 | present_front, present_threequarter, present_full | river_empty, river_character, continuity_master | blocked |
| Q05 | Independent review: River style and continuity master package | T05 | — | river_empty, river_character, continuity_master | blocked |
| T06 | K1 K2 K3 and planned boundary handoffs | Q05 | continuity_master, present_front, river_character | K1, K2, K3, boundary_K2, boundary_K3 | blocked |
| Q06 | Independent review: K1 K2 K3 and planned boundary handoffs | T06 | — | K1, K2, K3, boundary_K2, boundary_K3 | blocked |
| T07 | Mandatory K4 and K7 K8 K9 boundary handoffs | Q05 | continuity_master, river_character | K4, K7, K8, K9, boundary_K8 | blocked |
| Q07 | Independent review: Mandatory K4 and K7 K8 K9 boundary handoffs | T07 | — | K4, K7, K8, K9, boundary_K8 | blocked |
| T08 | Flashback K5 K6 | Q04 | young_sheet, flashback_style | K5, K6 | blocked |
| Q08 | Independent review: Flashback K5 K6 | T08 | — | K5, K6 | blocked |
| P01 | Technical feasibility: each duration/control, cost bound, clean-clone storage and edit proof | Q06, Q07, Q08 | K1, K2, K3, K4, K5, K6, K7, K8, K9 | preflight | blocked |
| QP01 | Independent preflight review | P01 | — | preflight | blocked |
| T09 | A candidate/model comparison and motion anchor | QP01 | K1, K2, continuity_master, preflight | A, motion_anchor, river_recipe | blocked |
| Q09 | Independent review: A candidate/model comparison and motion anchor | T09 | — | A, motion_anchor, river_recipe | blocked |
| T10 | B candidate: five steps and A/B seam | Q09 | K2, K3, A, motion_anchor, boundary_K2 | B, seam_AB | blocked |
| Q10 | Independent review: B candidate: five steps and A/B seam | T10 | — | B, seam_AB | blocked |
| T11 | C candidate: eye/ripple and B/C seam | Q10 | K3, K4, B, motion_anchor, boundary_K3 | C, seam_BC | blocked |
| Q11 | Independent review: C candidate: eye/ripple and B/C seam | T11 | — | C, seam_BC | blocked |
| T12 | D flashback candidate and timed entry composite | QP01, Q09, Q11 | K5, K6, young_sheet, flashback_style, motion_anchor, C, K4 | D, D_entry | blocked |
| Q12 | Independent review: D flashback candidate and timed entry composite | T12 | — | D, D_entry | blocked |
| T13 | E candidate: plant to face and chest light | Q09, QP01 | K7, K8, A, motion_anchor, boundary_K8 | E | blocked |
| Q13 | Independent review: E candidate: plant to face and chest light | T13 | — | E | blocked |
| T14 | F candidate and E/F seam | Q13 | K8, K9, E, motion_anchor, boundary_K8 | F, seam_EF | blocked |
| Q14 | Independent review: F candidate and E/F seam | T14 | — | F, seam_EF | blocked |
| T15 | Authorized score, SFX, monologue stems and sample-exact mix | Q11, Q12, Q14 | A, B, C, D, E, F | audio_mix, audio_stems, audio_rights | blocked |
| Q15 | Independent review: Authorized score, SFX, monologue stems and sample-exact mix | T15 | — | audio_mix, audio_stems, audio_rights | blocked |
| T16 | Reproducible frame-exact assembly | Q11, Q12, Q14, Q15 | A, B, C, D_entry, E, F, audio_mix, seam_AB, seam_BC, seam_EF | rough, assembly_recipe | blocked |
| Q16 | Independent review: Reproducible frame-exact assembly | T16 | — | rough, assembly_recipe | blocked |
| T17 | Conservative consistency finishing; no required V2V | Q16 | rough, assembly_recipe, continuity_master | finished, finish_recipe | blocked |
| Q17 | Independent review: Conservative consistency finishing; no required V2V | T17 | — | finished, finish_recipe | blocked |
| T18 | Final encode, release QA and delivery approval | Q17 | finished, finish_recipe | final, final_pcm | blocked |
| Q18 | Independent review: Final encode, release QA and delivery approval | T18 | — | final, final_pcm | blocked |

## Open user decisions
- Audio: DECIDED 2026-10-27 — Kling sound on per clip for ambience only; monologue, step drums, muffle, silence and bell added at assembly. Voice/score source and rights still open.
- Sequential creation approved; see docs/SEQUENTIAL_DESIGN.md. Run S01 first.
- Paid generation: reliable OLU upper bounds required before submission, not USD guesses.
- Master packages Q03/Q04/Q05 and final Q18 need explicit user approvals for exact hashes.
- Optional generative finishing needs separate user authorization; default is deterministic.

## Handoff

- **S01**: Implement docs/SEQUENTIAL_DESIGN.md including the 2026-10-27 audio decision (Kling sound on = ambience only; monologue, step drums, muffle, silence and bell added at assembly) and docs/ri1285 pre-start fixes: per-part frame budgets (Take 1 = 312, flashback = 120, Take 2 = 288 incl. white hold) with generate-long-and-trim on the last clip of each part; ripple-dissolve handle frames at 0:13; per-clip review/accept before chaining, rejection makes later clips stale; user-approved fresh start stills for the flashback and Take 2; conform Kling output to 1920x1080 24 fps; Opus 5.5 llm_config id in this project is 0edabd39-3d21-42cb-9cfd-bc2c494eda84. Update SESSION_PROTOCOL/PIPELINE/MEDIA_CONTRACT/MODELS/README/AGENTS, state tasks, validate.py, assemble.py (mix clip ambience with added cues), render_queue and tests; commit, push, verify remote, stop. No paid generation.
- **T03**: Superseded by the sequential design; S01 replaces this task. Do not start.
- **T15**: Audio route decided 2026-10-27: Kling ambience per clip plus assembly-added monologue and cues. S01 rewrites this task. Voice and score source/rights still need user authorization.
