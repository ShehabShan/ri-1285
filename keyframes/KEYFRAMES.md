# Keyframes

Keyframes are locked stills at segment boundaries. A segment is generated from its start and end keyframes. Neighbouring segments share their boundary keyframe, which constrains pose/composition but does not guarantee an invisible motion join (see `docs/CONTINUITY.md`).

All keyframes are 16:9, at the highest resolution the chosen image model supports (≥1920×1080 target). They are conditioned on the locked character sheets and the river style frame.

| ID | Time | Used by | Frame description | Status |
|---|---|---|---|---|
| K1 | 0:00 | A start | Extreme wide. Lens just above the water, slight low angle. A small lone figure at frame center walks toward camera through raging rapids. The current flows away from camera. Mist drifts across the foreground; cliffs at the far edges. | not started |
| K2 | 0:04 | A end / B start | Camera directly in front of him, slightly low, framing head to waterline. Mid-step, with water erupting at his shins. Hair and outer robe stream behind him. Rim light on hair, face edge and white-covered shoulders. | not started |
| K3 | 0:09 | B end / C start | Same framing as K2, at a different step phase. Medium shot, ready to push in. | not started |
| K4 | 0:13 | C end | Mandatory real endpoint: left-eye ECU with reflected river (`eye_for_post`) or frame-filling reflection ripple (`ripple_generated`). Post route requires a tracked moving C composite before acceptance. | not started |
| K5 | 0:13 | D start | Flashback. From behind the younger self's shoulder: the grave mound and wooden marker in golden grass at amber dusk. | not started |
| K6 | 0:18 | D end | Flashback. Three-quarter profile of the younger self crying, tears catching the dusk light, fists clenched. | not started |
| K7 | 0:18 | E start | Waterline close-up of his leading lower leg driving against the current. Water bursts around the shin toward the lens; the boot is unseen. | not started |
| K8 | 0:23 | E end / F start | Medium shot, frontal three-quarter view, tracking backward. A faint pure-white light glows inside his chest, through the white inner robe. | not started |
| K9 | 0:29.5 | F end | Wide shot. He walks upstream, eyes open, expression unchanged, as a blinding white flare radiates from inside his body. Rays cut through mist and spray. The frame is nearly blown out. | not started |

## Rules

- Every river keyframe must pass the character and river items of `segments/COMMON.md` → Acceptance checklist.
- K2 and K3 share lighting, water level, mist density and costume state. Their gait phases follow the continuous take clock; record measured phase and velocity, never impose a new phase just to make stills differ.
- K7 and K8 must match the river of K1–K3: same water, sky and palette.
- Committed files: `media/keyframes/K<n>.png`, plus the prompt and model used, recorded in this table.

## Endpoint and review contract
K4 is mandatory even when the ripple is composited. K2/K3/K8 require boundary records
and +/-12-frame motion expectations. K1–K9 must be compared together against approved
masters, and registered by content hash before clips consume them. K4/K6/K9 lie on the
last displayed frame before their end-exclusive boundaries (311/431/707 respectively).
The timeline JSON governs sample positions, including A/B/E extra endpoint samples.
A still is not a motion proof: boundary plans remain provisional until real seams pass.
