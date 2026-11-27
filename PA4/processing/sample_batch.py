from pathlib import Path
import random
import shutil

# Source folder containing all extracted frames and destination for Batch 1
src = Path("extracted_frames")
dst = Path("roboflow_batch1")
dst.mkdir(exist_ok=True)

# Separate candidate detection frames (potholes + false positives) from clean road frames
det = sorted(src.glob("*_det.jpg")) # candidate potholes + false positives
bg = sorted(src.glob("*_bg.jpg")) # clean roads/cracks

# Fix the random seed so the sampled batch is repoducible if re-run
random.seed(42)

# Sample up to 250 detection frames and 100 background frames (350 total)
sample_det = random.sample(det, min(250, len(det)))
sample_bg = random.sample(bg, min(100, len(bg)))

# Copy (instead of move) so the full extracted_frames pool stays intact
for img in sample_det + sample_bg:
    shutil.copy2(img, dst / img.name)

print(f"Ready: {len(sample_det)} det + {len(sample_bg)} bg = {len(sample_det) + len(sample_bg)} images in {dst}")