#!/usr/bin/env python3
import json
from pathlib import Path

def render(root):
    state = json.loads((root/"production/state.json").read_text())
    lines = [
        "# Task queue — generated from production/state.json",
        "",
        "Do not edit this view. Resume `in_progress` first; then choose the first eligible",
        "`ready` task. Dependencies require `done`, and required input assets must be",
        "**accepted**, current and available. Run `python3 tools/validate.py --task ID`.",
        "T tasks make candidates; Q tasks independently review. Missing evidence = hold.",
        "",
        "| ID | Task | Depends | Required accepted inputs | Outputs | Status |",
        "|---|---|---|---|---|---|",
    ]
    for t in state["tasks"]:
        row = [t["id"], t["title"], ", ".join(t["depends"]) or "—",
               ", ".join(t["requires"]) or "—", ", ".join(t["outputs"]) or "—", t["status"]]
        lines.append("| " + " | ".join(row) + " |")
    lines += [
        "", "## Open user decisions",
        "- Audio: authorize music/SFX/voice source and rights; T15 stays needs_user until then.",
        "- Paid generation: reliable OLU upper bounds required before submission, not USD guesses.",
        "- Master packages Q03/Q04/Q05 and final Q18 need explicit user approvals for exact hashes.",
        "- Optional generative finishing needs separate user authorization; default is deterministic.",
        "", "## Handoff", "",
    ]
    for t in state["tasks"]:
        if t.get("next_action"):
            lines.append(f"- **{t['id']}**: {t['next_action']}")
    return "\n".join(lines)+"\n"

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root/"tasks/QUEUE.md").write_text(render(root))