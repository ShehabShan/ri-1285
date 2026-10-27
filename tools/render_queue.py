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
        "", "## User decisions",
        "- All open decisions were delegated to the bot and are LOCKED in docs/DECISIONS.md (2026-10-27): model, shot plan, stills, audio, spending, review, conform, session order.",
        "- Paid generation is authorized within 50 OLU/session (10 reserve), 3 attempts per item and a $60 Higgsfield-estimate film ceiling.",
        "- Run S01 first (no paid generation).",
        "", "## Handoff", "",
    ]
    for t in state["tasks"]:
        if t.get("next_action"):
            lines.append(f"- **{t['id']}**: {t['next_action']}")
    return "\n".join(lines)+"\n"

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root/"tasks/QUEUE.md").write_text(render(root))