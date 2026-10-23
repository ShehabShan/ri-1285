# Continuity contract
## Authority and master package
Text brand references ("feature-film", studio names) are not a style lock.
Before downstream work, freeze approved images for present front/three-quarter/profile/
full body; younger design and flashback look; river empty/with-character style frames.
The master package contains full frames and labelled crops of face, hair, covered white
shoulders and dropped charcoal robe, cloth, water/foam, mist, line weight, shadow edges.
It includes a colour script (cold river / warm D / evolving white F), sampled palette
with colour-space labels, lighting diagram and chosen grain/DOF/contrast examples.
Samples guide comparisons; flat global histogram equality is NOT proof of matching art.
Record exact files/hashes, approved image recipe, user approval citation and rationale.
No missing view, placeholder, watermark or unexplained difference across views passes.
Do not copy the source reference's seated pose, closed eyes or watercolor palette.

## Coordinate system and visual axis
Use a plan diagram in the master package: +Z = his upstream advance; current = -Z.
Initial camera is in front looking back along -Z; water moves away from camera.
At three-quarter angles project these vectors; do not substitute a fixed screen arrow.
Record chosen orbit side and extent (creative detail, not a new event), camera elevation,
distance/framing, lens feel/FOV and the visible side of his face. Never mirror footage
to solve direction (it would swap the requested anatomical left eye).
Lock skyline/cliff relationships, waterline at knees, rim-light side/softness, weather,
face readability, hair/collar/robe silhouette and wetness. Gold motes advect downstream.
Take 2 returns to the same river, design and base exposure; only the prescribed internal
white radiance changes. D is intentionally warmer, not a different drawing language.

## Boundary handoff: K2, K3, K8
For each, commit `production/boundaries/<K>.json` plus a diagram and short seam loop.
Specify position/composition scale, camera travel direction and relative velocity,
lens/focus trend, leading leg and gait phase, torso lean/bob, hair/robe/splash direction,
water/foam features, light/exposure state and expected change over +/-12 frames.
Use observable normalized landmark positions/flow descriptions; do not invent physical
lens millimetres, metres/second or exact depth that cannot be verified.
A arriving at K2 smoothly changes from approach to matching backward track BEFORE the
join; no decelerate-to-still then restart. K3 starts the eye approach smoothly.
K8 continues the existing three-quarter move and faint chest light; F holds medium
until 25s before the prescribed rising pull-back. No new orbit at the seam.
Gait is one continuous take clock: phase/weight transfer cannot reset between clips.
B must contain the brief's five planted steps, not "as close as possible".
Review dry loops for motion, silhouette, fluid advection, local brightness/colour and
focus continuity. A matching K image with a zero-velocity hold fails.
Before a predecessor exists, the boundary remains `planned`; only measured neighboring
footage can make it `verified`. Later segment generation reads accepted predecessor
tail (last 0.5s minimum) and report; if API cannot consume video, include still crops/
motion notes as supported conditioning and independently verify the result.
Independent sessions mean independent execution, NOT arbitrary segment order.

## Prompt and reference hygiene
Every submit stores fully expanded shared + specific + boundary text (no unresolved
[STYLE] tokens), negative prompt, input order/roles and hash. Unsupported negative
fields are folded into positive constraints, not silently discarded.
Use the right role references: character for identity, style for rendering, keyframes
for composition, predecessor tail for motion. Never ask a model to copy a collage's
labels/grid/multiple characters into the shot. Reference count limits require an
approved composite/crop that preserves identity and style, with provenance.
Do not rewrite stable shared blocks for taste. Necessary endpoint-specific wording
is recorded as a versioned recipe delta and reviewed for semantic equivalence.
Gold motes, pure-white inner light and warm D are deliberate exceptions, not drift.
River-only rules must not ban D's tears, tied-back hair or amber light.

## Freeze and invalidation
A lock is a named versioned record in assets.json, not a sentence in chat or MODELS.
Every asset lists input asset hashes and lock hashes. No mutable "latest" filenames
or main-branch input URLs; new revisions get new IDs/paths. Any ancestor or lock change
makes downstream products stale, even if their file bytes did not change.
Re-review both sides of every affected seam and all assembled/finished versions.
Mark stale tasks blocked, clear downstream publication flags and regenerate QUEUE.
Keep the old lineage for rollback; a candidate may not be promoted by renaming it.
User approval is specific to the reviewed hashes, never a blanket future acceptance.
