# Production decisions (locked 2026-10-27)

The user delegated every open decision to the bot (bot a5cd703a-1957-4fa8-80d2-33e683f8fd6a,
2026-10-27: "decide for me ... you will act for everything to make it best"). These
decisions are binding on every later session. They supersede `docs/SEQUENTIAL_DESIGN.md`,
`docs/MODELS.md`, `docs/MEDIA_CONTRACT.md` and `docs/SESSION_PROTOCOL.md` wherever those
conflict. `brief/BRIEF.md` still overrides this file. A session may not stop for a
`needs_user` decision that this file already answers.

## D1. Video model
- `kling-video/v3.0/4k/image-to-video` (Higgsfield) for every clip. Estimate checked
  2026-10-27: 5 s = 33.6 credits = $2.10 (sound off).
- Explicit body fields every submit: `prompt`, `negative_prompt` (brief NEGATIVE PROMPT),
  `image_url`, `duration`, `cfg_scale: 0.5`, `sound: "on"`. No `last_image_url`
  (end frames make motion stiff; continuity comes from start-frame chaining).
- Fallback: if 4K becomes unavailable or a single clip's estimate cannot fit D5's session
  budget, switch to `kling-video/v3.0/pro/image-to-video` ($0.84 / 5 s) **for the whole
  film** and regenerate any 4K clips already accepted. Never mix models inside the film.

## D2. Shot plan and exact frame map (24 fps, 720 frames)
Fixed clip lengths replace "Opus picks the length". Each clip is generated longer than it
needs and trimmed, so integer durations never shift the cuts.

| Clip | Brief beat | Film frames (retained) | Generate | Start image |
|---|---|---|---|---|
| C1 | 0:00–0:04 extreme wide, glide toward him | 0–95 (96) | 5 s | Still S1 |
| C2 | 0:04–0:09 backward track, five steps | 96–215 (120) | 6 s | C1 frame 96 |
| C3 | 0:09–0:13 push in to left eye, ripple | 216–311 (96) + 6 handle | 5 s | C2 frame 120 |
| C4 | 0:13–0:18 grave flashback, one arc | 312–431 (120) | 6 s | Still S2 |
| C5 | 0:18–0:25 waterline leg, tilt up, medium, light kindles | 432–599 (168) | 8 s | Still S3 |
| C6 | 0:25–0:29.5 rising pull-back, flare | 600–707 (108) | 5 s | C5 frame 168 |
| — | 0:29.5–0:30 pure white hold | 708–719 (12) | assembly | — |

Total 96+120+96+120+168+108+12 = 720.

**Chaining rule.** For a chained clip, the next clip's start image is the exact frame at
the trim point `n` (the first frame NOT retained). Retained frames are `[0, n)` and the next
clip begins with its own frame 0. There is no duplicate frame and no drift.
**Ripple dissolve** (film frames 312–317): C3 retains 6 handle frames (96–101) that are
cross-dissolved with C4 frames 0–5 through a radial ripple in assembly.
**Cuts:** only at 312 (dissolve) and 432 (hard cut). C4 and C5 start from fresh stills.

## D3. Start stills
- V01 makes three stills, 2k, 16:9, from the reference image: S1 (C1 extreme wide,
  present-day design, anime style), S2 (younger self at the grave, dusk sepia), S3
  (waterline close-up of his leading leg, matched to S1's river look).
- Bake-off: `alibaba/qwen-image-3/edit` ($0.075, set `prompt_extend: false`) vs
  `xai/grok-imagine-image-2.0` ($0.09). Up to 2 candidates per model per still.
- S1 is also the **style anchor**: its prompt block and image are passed to every river clip.
- The first submit of V01 measures the real OLU per USD; record it in `production/sequence.json`.

## D4. Audio
- Kling native sound on each clip = water, wind and footstep **ambience only**. If a clip's
  sound has speech, singing or obvious seam pops, mute it and use synthesized water ambience.
- Monologue "I had once screamed, gradually, I lost my voice.": generated in the VM with
  Kokoro-82M (Apache-2.0), a low adult male voice, slowed, pitched down, with echo; starts
  0:12, finishes by 0:17. Fallback if Kokoro will not install: Piper (MIT).
- Score and cues (drone, taiko hits on each reviewed footstep plant plus 0:03 and 0:18,
  low cello ostinato, choir/throat hum, erhu note, crystalline hum, temple bell, strings):
  synthesized procedurally in the VM, or CC0-licensed samples with source URL and licence
  recorded. No copyrighted music. The 0:10–0:12 muffle and the 0:27.0–0:27.5 digital silence
  are applied in the mix.
- Rights record: `production/audio_rights.json`.

## D5. Spending authorization
- Paid Higgsfield submits are authorized without asking, within:
  - 50 OLU per session all-in, keeping 10 OLU in reserve (unchanged);
  - at most 3 attempts per clip or still;
  - a film-wide generation ceiling of **$60 of Higgsfield estimates** (about four full passes
    of D2 at 4K). Stop and ask the user before exceeding it.
- Always call the estimate endpoint with the exact submit body first. Estimates are free and
  may be retried; if none succeeds, do not submit (the platform refuses anyway).
- Never resubmit a job with an unknown outcome (submit journal rules still apply).

## D6. Review and acceptance
- Each production session first reviews the previous session's output in a fresh context
  (this replaces separate Q sessions): full playback frames at 24 fps for motion, dense
  frames around trim points, the trim frame itself, and a vision check with Claude Opus 5.5
  (`llm_config` id `0edabd39-3d21-42cb-9cfd-bc2c494eda84` in project p-fc80a416-c97c)
  against the brief and bibles.
- Accept, or reject with reason codes. A rejected clip is regenerated (D5 attempt limit) and
  every later clip in the same take becomes stale.
- The user delegated visual-master approval: the reviewing session's acceptance of S1, S2,
  S3 counts as approval, recorded with this file as its source. The final film still gets a
  one-line user confirmation before it is called delivered.

## D7. Conform
Every clip is conformed before trimming: decode, convert to 24 fps by timestamp if the
source is not 24 fps, scale to 1920x1080 (lanczos), centre-crop if not 16:9, then trim by
the D2 frame map. Record source resolution and fps.

## D8. Session order
| Task | Work | Paid |
|---|---|---|
| S01 | Rewrite repo to implement D1–D8; verify Kokoro installs | No |
| V01 | Stills S1, S2, S3 (bake-off); measure OLU/USD | ~$0.5 |
| V02 | Review stills; C1 | ~$2.1 |
| V03 | Review C1; C2 | ~$2.5 |
| V04 | Review C2; C3 | ~$2.1 |
| V05 | Review C3; C4 flashback | ~$2.5 |
| V06 | Review C4; C5 | ~$3.4 |
| V07 | Review C5; C6 | ~$2.1 |
| V08 | Review C6; audio, assembly, final QA, user confirmation | No |

If a session's budget cannot fit its clip plus review, it stays `in_progress` and the next
session continues it.