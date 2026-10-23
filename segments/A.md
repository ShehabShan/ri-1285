# Segment A — Take 1 opening glide (0:00–0:04)

| Field | Value |
|---|---|
| Status | blocked (needs T02, K1, K2) |
| Part | Take 1, unbroken river take |
| Timeline | 0:00.000–0:04.000 (96 frames at 24 fps) |
| Start keyframe | K1 |
| End keyframe | K2 |
| Before | video start |
| After | B (invisible join) |
| Model | chosen at generation time; follow the river lock in `docs/MODELS.md` once it is set |

## Beat (from the brief)

Extreme wide shot, lens just above the water, slight low angle. He is a small lone figure at frame center, walking toward the camera, upstream, through the raging river. The current flows away from the camera and past him. Waves break against his legs, spray bursts upward, mist drifts across the foreground. The camera glides forward low over the water toward him. By 0:04 it arrives in front of him and starts a backward tracking move at his walking pace, framing him from head to waterline.

## Generation prompt

[STYLE] [CHARACTER] [RIVER]
One continuous camera move. It opens on an extreme wide shot, lens skimming just above the raging water at a slight low angle. Fang Yuan is a small lone figure at frame center, walking toward the camera, upstream. The current runs away from the camera, past him, into the misty distance. Waves break against his legs, spray bursts upward, foreground mist drifts across the lens. The camera glides forward, low over the water, steadily closing the distance. It ends directly in front of him, slightly low, framing him from head to waterline, and begins matching his walking pace backward.

## Segment-specific negatives

water flowing toward the camera, camera passing him, camera rising high, aerial drone shot

## Segment-specific checklist

- [ ] The camera stays low over the water for the whole glide.
- [ ] The figure stays at frame center and grows steadily, with no zoom jump.
- [ ] The wide view shows cliffs at the far edges and endless mist upstream.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T09`.
Candidate sample count: **97** at 24 fps; retained final count:
**96**, range **[0, 96)**.
Last sample is boundary-only and discarded from THIS clip at assembly.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T09 produces candidates only; Q09 independently accepts/rejects.
Match the approved full-film motion language and visual master; no standalone style reinterpretation.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
