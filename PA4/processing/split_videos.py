from pathlib import Path
import random
import shutil

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv"}

src_dir = Path(".")
train_dir = Path("train_videos")
test_dir = Path("test_videos")

train_dir.mkdir(exist_ok=True)
test_dir.mkdir(exist_ok=True)

videos = [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS]

random.seed(42)  # Keeps the split reproducible
random.shuffle(videos)

test_videos = videos[:9]
train_videos = videos[9:]

for v in test_videos:
    shutil.move(str(v), test_dir / v.name)

for v in train_videos:
    shutil.move(str(v), train_dir / v.name)

print(f"Moved {len(train_videos)} videos to {train_dir}/ and {len(test_videos)} videos to {test_dir}/")