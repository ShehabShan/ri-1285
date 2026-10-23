#!/usr/bin/env python3
"""Mechanical assembler; inputs must already include reviewed D-entry ripple.
Never fabricates an artistic transition or certifies the resulting film."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from validate import Gate, RANGES, digest, load, probe


def run(cmd):
    subprocess.run(cmd, check=True)


def assemble(inputs, output, pcm, manifest, width=1920, height=1080, smoke=False):
    """Exact endpoint ownership; no xfade, -shortest or incidental timing shifts."""
    if not smoke:
        raise ValueError("Use the CLI for real production so asset/task gates cannot be skipped")
    # Used by CLI only AFTER validation; also exercised with small synthetic frames in tests.
    output, pcm = Path(output).resolve(), Path(pcm).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    work = output.parent / (output.stem+"_work")
    work.mkdir(exist_ok=True)
    commands, masters = [], []
    for sid in "ABCDEF":
        source = Path(inputs[sid]).resolve()
        n = RANGES[sid][1]-RANGES[sid][0]
        v = next(x for x in probe(source)["streams"] if x["codec_type"] == "video")
        if (int(v["nb_read_frames"]) != RANGES[sid][2] or v["width"] != width
                or v["height"] != height or v["avg_frame_rate"] != "24/1"
                or v["r_frame_rate"] != "24/1"):
            raise ValueError(f"{sid}: incorrect preconformed input; assembler must not retime")
        if any(s["codec_type"] == "audio" for s in probe(source)["streams"]):
            raise ValueError(f"{sid}: source audio must be removed before acceptance")
        target = work/f"{sid}.mkv"
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(source), "-an", "-vf",
               f"trim=start_frame=0:end_frame={n},setpts=N/(24*TB)",
               "-c:v", "ffv1", "-level", "3", "-pix_fmt", "yuv444p",
               "-color_primaries", "bt709", "-color_trc", "bt709",
               "-colorspace", "bt709", "-color_range", "tv", str(target)]
        run(cmd); commands.append(cmd); masters.append(target)
    white = work/"white.mkv"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
           f"color=white:s={width}x{height}:r=24", "-frames:v", "12",
           "-c:v", "ffv1", "-level", "3", "-pix_fmt", "yuv444p",
           "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", "-color_range", "tv", str(white)]
    run(cmd); commands.append(cmd); masters.append(white)
    concat = work/"concat.txt"
    # Escape concat-demuxer filenames, including ordinary apostrophes.
    concat.write_text("".join("file '"+str(p).replace("'", "'\\''")+"'\n" for p in masters))
    master = output.with_suffix(".master.mkv")
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
           "-i", str(concat), "-i", str(pcm), "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "copy", "-c:a", "pcm_s24le", str(master)]
    run(cmd); commands.append(cmd)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(master), "-map", "0:v:0",
           "-map", "0:a:0", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
           "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "320k",
           "-ar", "48000", "-movflags", "+faststart", str(output)]
    run(cmd); commands.append(cmd)
    versions = subprocess.check_output(["ffmpeg", "-version"], text=True)
    record = {
        "warning": "Mechanical build, not acceptance; inspect final export separately",
        "inputs": {sid: {"path": str(Path(p)), "sha256": digest(Path(p))} for sid,p in inputs.items()},
        "pcm": {"path": str(pcm), "sha256": digest(pcm)},
        "output": {"path": str(output), "sha256": digest(output)},
        "master": {"path": str(master), "sha256": digest(master)},
        "commands": commands, "ffmpeg_version": versions,
    }
    Path(manifest).write_text(json.dumps(record, indent=2)+"\n")
    return master


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", default="media/cuts/rough_v1.mp4")
    p.add_argument("--manifest", default="production/assembly/rough_v1.json")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    g = Gate(root)
    if not g.run("T16"):
        print("\n".join(g.errors), file=sys.stderr)
        return 1
    inputs = {s: g.path(g.assets["D_entry" if s=="D" else s]["path"]) for s in "ABCDEF"}
    for s in "ABCDEF":
        g.media_ok("D_entry" if s=="D" else s, RANGES[s][2])
    g.pcm_ok("audio_mix")
    if g.errors:
        print("\n".join(g.errors), file=sys.stderr); return 1
    output, manifest = g.path(args.output), g.path(args.manifest)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    assemble(inputs, output, g.path(g.assets["audio_mix"]["path"]), manifest, smoke=True)
    # Record portable commands/paths relative to repo; re-run from repo root.
    record = load(manifest)
    text = json.dumps(record, indent=2).replace(str(root)+"/", "")
    manifest.write_text(text+"\n")
    print("Built candidate rough master, not accepted:", output)
    return 0

if __name__ == "__main__":
    sys.exit(main())