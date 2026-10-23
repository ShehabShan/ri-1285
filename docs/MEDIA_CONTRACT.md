# Frame-exact media and assembly contract
## Locked delivery profile (implementation choice subordinate to brief)
1920x1080, square pixels, 16:9, progressive constant **24/1** fps (NOT 23.976),
SDR Rec.709 primaries/transfer/matrix, declared limited-range video, no letterboxing.
This is the consistent delivery baseline, not a claim 4K generation is inherently better.
Keep native originals. Downscale once using a recorded high-quality filter; do not upscale
a sub-1080 candidate to conceal missing detail. Colour conversions must respect actual
input range/transfer; tagging is not conversion. Unknown source colour => inspect/test,
record a justified interpretation, do not assume. Scene-linear compositing if used must
have explicit input/output transforms; no double gamma or double grain.
Working conformed masters: lossless FFV1 in Matroska with recorded pixel format/colour,
24 fps. Delivery MP4 H.264 high-quality (CRF <=16, yuv420p, faststart) + AAC 48k stereo
>=320k. Retain lossless image+PCM master (not judged from delivery compression only).
AAC introduces delay; validate decoded playback alignment; master PCM is timing authority.

## Timeline: zero-based, half-open ranges
`production/timeline.json` is authoritative. Final frames 0..719, duration 30.000.
| Part | Final range [start,end) | Retained frames | Normalized candidate samples |
|---|---|---|---|
| A | [0,96) | 96 | 97 (0..96, final K2 is boundary-only) |
| B | [96,216) | 120 | 121 (0..120, final K3 is boundary-only) |
| C | [216,312) | 96 | 96 (K4 on local95 / global311) |
| D | [312,432) | 120 | 120 (K6 local119 / global431) |
| E | [432,552) | 120 | 121 (final K8 is boundary-only) |
| F | [552,708) | 156 | 156 (K9 local155 / global707) |
| White | [708,720) | 12 | composited pure white, held to end |

For A/B/E generate/conform N+1 samples over N/24 seconds of MOTION, including exact
start and shared-boundary endpoints. Retain first N, discard predecessor's boundary-only
last sample; the next segment's exact first sample appears ONCE at the join.
For terminal C/D/F, endpoints lie at the first and last displayed samples;
their motion spans are (N-1)/24 seconds. End-exclusive scene boundary is one sample later.
Keyframe timestamps in human docs name boundaries, not extra frames.
No removal of the next first sample and no extra white endcard added beyond 720.
Native generation duration and decoded sample count differ by vendor. Probe actual
fps, PTS/count and endpoint presence; map to these sample coordinates explicitly.
Retiming policy compares endpoint-to-endpoint source span with target motion span.
Keep explicit interpolation method, source/output index mapping, encoder command, measured
speed ratio and visual verdict. Do not silently rely on ffmpeg -r duplicating frames.
If only 5s output is available for a 4s segment, ~1.25 speed violates the 1.15 limit:
exclude that candidate/model or ask for a different authorized strategy.

## Transitions without lost time
- C's eye close-up is reached by frame288 (12s); the reflection ripple occupies the
  final second and fills frame by C end. K4 is ALWAYS a real endpoint image. Choose
  `ripple_generated` or `eye_for_post` in its metadata. In eye_for_post mode, T11 must
  provide a moving, tracked ripple-composited C candidate as well as the raw eye clip;
  it must pass before assembly, never freeze C's last image for a second.
- Ripple D entry is an in-place overlay, not a duration-shortening xfade. Default
  transition window is D frames312..317 (6 frames): C's already frame-filling abstract
  ripple settles/reveals D using a moving handle or procedural effect with saved recipe.
  This is the ONE dissolve beginning at13s; no earlier D image or second silhouette.
  D's camera/action continues under it. No frozen face ghost over the younger self.
  Six-frame duration is an implementation choice; revise explicitly with review, never
  move scene boundaries or steal D's 5s. Effect parameters/handles/hashes required.
- Frame432 (18s) is the hard cut to E's foot plant: no interpolation or warm-frame bleed.
- K9 at707 is near-white but still coherent; from708 (29.5s) bloom to pure white and
  hold all 12 samples through719. No added cut, black flash, duplicate or fade back.
- No optical-flow repair unless scoped, reversible and independently reviewed. No hidden
  silhouette swaps under spray/light, extra cuts or inserted neutral frames.
`tools/assemble.py` deliberately refuses to invent a ripple recipe: it consumes a reviewed,
already composited 120-frame D entry asset. Plain D is not a release-ready substitute.

## Audio sample contract
PCM WAV stereo 48000 Hz, 24-bit preferred, exact **1,440,000** samples/channel.
Keep separate score, water/wind/footstep SFX and off-screen voice stems plus mix.
Only intelligible speech is exactly:
"I had once screamed, gradually, I lost my voice."
Adult low/calm/flat voice starts at12s (576000); finishes by17s (816000).
Echo tail cut at18s (864000); massive drum/plant there. Record measured speech and tail
times. Native clip audio is discarded. Place step hits using reviewed actual plant times,
not assumed 1Hz if visuals differ. B still must have five steps, and 4–10s drum cues
continue into C. C muffling starts10s, erhu13–18s, build20–27s, bell at27.5s.
**Total silence [27,27.5) = samples1296000..1319999** on ALL stems and mix: no reverb,
dither noise, hidden voice or limiter release. Apply the silence after FX; test PCM zeros.
Delivery lossy codec may ring across a boundary: inspect decoded output and align/extend
codec-safe mute as needed without shifting cues; retain PCM master for exact proof.
No clipping; record true-peak/loudness measurement (delivery target -16 LUFS integrated,
<=-1 dBTP, artistic dynamics preserved; no normalizing the silence away).
Listen for invented words in choir/chant; confirm rights/source/license for every asset.
No audio source decision => T15 `needs_user`, not silent final delivery.

## Reproducibility and final release
A T16 assembly package contains input asset IDs/hashes, exact edit/FX recipe and tool
versions, ffmpeg command(s), LUT/grade/grain settings, audio stem sample placements,
probe output and resulting hashes. Do not accept a command that references /tmp or
another bot's filesystem. Hash any external Release download and check byte size.
Run scaffold validator, task gate and `--delivery` for candidate technical checks BEFORE Q18. After Q18 approves, run `--release`; automated pass is necessary but
not sufficient. Independently review the final encoded file after any mux/transcode,
not just its source. Verify 720 decoded CFR frames, zero start PTS, audio sync/duration,
720-frame semantic report, both transition coordinates, final pure-white pixels,
no residual generated audio, no logos/black edges. Record delivery/user approval.

## Raw endpoints vs intentional composites
Raw C must match its declared K4 eye/ripple endpoint and pass every source-frame check.
A tracked C ripple composite intentionally replaces pixels in the eye reflection; keep
the raw and composed hash/evidence, never use effect coverage to waive a failed face.
Raw D must match K5/K6; D_entry intentionally reveals K5 over its first six frames.
Its altered entry is reviewed as the single prescribed transition, not held to exact
unobscured K5 pixel equality while the ripple is visible. Both raw D and D_entry need
acceptance; a transition cannot hide a bad underlying frame.
