# Pipeline

## Approach: keyframe-first

Video models produce short clips, but the brief requires two *unbroken* takes: 13 s and 12 s. Each take is therefore built from segments that join seamlessly. Seamless joins come from **shared boundary keyframes**. A segment's last frame and the next segment's first frame are the same locked still. Every segment is generated in first-frame + last-frame mode from its two keyframes. This makes the segments independent: they can be generated in any order, by any session.

## Stages

| Stage | Output | Tasks |
|---|---|---|
| 0. Setup | Repo scaffold | T01 |
| 1. Model survey | `docs/MODELS.md`: available models, supported inputs, durations, cost | T02 |
| 2. Design locks | Character sheets (present-day and younger self), river style frame | T03–T05 |
| 3. Keyframes | K1–K9 stills (`keyframes/KEYFRAMES.md`) | T06–T08 |
| 4. Segments | Clips A–F (`segments/`) | T09–T14 |
| 5. Audio | Score, SFX and monologue as a separate track | T15 |
| 6. Assembly | Rough cut with transitions and the white-out | T16 |
| 7. Consistency pass | Video-to-video harmonisation of the assembled cut | T17 |
| 8. Final QA | Check against the brief's FIXED list, then export | T18 |

Each stage is gated: a stage starts only after the assets it depends on are `accepted`.

## Model policy

- **No model is hardcoded.** At generation time the session picks the highest-quality model available that supports what the task needs:
  - character sheets and keyframes: image generation with reference-image conditioning
  - segments: image-to-video with **both a first frame and a last frame**
  - consistency pass: video-to-video with style or reference conditioning
- **Quality first.** Cost is a constraint, not the goal. Inside the 50 OLU session budget, pick the best model.
- **Lock after first success.** Once the first river segment is accepted, every other river segment uses the same model, version and core settings. This prevents look drift. Record the lock in `docs/MODELS.md`. The flashback (D) may use a different model only if it gives clearly better quality.
- Record the exact model path and version in each attempt row.

## Durations and conforming

Some segment lengths may not match the durations a model supports. In that case, generate the closest supported duration and conform the clip by **retiming** it, within ±15%. Do not trim it, because trimming would discard the frame that matches the keyframe. Note the retime factor in the attempt row.

## Seams

- A→B, B→C and E→F are invisible joins. At assembly, drop the duplicated first frame of the following segment.
- Inspect every seam frame by frame for pops in camera, lighting, water, hair or robe.
- If a seam pops, regenerate the shorter side first. As a last resort, use a 2–4 frame optical-flow blend. Never use a visible dissolve.

## Transitions and effects (assembly)

- **0:13 ripple dissolve, C→D.** If segment C does not resolve into a frame-filling ripple, build the ripple in post from C's last frame. Then dissolve into D while warming the grade.
- **0:18 hard cut, D→E.** No transition at all.
- **0:29.5–0:30 white-out.** Bloom F's last frames to pure white and hold white until 0:30.000.
- **Grades.** Cold river grade for A–C and E–F. Amber-sepia with heavier grain and a vignette for D.

## Audio

Audio is produced as a separate track and mixed at assembly. The clips are not expected to carry usable audio. The brief's audio cues are the spec. No lip-sync anywhere. The monologue is an off-screen voice-over.

## Consistency pass

After assembly, one video-to-video pass harmonises line weight, palette and character details across segments.
- It must not add cuts, change timing, or change the content of any frame (camera, action, composition).
- Judge it against `bible/` and the locked character sheets, not just against the rough cut. A restyle pass can introduce drift of its own.
- Re-check every seam and every FIXED item afterwards. Keep the rough cut if the pass makes things worse.

## Storage

- Images and clips are committed under `media/`.
- Files over 50 MB are attached to a GitHub Release, with the link committed instead.