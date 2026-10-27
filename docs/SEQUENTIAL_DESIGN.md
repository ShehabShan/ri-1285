# ri-1285 — Sequential video creation (proposed redesign)

## Verified facts (2026-10-23)

| Item | Finding | Status |
|---|---|---|
| Video model | `kling-video/v3.0/4k/image-to-video` on the Higgsfield integration. Integer durations 3–15 s. Start frame `image_url`, optional end frame `last_image_url`, `sound` defaults to **on**. | In catalog today |
| Price | 5 s = 33.6 credits = **$2.10** (16 credits = $1, from the T02 survey). 10 s ≈ $4.20 assumes the price scales with length. | **Not re-verified.** The live estimate endpoint returned HTTP 500 and then hung today. |
| Price → OLU | PromptQL charges OLUs from Higgsfield's USD estimate. The OLU-per-USD rate is not published. | **Unknown.** The first paid submit must measure it. |
| Audio | Higgsfield has **no standalone audio, music, SFX or TTS model** (all 87 models checked). Audio is only available as native sound on video models (Kling 3.0 4K `sound: on`, Wan, LTX, Seedance). Seedance 2.5 video-edit returns only a text price, so PromptQL will probably refuse it. | Needs your decision |
| Judge model | **Claude Opus 5.5** is available in this project (`llm_config` id `b90a5408-0ab4-4cd5-b459-9951605d40ac`). | Available |

## Flow

**Session 1**
1. Make one anime start still of Fang Yuan in the river from the reference design. The reference image is watercolor, seated and has closed eyes, and the brief forbids copying that look. A cheap image model costs about $0.08.
2. Generate clip 1 (about 6 s) with Kling 3.0 4K, start frame = that still, `sound: on` (ambience only; see the 2026-10-27 audio decision).
3. Record the clip in the repo.

**Session N (each fresh session)**
1. **Analyze the previous clip.** Extract the last frame plus about 12 sampled frames. Record framing, camera direction and speed, gait phase, hair and robe direction, water and mist, light and exposure, and line and color treatment.
2. **Plan the next segment.** Read the brief's beat for the next timeline position (for example 0:06 → B's five steps).
3. **Size it (Opus 5.5).** Opus 5.5 rates the scene's complexity and chooses a duration `d` (3–15 s) such that:
   `est_OLU(d) + session_overhead + 10 OLU reserve ≤ 50 OLU`
   `est_OLU(d)` = the live Higgsfield USD estimate × the measured OLU/USD rate. If the estimate fails, the session does **not** submit.
4. **Generate.** Start frame = the previous clip's exact last frame. The prompt carries forward the analysis, the locked style block and the next beat.
5. **Record and commit.** Append to `production/sequence.json`, add a session log entry, commit, push and stop.

**Stop condition:** cumulative duration reaches 30 s. A final session assembles and trims to exactly 720 frames at 24 fps.

## What gets recorded each session (`production/sequence.json`)
`index, timeline_start, duration_s, beat, model, request_body, prompt, request_id, est_usd, olu_charged, complexity_rating, clip_sha256, last_frame_sha256, analysis_of_previous, session_url`

## Brief constraints this design must respect
- **Two cuts break the chain.** Last-frame chaining cannot pass through the cuts.
  - The 0:13 flashback starts from a fresh younger-self frame. The ripple dissolve is added in assembly.
  - The 0:18 hard cut back to the river starts from a fresh frame matched to Take 1, not D's last frame.
- **Seams.** Kling's first frame reproduces the input image, so the duplicate frame is dropped at each join.
- **Style drift.** Drift compounds over successive clips. Every session therefore conditions on the session-1 style still as well as the previous last frame, so the chain does not drift one generation at a time.

## What changes in the repo
- **Replace:** the K1–K9 keyframe plan, the fixed A–F segment lengths and the T03–T18 task chain in `state.json`, `QUEUE.md` and `PIPELINE.md`.
- **Keep:** the immutable brief and its beat timings, the bibles, COMMON prompt blocks, the 50 OLU per session cap, the submit journal and no-blind-retry rule, and frame-exact assembly.
- **Add:** `production/sequence.json`, the new `docs/SESSION_PROTOCOL.md`, and validator rules for the chain.

## Decisions recorded 2026-10-23 (user, in bot eeec6cca-29b2-48b3-9939-4064732345b0)
- Sequential creation: **approved**.
- Audio: **Kling 3.0 built-in sound (`sound: on`) per clip**, no separate audio track. Superseded on 2026-10-27; see below.

## Decision recorded 2026-10-27 (user, in bot a5cd703a-1957-4fa8-80d2-33e683f8fd6a)
- Audio: Kling 3.0 built-in sound (`sound: on`) is kept per clip **for water, wind and footstep ambience only**.
- Added at assembly, at brief-exact times: the off-screen monologue "I had once screamed, gradually, I lost my voice." (0:12–0:17, never lip-synced), the drum hit on each footstep and at 0:03 and 0:18, the underwater muffle at 0:10–0:12, the erhu note, the score swells, total silence at 0:27.0–0:27.5 and the temple bell into the white at 0:27.5–0:30.
- A clip whose native sound contains speech, singing or anything implying lip movement is rejected.
- Still open: the source and rights for the monologue voice and the added score/cues (Higgsfield has no TTS or music model).

## Remaining work — task S01 (not done; stopped early because the user's OLU ran low)
- [ ] Create `production/sequence.json` (clips list: index, part take1/flashback/take2, start_s, duration_s, prompt, start-frame source, style-still hash, job id, output hash, last-frame hash, OLU charged, review pointer; plus `measured_olu_per_usd`).
- [ ] Rewrite `docs/SESSION_PROTOCOL.md` and `docs/PIPELINE.md` for the per-session loop: analyze previous clip → Opus 5.5 picks length (3–15 s) so estimate + overhead + 10 OLU reserve ≤ 50 → chain from exact last frame + session-1 style still → record → commit → stop.
- [ ] Session-1 rules: style still + clip 1 (~6 s); measure OLU per USD on the first paid submit; do not submit while the price check fails.
- [ ] Cut alignment: clip boundaries land exactly on 13 s and 18 s; flashback and Take 2 start from fresh frames, not chained.
- [ ] Replace K1–K9 (`keyframes/`), fixed A–F (`segments/`, `production/timeline.json`) and the T03–Q18 chain in `state.json` with sequential clip tasks; keep brief, bibles, COMMON prompt blocks, budget rules, submit journal.
- [ ] Update `tools/validate.py`, `tools/assemble.py` (variable clips, drop duplicate first frame at joins, keep Kling audio), `tools/render_queue.py`, tests; update README, AGENTS, MODELS.
- [ ] Run validator + `python3 -m unittest discover -s tests`, commit, push, verify remote. No paid generation in S01.
