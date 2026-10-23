# Segment F — Take 2 radiance, pull-back and white-out (0:23–0:30)

| Field | Value |
|---|---|
| Status | blocked (needs T02, K8, K9) |
| Part | Take 2, unbroken river take |
| Timeline | 0:23.000–0:29.500 generated (156 frames). The white-out from 0:29.5 to 0:30.000 is done at assembly. |
| Start keyframe | K8 |
| End keyframe | K9 |
| Before | E (invisible join) |
| After | video end |
| Model | follow the river lock in `docs/MODELS.md` |

## Beat (from the brief)

- **0:23–0:25:** Tracking backward in a frontal three-quarter medium shot. The white light inside his chest grows brighter with each step, spreading through his silhouette and lighting the edges of his robe folds. The light catches the moving spray around him. His face and his walk do not change.
- **0:25–0:29.5:** One smooth rising pull-back into a wide shot. The light surges into a blinding flare from inside his body, radiating out through his skin, collar, sleeves and hair edges. Rays of light cut through the mist and spray. He keeps walking upstream, eyes open, expression unchanged. The river keeps raging.
- **0:29.5–0:30:** The flare blooms the frame to pure white and holds white to the end (assembly).

## Generation prompt

[STYLE] [CHARACTER] [RIVER]
One continuous shot. A frontal three-quarter medium shot tracks backward with Fang Yuan as he walks upstream. The pure-white light inside his chest grows brighter with each step. It spreads through his silhouette and lights the edges of his robe folds, catching the moving spray around him. His face and his walk do not change. The camera then makes one smooth, rising pull-back into a wide shot. The light surges into a blinding flare from inside his body, radiating through his skin, collar, sleeves and hair edges. Rays of light cut through the mist and spray. He keeps walking upstream, eyes open, expression unchanged. The river keeps raging around him.

## Segment-specific negatives

external beam, light from the sky, sunburst behind him, glowing eyes, transformation, wings, aura creature, levitation, the river calming, him stopping

## Segment-specific checklist

- [ ] The light originates inside his body only, with no external source.
- [ ] The light grows monotonically. No flicker, no sudden jump.
- [ ] He keeps walking through the whole pull-back.
- [ ] Eyes open and expression unchanged, even at the flare peak.
- [ ] The river keeps raging; it does not calm.
- [ ] The pull-back is smooth and rising, ending on a wide shot.

## Cross-session contract (mandatory)
Queue status is in `production/state.json`; the header is descriptive, not authorization.
Read the whole brief, COMMON, CONTINUITY, QUALITY_GATE and MEDIA_CONTRACT, inspect actual
masters and the approved model/recipe, and run `--task T14`.
Candidate sample count: **156** at 24 fps; retained final count:
**156**, range **[552, 708)**.
Both endpoint samples are displayed; no endpoint may be trimmed.
Retiming uses endpoint-to-endpoint span, not nominal container duration.
Store native and conformed attempts, payloads/locks/hashes, full-frame review and timed
beat evidence. T14 produces candidates only; Q14 independently accepts/rejects.
Inspect approved predecessor E tail and review a +/-12-frame seam loop; static endpoint matching is insufficient.
Hold evolving three-quarter medium framing until600 (25s), then rising pull-back. K9 is global707; final pure-white samples708–719 belong to assembly, not extra running time.

## Attempts

| # | Date | Session | Model + version | Settings | Retime | Cost (OLU) | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
