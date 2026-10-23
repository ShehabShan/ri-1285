import array
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from assemble import assemble
from validate import probe, RANGES

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"requires ffmpeg")
class AssemblyTest(unittest.TestCase):
    def test_exact_endpoint_ownership_and_audio(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);inputs={}
            # Endpoints distinguishable from earlier frames: testing predecessor-tail
            # discard rather than next-head loss. B head green, tail white; C head blue.
            colors={"A":"red","B":"green","C":"blue","D":"yellow","E":"magenta","F":"cyan"}
            for sid,(_,_,count) in RANGES.items():
                path=root/f"{sid}.mkv"
                # Extra endpoint samples are white, never allowed into final visible ranges.
                vf=f"drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='eq(n,{count-1})'" if sid in "ABE" else "null"
                subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                    f"color={colors[sid]}:s=64x36:r=24","-vf",vf,
                    "-frames:v",str(count),"-c:v","ffv1","-pix_fmt","yuv444p",str(path)],check=True)
                inputs[sid]=path
            pcm=root/"mix.wav"
            samples=array.array("h")
            # Deterministic modest tone-like constant except exact silence.
            for i in range(1440000):
                value=0 if 1296000<=i<1320000 else 256
                samples.extend([value,value])
            if sys.byteorder!="little":samples.byteswap()
            with wave.open(str(pcm),"wb") as w:
                w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000);w.writeframes(samples.tobytes())
            out=root/"synthetic.mp4"
            master=assemble(inputs,out,pcm,root/"build.json",width=64,height=36,smoke=True)
            v=next(s for s in probe(out)["streams"] if s["codec_type"]=="video")
            self.assertEqual(int(v["nb_read_frames"]),720)
            self.assertEqual(v["avg_frame_rate"],"24/1")
            # Lossless master pixel samples identify ownership on both sides of every seam.
            raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(master),
                "-an","-pix_fmt","rgb24","-f","rawvideo","-"])
            stride=64*36*3
            def pixel(frame): return tuple(raw[frame*stride:frame*stride+3])
            for before,after in [(95,96),(215,216),(551,552),(431,432)]:
                self.assertNotEqual(pixel(before),pixel(after))
                self.assertNotEqual(pixel(before),(255,255,255))
            self.assertEqual(pixel(96),pixel(97)) # following first frame retained
            self.assertEqual(pixel(216),pixel(217))
            self.assertNotEqual(pixel(707),(255,255,255))
            self.assertTrue(all(pixel(i)==(255,255,255) for i in range(708,720)))
            with wave.open(str(pcm),"rb") as w:
                self.assertEqual(w.getnframes(),1440000)
            decoded=subprocess.check_output(["ffmpeg","-v","error","-i",str(master),
                "-vn","-f","s16le","-"])
            self.assertEqual(len(decoded),1440000*4)
            self.assertFalse(any(decoded[1296000*4:1320000*4]))
            # Wrong input samples must fail, not be padded/truncated automatically.
            bad=dict(inputs);bad["A"]=inputs["C"]
            with self.assertRaises(ValueError):
                assemble(bad,root/"bad.mp4",pcm,root/"bad.json",width=64,height=36,smoke=True)
