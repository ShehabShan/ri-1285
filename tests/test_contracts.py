import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate import Gate, digest
from render_queue import render

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        for name in ["brief","production","media/refs"]:
            shutil.copytree(ROOT/name,self.root/name)
    def tearDown(self):
        self.tmp.cleanup()
    def edit(self, name, fn):
        p=self.root/name;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
    def gate(self,**kw):
        g=Gate(self.root);g.run(**kw);return g
    def test_scaffold_passes(self):
        self.assertEqual(self.gate().errors,[])
    def test_release_fails_with_empty_media(self):
        self.assertTrue(self.gate(release=True).errors)
    def test_brief_mutation_fails(self):
        with (self.root/"brief/BRIEF.md").open("a") as f:f.write("\nmodified")
        self.assertTrue(any("immutable brief" in e for e in self.gate().errors))
    def test_frame_deletion_fails(self):
        self.edit("production/timeline.json",lambda t:t["segments"]["B"].update(candidate_frames=120))
        self.assertTrue(any("B accounting" in e for e in self.gate().errors))
    def test_event_shift_fails(self):
        self.edit("production/timeline.json",lambda t:t.update(hard_cut=431))
        self.assertTrue(any("transition" in e for e in self.gate().errors))
    def test_premature_task_fails(self):
        self.edit("production/state.json",lambda s:next(t for t in s["tasks"] if t["id"]=="T10").update(status="ready"))
        self.assertTrue(self.gate(tid="T10").errors)
    def test_missing_lock_and_inputs_fail(self):
        self.edit("production/state.json",lambda s:next(t for t in s["tasks"] if t["id"]=="T10").update(status="in_progress",session="s",next_action="test"))
        errors=self.gate(tid="T10").errors
        self.assertTrue(any("missing river lock" in e for e in errors))
        self.assertTrue(any("missing asset" in e for e in errors))
    def test_cycle_fails(self):
        self.edit("production/state.json",lambda s:next(t for t in s["tasks"] if t["id"]=="T01").update(depends=["T18"]))
        self.assertTrue(any("cycle" in e for e in self.gate().errors))
    def test_path_traversal_rejected(self):
        g=Gate(self.root)
        self.assertFalse(g.file_ok("../outside","abc","test"))
        self.assertFalse(g.file_ok("/etc/passwd","abc","test"))
    def fixture(self):
        # Valid independent non-art technical preflight document and hashed report.
        evidence=self.root/"evidence.txt";evidence.write_text("Observed preflight evidence")
        asset=self.root/"preflight.txt";asset.write_text("preflight fixture")
        a={"path":"preflight.txt","sha256":digest(asset),"bytes":asset.stat().st_size,
           "kind":"document","status":"accepted","producer_session":"producer",
           "inputs":{},"locks":{},"review":"review.json"}
        s=json.loads((self.root/"production/state.json").read_text())
        criteria=next(t for t in s["tasks"] if t["id"]=="QP01")["criteria"]
        r={"asset_id":"preflight","sha256":a["sha256"],"producer_session":"producer",
           "reviewer_session":"reviewer","verdict":"accepted","input_hashes":{},"lock_hashes":{},
           "criteria":[{"id":i,"status":"pass","reason":"measured","evidence":["evidence.txt"]} for i in criteria],
           "scores":{},"evidence":[{"path":"evidence.txt","sha256":digest(evidence)}]}
        (self.root/"review.json").write_text(json.dumps(r))
        a["review_sha256"]=digest(self.root/"review.json")
        self.edit("production/assets.json",lambda x:x["assets"].update(preflight=a))
        # Isolate evidence mechanics; production input graphs are tested separately.
        self.edit("production/state.json",lambda x:next(t for t in x["tasks"] if t["id"]=="P01").update(requires=[]))
        return a,r
    def update_report(self,r):
        (self.root/"review.json").write_text(json.dumps(r))
        self.edit("production/assets.json",lambda x:x["assets"]["preflight"].update(review_sha256=digest(self.root/"review.json")))
    def test_valid_evidence_gate(self):
        self.fixture()
        self.assertEqual(self.gate().errors,[])
    def test_self_acceptance_fails(self):
        a,r=self.fixture();r["reviewer_session"]="producer";self.update_report(r)
        self.assertTrue(any("independent" in e for e in self.gate().errors))
    def test_unreviewed_criterion_fails(self):
        a,r=self.fixture();r["criteria"][0]["status"]="unknown";self.update_report(r)
        self.assertTrue(any("not passed" in e for e in self.gate().errors))
    def test_rewritten_evidence_fails(self):
        self.fixture();(self.root/"evidence.txt").write_text("different")
        self.assertTrue(any("hash mismatch" in e for e in self.gate().errors))
    def test_rewritten_report_fails(self):
        self.fixture()
        with (self.root/"review.json").open("a") as f:f.write(" ")
        self.assertTrue(any("review report" in e for e in self.gate().errors))
    def test_stale_input_fails(self):
        self.fixture()
        self.edit("production/assets.json",lambda x:x["assets"]["preflight"].update(inputs={"missing":"0"*64}))
        self.assertTrue(any("stale input" in e for e in self.gate().errors))
    def test_rejected_not_consumable(self):
        self.fixture()
        self.edit("production/assets.json",lambda x:x["assets"]["preflight"].update(status="rejected"))
        g=Gate(self.root);g.asset_ok("preflight",True)
        self.assertTrue(any("not accepted" in e for e in g.errors))
    def test_queue_view_current(self):
        self.assertEqual(render(ROOT),(ROOT/"tasks/QUEUE.md").read_text())

    def test_source_reference_mutation_fails(self):
        (self.root/"media/refs/fang-yuan-reference.webp").write_bytes(b"changed")
        self.assertTrue(any("design reference" in e for e in self.gate().errors))
    def test_required_producer_inputs_cannot_be_omitted(self):
        self.fixture()
        self.edit("production/state.json",lambda x:next(t for t in x["tasks"] if t["id"]=="P01").update(requires=["K1"]))
        self.assertTrue(any("producer input lineage absent" in e for e in self.gate().errors))
    def test_low_craft_score_fails(self):
        a,r=self.fixture()
        self.edit("production/state.json",lambda x:next(t for t in x["tasks"] if t["id"]=="QP01")["criteria"].append("craft"))
        r["criteria"].append({"id":"craft","status":"pass","reason":"test","evidence":["evidence.txt"]})
        from validate import CRAFT
        r["scores"]={d:{"score":4,"reason":"measured","evidence":["evidence.txt"]} for d in CRAFT}
        r["scores"]["identity_drawing"]["score"]=3
        self.update_report(r)
        self.assertTrue(any("craft floor" in e for e in self.gate().errors))
    def test_missing_user_approval_fails(self):
        a,r=self.fixture()
        self.edit("production/state.json",lambda x:next(t for t in x["tasks"] if t["id"]=="QP01").update(user_approval_required=True))
        self.assertTrue(any("user approval" in e for e in self.gate().errors))
    def test_unknown_job_blocks_production_not_recovery(self):
        jobs=self.root/"production/jobs";jobs.mkdir(exist_ok=True)
        (self.root/"request.json").write_text("{}")
        j={"status":"unknown","task":"T03","session":"s","input_commit":"a",
           "inputs":{},"request_path":"request.json","estimate_path":"request.json",
           "submit_time":"2026-10-23T08:16:26Z","olu_upper_bound":1}
        (jobs/"test.json").write_text(json.dumps(j))
        self.assertEqual(self.gate().errors,[])
        self.assertTrue(any("recover unresolved" in e for e in self.gate(tid="T03").errors))

    def test_media_provenance_cannot_be_omitted(self):
        a,r=self.fixture()
        self.edit("production/assets.json",lambda x:x["assets"]["preflight"].update(kind="image"))
        self.assertTrue(any("provenance" in e for e in self.gate().errors))
    def test_out_of_bounds_retime_fails(self):
        # Exercise numerical accounting without pretending the payload is a valid film.
        a,r=self.fixture()
        self.edit("production/assets.json",lambda x:x["assets"].update(A={
            **a,"kind":"video","status":"candidate",
            "conform":{"source_motion_span":5,"target_motion_span":4,
                       "method":"test","endpoint_evidence":"evidence.txt",
                       "index_mapping_path":"evidence.txt","index_mapping_sha256":digest(self.root/"evidence.txt")}
        }))
        self.assertTrue(any("speed ratio" in e for e in self.gate().errors))
