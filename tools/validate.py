#!/usr/bin/env python3
"""Fail-closed accounting/provenance gates; explicitly NOT an artistic classifier."""
import argparse
import hashlib
import json
import subprocess
import sys
import wave
from pathlib import Path

BRIEF_HASH = "4027727c897c20c10a9f2ef1037851ed14a3cfc273a47e82d5d2b56380419432"
RANGES = {"A": (0, 96, 97), "B": (96, 216, 121), "C": (216, 312, 96),
          "D": (312, 432, 120), "E": (432, 552, 121), "F": (552, 708, 156)}
CRAFT = ["identity_drawing", "composition_camera", "line_material",
         "colour_light_depth", "acting_motion", "fluid_cloth_hair",
         "temporal_stability", "seam_integration", "emotional_pacing"]
AUDIO_CRAFT = ["performance_timbre", "arrangement", "timing_sync",
               "intelligibility", "mix_cleanliness"]
STATUSES = {"blocked", "ready", "in_progress", "needs_user", "done"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format",
        "-of", "json", str(path)], text=True))


class Gate:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.errors = []
        self.state = load(self.root / "production/state.json")
        self.timeline = load(self.root / "production/timeline.json")
        registry = load(self.root / "production/assets.json")
        self.assets, self.locks = registry["assets"], registry["locks"]
        self.tasks = {t["id"]: t for t in self.state["tasks"]}
        self.unresolved_jobs = []
        self.asset_cache = {}

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def path(self, value):
        """All durable local references must be portable and stay inside repo."""
        p = Path(value)
        candidate = (self.root / p).resolve()
        if not value or p.is_absolute() or not candidate.is_relative_to(self.root):
            raise ValueError(f"unsafe repo path: {value!r}")
        return candidate

    def file_ok(self, path, sha, label):
        try:
            p = self.path(path)
            return self.check(p.is_file() and digest(p) == sha, f"{label}: missing or hash mismatch {path}")
        except (ValueError, OSError):
            return self.check(False, f"{label}: invalid path {path!r}")

    def timeline_ok(self):
        t = self.timeline
        self.check(t["fps"] == 24 and t["total_frames"] == 720, "timeline: 24/1 and 720 required")
        self.check((t["width"], t["height"]) == (1920, 1080), "timeline: delivery profile changed")
        self.check(t["sample_rate"] == 48000 and t["audio_samples"] == 1440000, "timeline: audio length")
        self.check(t["silence_samples"] == [1296000, 1320000], "timeline: silence placement")
        self.check(t["white"] == [708, 720] and t["ripple"] == [312, 318]
                   and t["hard_cut"] == 432, "timeline: transition/white window")
        self.check(set(t["segments"]) == set(RANGES), "timeline: segment IDs")
        for sid, (start, end, samples) in RANGES.items():
            x = t["segments"][sid]
            self.check(x["range"] == [start, end] and x["retained_frames"] == end-start
                       and x["candidate_frames"] == samples
                       and x["discard_last_endpoint"] == (sid in "ABE"), f"timeline: {sid} accounting")
        pairs = [("A", "B"), ("B", "C"), ("E", "F")]
        for a, b in pairs:
            self.check(t["segments"][a]["end_keyframe"] == t["segments"][b]["start_keyframe"],
                       f"timeline: shared endpoint {a}/{b}")

    def asset_ok(self, aid, accepted=False, visiting=None):
        visiting = set() if visiting is None else visiting
        if not self.check(aid in self.assets, f"missing asset: {aid}"):
            return False
        if not self.check(aid not in visiting, f"asset dependency cycle: {aid}"):
            return False
        if (aid, accepted) in self.asset_cache:
            return self.asset_cache[(aid, accepted)]
        before = len(self.errors)
        a = self.assets[aid]
        producers = [t for t in self.tasks.values() if t["kind"] != "review" and aid in t["outputs"]]
        if producers:
            self.check(len(producers) == 1, f"{aid}: duplicate producer tasks")
            owner = producers[0]
            self.check(set(owner["requires"]).issubset(a.get("inputs", {})),
                       f"{aid}: required producer input lineage absent")
        self.check(a.get("status") in {"candidate", "accepted", "rejected", "stale"}, f"{aid}: status")
        self.check(bool(a.get("producer_session")), f"{aid}: producer session required")
        self.check(a.get("kind") in {"image", "video", "audio", "document", "recipe", "boundary"},
                   f"{aid}: kind required")
        if accepted:
            self.check(a.get("status") == "accepted", f"{aid}: not accepted ({a.get('status')})")
        if not self.file_ok(a.get("path", ""), a.get("sha256", ""), aid):
            return False
        self.check(a.get("bytes") == self.path(a["path"]).stat().st_size, f"{aid}: byte size mismatch")
        for upstream, sha in a.get("inputs", {}).items():
            self.asset_ok(upstream, True, visiting | {aid})
            self.check(self.assets.get(upstream, {}).get("sha256") == sha, f"{aid}: stale input {upstream}")
        self.check("inputs" in a and "locks" in a, f"{aid}: explicit input/lock lineage required")
        for name, sha in a.get("locks", {}).items():
            lock = self.locks.get(name, {})
            self.check(lock.get("sha256") == sha, f"{aid}: stale/missing lock {name}")
            target = lock.get("asset_id")
            if target:
                self.asset_ok(target, True, visiting | {aid})
                self.check(self.assets.get(target, {}).get("sha256") == sha, f"{aid}: lock hash differs {name}")
        if a.get("kind") in {"image", "video", "audio"}:
            provenance = a.get("provenance", {})
            mode = provenance.get("mode")
            self.check(mode in {"generated", "derived", "licensed_source"},
                       f"{aid}: media provenance mode required")
            files = provenance.get("files", [])
            self.check(bool(files), f"{aid}: native/source/payload evidence required")
            roles = {f.get("role") for f in files}
            required_roles = ({"native", "request", "terminal_job"} if mode == "generated" else
                              {"recipe", "source_manifest"} if mode == "derived" else {"rights"})
            self.check(required_roles.issubset(roles), f"{aid}: missing provenance roles")
            for f in files:
                self.file_ok(f["path"], f["sha256"], f"{aid} {f.get('role')}")
            if aid in RANGES:
                conform = a.get("conform", {})
                try:
                    target = (RANGES[aid][2]-1)/24
                    source = float(conform["source_motion_span"])
                    self.check(abs(float(conform["target_motion_span"])-target) < 1e-6,
                               f"{aid}: wrong endpoint target span")
                    ratio = source/target
                    self.check(0.85 <= ratio <= 1.15, f"{aid}: speed ratio outside allowed 15%")
                    self.check(bool(conform.get("method")) and bool(conform.get("endpoint_evidence"))
                               and bool(conform.get("index_mapping_path")),
                               f"{aid}: conform mapping/endpoints required")
                    if conform.get("index_mapping_path"):
                        self.file_ok(conform["index_mapping_path"], conform.get("index_mapping_sha256", ""),
                                     f"{aid} conform index map")
                except (KeyError, ValueError, TypeError):
                    self.check(False, f"{aid}: missing/invalid endpoint-span conform record")
        if a.get("status") == "accepted":
            self.review_ok(aid)
        result = len(self.errors) == before
        if result:
            self.asset_cache[(aid, accepted)] = result
        return result

    def review_ok(self, aid):
        a = self.assets[aid]
        report_path = a.get("review")
        try:
            r = load(self.path(report_path or ""))
            self.file_ok(report_path, a.get("review_sha256", ""), f"{aid} review report")
        except (ValueError, OSError, json.JSONDecodeError):
            self.check(False, f"{aid}: missing/invalid independent review")
            return
        self.check(r.get("asset_id") == aid and r.get("sha256") == a["sha256"], f"{aid}: review hash/ID differs")
        self.check(bool(r.get("reviewer_session")) and r.get("reviewer_session") != a.get("producer_session"),
                   f"{aid}: independent fresh-session reviewer required")
        self.check(r.get("producer_session") == a.get("producer_session"), f"{aid}: producer differs in review")
        self.check(r.get("verdict") == "accepted", f"{aid}: review verdict not accepted")
        self.check(r.get("input_hashes") == a.get("inputs") and r.get("lock_hashes") == a.get("locks"),
                   f"{aid}: review input/lock lineage mismatch")
        if a.get("kind") == "video":
            inspected = r.get("inspection", {})
            self.check(inspected.get("normal_playback") is True and inspected.get("slow_playback") is True
                       and inspected.get("all_frames") is True and bool(inspected.get("frame_ranges")),
                       f"{aid}: complete normal/slow/all-frame inspection required")
            count = RANGES[aid][2] if aid in RANGES else (120 if aid == "D_entry" else
                    (720 if aid in {"rough", "finished", "final"} else None))
            if count:
                self.check(inspected.get("frame_ranges") == [[0, count]],
                           f"{aid}: all-frame range must cover [0,{count})")
        owners = [t for t in self.tasks.values() if t["kind"] == "review" and aid in t["outputs"]]
        self.check(len(owners) == 1, f"{aid}: exactly one owning review task required")
        owner = owners[0] if len(owners) == 1 else {}
        criteria = r.get("criteria", [])
        results = {x["id"]: x for x in criteria}
        self.check(len(results) == len(criteria), f"{aid}: duplicate criterion IDs")
        required = owner.get("criteria", [])
        self.check(set(required).issubset(results), f"{aid}: missing required criteria")
        # Reports may not bury a failed optional criterion under overall acceptance.
        for cid, c in results.items():
            self.check(c.get("status") == "pass" or
                       (cid not in required and c.get("status") == "not_applicable" and c.get("reason")),
                       f"{aid}: {cid} not passed")
            self.check(bool(c.get("reason")) and bool(c.get("evidence")), f"{aid}: {cid} lacks evidence/reason")
        evidence = r.get("evidence", [])
        self.check(bool(evidence), f"{aid}: review evidence files required")
        paths = {e["path"] for e in evidence}
        for e in evidence:
            self.file_ok(e["path"], e["sha256"], f"{aid} review evidence")
        for c in results.values():
            self.check(set(c.get("evidence", [])).issubset(paths), f"{aid}: criterion evidence not hashed")
        scores = r.get("scores", {})
        # Metadata-only recipe/boundary/doc still need craft if owning gate demands it.
        dimensions = AUDIO_CRAFT if a["kind"] == "audio" else CRAFT
        if "craft" in required:
            self.check(set(dimensions).issubset(scores), f"{aid}: incomplete craft dimensions")
            for dimension in dimensions:
                x = scores.get(dimension, {})
                if x.get("not_applicable"):
                    allowed = ((a["kind"] not in {"video", "audio"} and dimension in
                                {"acting_motion", "fluid_cloth_hair", "temporal_stability", "seam_integration"})
                               or (dimension == "seam_integration" and aid in {"A", "D", "D_entry", "E"}))
                    self.check(allowed and bool(x.get("reason")),
                               f"{aid}: invalid N/A craft dimension {dimension}")
                else:
                    self.check(isinstance(x.get("score"), (int, float)) and 4 <= x["score"] <= 5
                               and bool(x.get("reason")) and bool(x.get("evidence"))
                               and set(x.get("evidence", [])).issubset(paths),
                               f"{aid}: craft floor/evidence {dimension}")
        if owner.get("user_approval_required"):
            approval = r.get("user_approval") or {}
            self.check(bool(approval.get("source")) and approval.get("sha256") == a["sha256"],
                       f"{aid}: explicit user approval citation for this hash required")

    def task_ok(self, tid, completing=False):
        if not self.check(tid in self.tasks, f"unknown task {tid}"):
            return
        t = self.tasks[tid]
        if not completing and t["kind"] == "production":
            self.check(not self.unresolved_jobs, f"{tid}: recover unresolved jobs before new production")
        self.check(t["status"] in ({"done"} if completing else {"ready", "in_progress"}),
                   f"{tid}: status {t['status']} is not runnable")
        for dep in t["depends"]:
            self.check(self.tasks.get(dep, {}).get("status") == "done", f"{tid}: dependency {dep} not done")
        # Follow dependencies to output assets: "done" cannot disguise missing acceptance.
        for aid in t["requires"]:
            self.asset_ok(aid, True)
        if t["kind"] == "review":
            if completing and tid in {"Q03", "Q09"}:
                name, recipe = ("image", "image_recipe") if tid == "Q03" else ("river", "river_recipe")
                self.check(self.locks.get(name, {}).get("asset_id") == recipe,
                           f"{tid}: accepted recipe must establish {name} lock")
            for aid in t["outputs"]:
                self.asset_ok(aid, completing)
                if completing and aid in self.assets:
                    try:
                        report = load(self.path(self.assets[aid].get("review", "")))
                        self.check(report.get("reviewer_session") == t.get("session"),
                                   f"{tid}: reviewer_session differs from final review task session")
                    except (ValueError, OSError, json.JSONDecodeError):
                        self.check(False, f"{tid}: missing review report")
        elif completing:
            for aid in t["outputs"]:
                self.asset_ok(aid, False)
                if aid in self.assets:
                    self.check(self.assets[aid].get("producer_session") == t.get("session"),
                               f"{tid}: output producer_session does not match claimed task session")
                if aid in {f"K{i}" for i in range(1, 10)}:
                    self.image_ok(aid)
                elif aid in RANGES:
                    self.media_ok(aid, RANGES[aid][2])
                elif aid == "D_entry":
                    self.media_ok(aid, 120)
                elif aid in {"audio_mix", "final_pcm"}:
                    self.pcm_ok(aid)
                elif aid == "final":
                    self.media_ok(aid, 720, final=True)
        # Enforce task-specific locks even when a prose input list is incomplete.
        required_locks = []
        if tid.startswith("T") and tid[1:].isdigit():
            n = int(tid[1:])
            if 4 <= n <= 14:
                required_locks.append("image")
            if n in {10, 11, 13, 14}:
                required_locks.append("river")
        for name in required_locks:
            l = self.locks.get(name, {})
            self.check(bool(l), f"{tid}: missing {name} lock")
            if l:
                self.asset_ok(l["asset_id"], True)
                self.check(self.assets.get(l["asset_id"], {}).get("sha256") == l.get("sha256"),
                           f"{tid}: wrong {name} lock hash")
        if t["kind"] != "review":
            for aid in t["outputs"]:
                if aid in self.assets:
                    a = self.assets[aid]
                    self.check(set(t["requires"]).issubset(a.get("inputs", {})),
                               f"{aid}: required task inputs absent from lineage")
                    self.check(set(required_locks).issubset(a.get("locks", {})),
                               f"{aid}: task lock lineage absent")

    def structure(self):
        self.file_ok("brief/BRIEF.md", BRIEF_HASH, "immutable brief")
        self.check(self.state.get("brief_sha256") == BRIEF_HASH, "state brief hash changed")
        self.file_ok("media/refs/fang-yuan-reference.webp", self.state.get("reference_sha256", ""),
                     "canonical design reference")
        self.timeline_ok()
        self.check(len(self.tasks) == len(self.state["tasks"]), "duplicate task IDs")
        def walk(tid, seen):
            if tid in seen:
                self.check(False, f"task dependency cycle: {tid}")
                return
            for dep in self.tasks[tid]["depends"]:
                if self.check(dep in self.tasks, f"{tid}: nonexistent dependency {dep}"):
                    walk(dep, seen | {tid})
        for tid, t in self.tasks.items():
            self.check(t["status"] in STATUSES, f"{tid}: invalid status")
            walk(tid, set())
            if t["status"] in {"ready", "done"}:
                for dep in t["depends"]:
                    self.check(self.tasks.get(dep, {}).get("status") == "done", f"{tid}: {t['status']} before {dep}")
            if t["status"] == "in_progress":
                self.check(bool(t.get("session")) and bool(t.get("next_action")), f"{tid}: claim/handoff absent")
            if t["status"] == "done":
                self.task_ok(tid, True)
            if t["status"] == "ready":
                for aid in t["requires"]:
                    self.asset_ok(aid, True)
        active = [t for t in self.tasks.values() if t["status"] == "in_progress"]
        self.check(len(active) <= 1, "serialized production: multiple in_progress tasks")
        for aid in self.assets:
            self.asset_ok(aid)
        for name, lock in self.locks.items():
            self.asset_ok(lock["asset_id"], True)
            self.check(self.assets.get(lock["asset_id"], {}).get("sha256") == lock["sha256"],
                       f"{name}: lock registry hash")
        for p in (self.root / "production/jobs").glob("*.json"):
            j = load(p)
            self.check(j.get("status") in {"prepared", "submitted", "running", "unknown",
                                         "succeeded", "failed", "nsfw", "canceled"}, f"{p.name}: job status")
            for key in ["task", "session", "input_commit", "inputs", "request_path",
                        "estimate_path", "submit_time", "olu_upper_bound"]:
                self.check(key in j, f"{p.name}: job missing {key}")
            for key in ["request_path", "estimate_path"]:
                if key in j:
                    self.check(self.path(j[key]).is_file(), f"{p.name}: missing {key}")
            if j.get("status") in {"submitted", "running", "unknown", "prepared"}:
                self.unresolved_jobs.append(p.name)

    def image_ok(self, aid):
        if aid not in self.assets:
            return
        try:
            image = next(s for s in probe(self.path(self.assets[aid]["path"]))["streams"]
                         if s["codec_type"] == "video")
            self.check(image["codec_name"] == "png", f"{aid}: keyframe must decode as PNG")
            self.check(image["width"] >= 1920 and image["height"] >= 1080
                       and image["width"] * 9 == image["height"] * 16,
                       f"{aid}: keyframe below 1080p or not 16:9")
        except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as e:
            self.check(False, f"{aid}: invalid keyframe image ({e})")

    def media_ok(self, aid, expected_frames=None, final=False):
        if aid not in self.assets:
            self.check(False, f"missing media {aid}")
            return
        p = self.path(self.assets[aid]["path"])
        try:
            data = probe(p)
            streams = data["streams"]
            v = next(s for s in streams if s["codec_type"] == "video")
            self.check((v["width"], v["height"]) == (1920, 1080), f"{aid}: not 1920x1080")
            self.check(v["avg_frame_rate"] == "24/1" and v["r_frame_rate"] == "24/1", f"{aid}: not CFR 24")
            self.check(v.get("sample_aspect_ratio") in {"1:1", None}, f"{aid}: nonsquare pixels")
            if expected_frames:
                self.check(int(v["nb_read_frames"]) == expected_frames, f"{aid}: wrong decoded frame count")
            self.check(v.get("field_order") in {"progressive", "unknown"}, f"{aid}: not progressive")
            for key in ["color_space", "color_transfer", "color_primaries"]:
                self.check(v.get(key) == "bt709", f"{aid}: unknown/wrong {key}")
            self.check(v.get("color_range") == "tv", f"{aid}: range not limited")
            if not final:
                self.check(not any(s["codec_type"] == "audio" for s in streams), f"{aid}: generated audio present")
            else:
                self.check(v["codec_name"] == "h264", "final: H.264 required")
                self.check(v.get("pix_fmt") == "yuv420p", "final: yuv420p required")
                self.check(len(streams) == 2, "final: extraneous media streams")
                self.check(abs(float(v.get("duration", 0))-30) < 0.001,
                           "final: video duration not exactly 30s")
                au = [s for s in streams if s["codec_type"] == "audio"]
                self.check(len(au) == 1 and au[0].get("codec_name") == "aac"
                           and au[0].get("sample_rate") == "48000" and au[0].get("channels") == 2,
                           "final: one AAC 48k stereo stream required")
                if au:
                    self.check(abs(float(au[0].get("duration", 0))-30) < 0.022,
                               "final: AAC duration beyond codec padding tolerance")
                    self.check(abs(float(au[0].get("start_time", 0))) < 0.0001,
                               "final: AAC timeline offset")
            # Exact PTS grid, not merely nominal frame-rate metadata.
            frames = json.loads(subprocess.check_output([
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_frames", "-show_entries", "frame=best_effort_timestamp_time",
                "-of", "json", str(p)], text=True))["frames"]
            self.check(all(abs(float(f["best_effort_timestamp_time"])-i/24) < 0.00051
                           for i, f in enumerate(frames)), f"{aid}: nonzero or non-CFR PTS")
            if final:
                raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-vf",
                    "select=gte(n\\,708)", "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
                self.check(len(raw) == 12*1920*1080*3 and raw.count(255) == len(raw),
                           "final: last 12 decoded frames not pure white")
                audio = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p),
                    "-vn", "-ar", "48000", "-ac", "2", "-f", "s16le", "-"])
                self.check(len(audio) >= 1440000*4, "final: decoded AAC too short")
                silence = audio[1296000*4:1320000*4]
                self.check(bool(silence) and not any(silence), "final: decoded AAC silence not zero")
        except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as e:
            self.check(False, f"{aid}: media probe failed ({e})")

    def pcm_ok(self, aid):
        if aid not in self.assets:
            self.check(False, f"missing PCM {aid}")
            return
        try:
            with wave.open(str(self.path(self.assets[aid]["path"])), "rb") as w:
                self.check(w.getframerate() == 48000 and w.getnchannels() == 2
                           and w.getnframes() == 1440000, f"{aid}: PCM layout/duration")
                width = w.getsampwidth()
                self.check(width in {2, 3}, f"{aid}: PCM sample width")
                w.setpos(1296000)
                self.check(not any(w.readframes(24000)), f"{aid}: nonzero silence")
        except (OSError, wave.Error) as e:
            self.check(False, f"{aid}: invalid PCM ({e})")

    def run(self, tid=None, release=False, delivery=False):
        self.structure()
        if release:
            self.check(not self.unresolved_jobs, "release: unresolved paid jobs")
        if tid:
            self.task_ok(tid)
        if release:
            self.check(self.tasks.get("Q18", {}).get("status") == "done", "Q18 final approval not done")
        if release or delivery:
            for aid in ["A", "B", "C", "D_entry", "E", "F", "audio_mix", "final", "final_pcm"]:
                self.asset_ok(aid, accepted=release or aid not in {"final", "final_pcm"})
            for sid in "ABCEF":
                self.media_ok(sid, RANGES[sid][2])
            self.media_ok("D_entry", 120)
            self.media_ok("final", 720, final=True)
            self.pcm_ok("audio_mix")
            self.pcm_ok("final_pcm")
        return not self.errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--task")
    p.add_argument("--release", action="store_true")
    p.add_argument("--delivery", action="store_true", help="final-candidate mechanics before Q18 approval")
    args = p.parse_args()
    try:
        gate = Gate(args.root)
        ok = gate.run(args.task, args.release, args.delivery)
    except (KeyError, ValueError, TypeError, OSError) as e:
        print(f"FAIL invalid registry/state: {e}", file=sys.stderr)
        return 1
    for error in dict.fromkeys(gate.errors):
        print("FAIL", error, file=sys.stderr)
    if ok:
        print("PASS", "release mechanics (art review still required)" if args.release else
              f"task {args.task}" if args.task else "delivery candidate mechanics; approval pending" if args.delivery else "scaffold/provenance only; NOT film acceptance")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())