# Character bible — Fang Yuan

Fang Yuan is the only person on screen in the whole video. There are no other people, crowds or duplicates.

## Reference image

`media/refs/fang-yuan-reference.webp` defines his **design only**: face, hair, skin, and the cut, material and color of both robes.

**Do not take from it:** the watercolor art style, the seated pose, the closed eyes, the chair, the branch, the background or the warm cream palette.

**Where the brief differs from the image, the brief wins:**
- his eyes are open
- he is standing and walking
- the white inner robe covers his torso **and shoulders**
- the charcoal outer robe has slipped **below both shoulders** and hangs at his upper arms

## Present-day design (every river frame: A, B, C, E, F)

- **Build:** tall, slender young man. Pale skin with a cool undertone.
- **Face:** long narrow face, sharp jaw, straight nose, thin closed lips, narrow dark eyes under straight brows.
- **Hair:** very long, straight, jet black, center-parted, worn loose. Soaked and heavy, streaming behind him.
- **Inner robe:** loose, pure white, cross-collar, wide sleeves, loosely open at the collar. It covers his torso and shoulders.
- **Outer robe:** dark charcoal-black with a faint deep-teal tint and the soft mottled texture of the reference. Worn open, slipped down below both shoulders, hanging loosely at the upper arms. Its long fabric trails behind him in the current.
- **Lower body:** dark loose trousers and dark cloth boots. The boots are always under the water and never visible.
- **Wet fabric:** darker and heavy at the hems.
- **Never:** jewelry, weapons, armor or headwear.

## Present-day expression and movement

- Neutral, emotionless face. Gaze fixed forward, cold and unwavering. Mouth closed.
- No smile, frown, grimace or tears. No lip movement.
- He is alive, not frozen: subtle breathing, natural weight transfer, a slight forward lean into the current.
- A steady, heavy, unhurried walk of about one step per second, without pause, through both river takes.
- Each submerged foot plants firmly. The step reads through his legs, the shift of weight in his torso, and the burst of water at his shins. No sliding, no floating.
- He never stumbles, stops or looks away.

## Younger self (flashback D only)

- Same face as the reference, younger and softer.
- Long black hair **tied back**.
- Plain, worn grey-brown traveler's clothes.
- Fists clenched at his sides, crying openly: tears on his cheeks, lips trembling, shoulders shaking.
- This is the **only** appearance change in the video.

## Locked assets

Filled in by T03 and T04. Every later generation conditions on these.

| Asset | Path | Model | Status |
|---|---|---|---|
| Present-day sheet: front, three-quarter, profile, full body standing | `media/sheets/present_*.png` | — | not started |
| Younger-self sheet | `media/sheets/young_*.png` | — | not started |

## Highest-risk failure modes

These are the errors most likely to appear, so check for them first.

1. The outer robe drifts up onto his shoulders.
2. The white inner robe slips off his shoulders.
3. The hair is shortened, tied up, or loses its center part.
4. The face morphs or loses its identity across a clip.
5. The watercolor style or cream palette bleeds in from the reference.
6. The eyes are closed or glowing.

## Lock and review evidence
The asset tables above are descriptive summaries, not proof of acceptance. Candidate
sheets/style frames must be reviewed through QUALITY_GATE and registered with exact
hashes and approval citations in `production/assets.json`. No downstream session may
consume an unapproved, missing, stale or merely named asset. Changing a locked design/
style invalidates dependent keyframes, clips, seams and edits transitively.
