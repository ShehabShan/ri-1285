# Durable production state
JSON files are source-of-truth contracts, never chat memory. Scaffolding CI passing
means only the *contract* is internally valid. All media/lock registries start empty.

## Task transitions
`blocked` -> `ready` only when dependencies are done AND required assets accepted.
`ready` -> `in_progress` only with serialized pushed claim/session URL and next_action.
Candidate-producing T task -> `done` only with all candidate files and evidence registered.
Its Q task -> `ready`; Q task -> `done` only with accepted, current output review reports.
Reject => keep the attempt, reopen T as `in_progress`, Q blocked; never set done on rejection.
`needs_user` is manually cleared only after the exact decision/authority is committed.
Never auto-clear a needs_user state merely because dependencies finished.
A rejected review may end one session; a subsequent fresh producer session reopens T.
Record all attempted versions in immutable paths; active asset IDs refer to chosen
revision, attempt archives keep old paths/hash metadata. Never reuse mutable bytes.
If asset content changes, mark descendant assets stale and downstream tasks blocked.
Even edits to evidence/recipes require a review-hash update and requalification.

## Asset schema (per ID in assets.json)
```
{
  "path": "media/clips/attempts/B_002.mkv",
  "sha256": "<64 hex>",
  "bytes": 123,
  "kind": "video",
  "status": "candidate",
  "producer_session": "<unique fresh-session identifier/source>",
  "inputs": {"K2": "<hash>", "K3": "<hash>", "A": "<hash>", "...": "..."},
  "locks": {"image": "<image_recipe hash>", "river": "<river_recipe hash>"},
  "review": "production/reviews/B_002.json"
}
```
All local paths repo-relative, even for >50MB Release downloads restored locally.
For external storage also record `release_url`, `download_bytes`, `sha256`,
`proxy_asset_id`, and instructions in a committed manifest. Native original/probe/
request/evidence are separate hashed input assets or review evidence entries.
No authentication secret, vendor signed transport URL or token in any record.
A lineage hash alone is insufficient: upstream must remain accepted and valid.

## Lock schema (per name in locks)
`{"asset_id":"image_recipe","sha256":"<recipe bytes sha256>"}` (or river_recipe).
Recipe document includes actual endpoint/model version or unpinned service proof,
all supported explicit settings and ordered reference roles, prompt block versions,
master comparison, supported native durations/fps/resolution, and selection evidence.
Lock acceptance follows the recipe's owning Q review; a table in MODELS is only a view.

## Review schema
See QUALITY_GATE. Review `sha256` binds exact candidate bytes; registry also stores
`review_sha256` to detect editing the report after promotion. Required criteria come
from its Q task. Each criterion has `id`, `status`, `reason`, `evidence` paths.
Each evidence entry has portable `path` and `sha256`. Scores use explicit dimensions:
`identity_drawing`, `composition_camera`, `line_material`, `colour_light_depth`,
`acting_motion`, `fluid_cloth_hair`, `temporal_stability`, `seam_integration`,
`emotional_pacing` (see validator for audio dimensions).
Each score has numeric `score`4–5, reason and evidence; non-motion static items may
use a justified `not_applicable` rather than pretend to move.
Report includes `input_hashes` and `lock_hashes` exactly equal to the candidate lineage.
`producer_session` differs from `reviewer_session`; user_approval for masters/final is
`{"source":"<message or review link>","sha256":"<candidate hash>"}`.
Full-frame video evidence records inspected ranges and whether normal/slow playback
was possible; if not, HOLD. No empty token checklists as artistic proof.

## Commands
- `python3 tools/validate.py`: contracts and all existing claims/provenance.
- `python3 tools/validate.py --task T03`: dependency/input/model gates, no generation.
- `python3 tools/render_queue.py`: regenerate readable queue; no silent status promotion.
- `python3 tools/assemble.py`: fail-closed T16 input check + mechanical concat/master/mux.
- `python3 tools/validate.py --delivery`: checks final candidate mechanics before Q18, no approval claim.
- `python3 tools/validate.py --release`: fail until final media, PCM and approval exist.
- `python3 -m unittest discover -s tests -v`: includes synthetic FFmpeg smoke test.

Automatic checks are necessary but cannot authenticate a pasted approval citation,
watch a character act, or replace an independent viewer. Required CI/PR branch rules
are an administrator control, not automatically enabled by committing workflow YAML.

## Packages with sibling outputs
Within one producer task, all sibling candidate outputs are reviewed together.
Use task inputs as accepted lineage; supporting sibling files/selected model comparisons
belong in the hashed review-evidence package, not a circular accepted-input graph.
For example image_recipe cites four-view images as evidence; it must not require its
own image lock. motion_anchor cites A as hashed review evidence. After Q09, later tasks
consume accepted A AND motion_anchor and the river lock.
Recipes/boundary metadata use the owning gate's craft rubric to judge the visual results
they document; do not claim the JSON itself has acting or drawing quality.
On invalidation, archive prior asset/review records and their immutable files under
production/archive/ (unselected history), remove stale active IDs, block/reopen tasks
and rebuild forward. History is never deleted, and stale bytes cannot be promoted.
A review task can span multiple fresh sessions. Explicit user approval may arrive
after its independent review; keep in_progress/needs_user until the exact package
is approved, then finalize in a new session without regenerating it.

When completing T/Q handoffs, `session` names the final producing/reviewing fresh
session and matches the corresponding asset/report producer/reviewer IDs. If inputs
were made over multiple sessions, retain those earlier attempts with their session
IDs in the archive; the final integrated package is authored and reviewed explicitly.
Record authentic session URLs; these fields prevent accidental self-acceptance,
not a malicious writer forging multiple identities.

## Media provenance and retiming
Every image/video/audio asset includes `provenance.mode` (`generated`, `derived`,
`licensed_source`) and `provenance.files`: [{role,path,sha256}]. Required roles:
- generated: native original, resolved request, terminal_job response;
- derived: exact recipe and source_manifest (hashes, commands and tool versions);
- licensed_source: rights documentation (plus source identity in manifest).
All evidence files are durable and hashed, not a vendor link.
Each A–F candidate has `conform` with source_motion_span, target_motion_span (endpoint
sample spans in seconds), method, endpoint_evidence, index_mapping_path and its
index_mapping_sha256. Validator checks the speed limit numerically; the reviewer
still verifies actual source measurements and cadence. Endpoint evidence names
hashed review evidence; an index map alone cannot prove interpolation looks good.
