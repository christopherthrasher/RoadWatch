# RoadWatch Processing

Local video-processing pipeline, YOLO26n model weights, and Google Colab training setup for the **RoadWatch** pothole detection pipeline.

---

## 1. Files & Directory Status

RoadWatch/<br>
    &emsp;└─PA4/<br>
        &emsp;&emsp;&nbsp;&nbsp;└─processing/<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─Video-processing-per-frame-script/<br>
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;└─extract_frames.py -> Runs YOLO inference to extract *_det.jpg and *_bg.jpg frames<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─weights/<br>
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;└─best.pt -> Active trained YOLO26n weights<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─split_videos.py -> Splits raw road videos into train_videos/ and test_videos/<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─sample_batch.py -> Samples a reproducible subset (seed=42) into roboflow_batch1/(Not very useful for right now)<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─app.py -> Main backend entry point / API application<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─detector.py -> Core detection inference helper module<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─gps_sync.py -> Matches detection timestamps to GPS coordinates<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─post_processing.py -> Removes duplicates, saves images, and formats detection records<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─Dockerfile -> Container definition for packaging the processing/backend service<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─test_app.py -> Integration and test suite for backend API/pipeline components<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─test_gps_sync.py -> Unit tests for GPS synchronization<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─test_post_processing.py -> Unit tests for post-processing<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─RoadWatch_YOLO26_Baseline.ipynb -> Google Colab training notebook<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─README.md<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─requirements.txt -> Python package dependencies (ultralytics, opencv-python, etc.)<br>
            &emsp;&emsp;&emsp;&emsp;&nbsp;├─.gitignore<br>
~/Desktop/CV model videos<br>
├─train_videos<br>
└─test_videos<br>

## 2. Pipeline Overview & Model Iteration Log

- v1(Baseline) - Trained yolo26n.pt on Pothole-1 dataset on Google Colab with 0 background frames.
- v2(Hard Negatives) - Retrained on Pothole-1 dataset plus 258 train and 50 validation local background frames to suppress false positives such as puddles, curb reflectors, and shadows (Not very good results)
- v3 (Planned) - Will be training using v2 and labeled local potholes

## 3. End-to-End Workflow (In Order)

### Part 1: VSCode (Local Setup and Data Preparation)

Step 1: Install Python dependencies (recommended: virtual environment, or without a virtual environment)

Virtual Environment Setup:

```powershell
python3 -m venv .venv
source .venv/bin/activate # macOS/Linux
# .venv\Scripts\activate # Windows

# Next install with pip or pip3
pip install -r requirements.txt
```

Step 2: Keep Raw videos local and DO NOT upload to GitHub

Keep raw video files in a separate local directory outside of your Git repo or in Google Drive. Never commit raw videos, extracted frames, or video folders to GitHub.

Step 3: Split Raw videos into Train and Test

Run from: `RoadWatch/PA4/processing`

```powershell
python3 split_videos.py
```

(Ensure your raw video files are placed inside your new local working video folder and not inside the GitHub Repository).

Step 4: Extract Candidate & Background Frames

Run from: `RoadWatch/PA4/processing`

```powershell
python3 Video-processing-per-frame-script/extract_frames.py --weights weights/best.pt --input "Path/to/your/training_videos_folder" --output "Path/to/your/extracted_frames_trained_folder"
```

Make sure that the videos, training videos, extracted frames from training videos are in all in the same main folder. Something like all the videos in one folder, split training and testing videos in two different folders and extracted frames from training and testing videos in two different folders and all those folders are in one data folder or Google Drive or even hard drive, if necessary.

Step 5: Sample & Upload the Training Batch (not needed currently)

Run from: `RoadWatch/PA4/processing`

```powershell
python3 sample_batch.py
```

Compress the output file and upload to Google Drive or keep it in local data video folder.

### Part 2: Google Colab (Model Retraining)

Step 6: Connect Google Drive & Open the Notebook

- Open `RoadWatch_YOLO26_Baseline.ipynb` in Google Colab (File -> Open Notebook -> GitHub).
- Set the runtime to GPU (Runtime -> Change runtime type -> T4 GPU)
- API key for the dataset has been added as ROBOFLOW_API_KEY

Step 7: Run the Training Notebook

Run the cells in order:

- Cell 1: Install `ultralytics` and `roboflow` # For YOLO and dataset
- Cell 2: Downloads the `Pothole-1` dataset in `yolo26` format.
- Cell 3: Mounts /content/drive, unzips the roboflow_batch1.zip, splits 50 frames to `valid` and the rest to `train`, and writes empty `.txt` label files (Null/Background).
- Cell 4: Renames the class in `data.yaml` to `pothole` and trains `yolo26n.pt` for 50 epochs (imgsz=640).
- Cell 5: Downloads `best.pt`, weights.

### Part 3: VSCode (Update Weights and Verify)

Step 8: Replace the local weights

Move the newly downloaded `best.pt` into `PA4/processing/weights/best.pt`, overwriting the previous version, and commit to Git.

Step 9: Test Locally on Held-Out Test Videos

Run from: `RoadWatch/PA4/processing`

```powershell
python3 Video-processing-per-frame-script/extract_frames.py --weights weights/best.pt --input "Path/to/your/test_videos_folder" --output "Path/to/your/extracted_frames_test_folder"
```

## 4. GPS Synchronization and Post-Processing

### Components

- `gps_sync.py`: Loads RouteKeep Cam GPS CSV data and matches detection timestamps to GPS coordinates.
- `post_processing.py`: Synchronizes detections with GPS, reduces duplicate detections, saves representative images, and formats detection records for the backend.
- `test_gps_sync.py`: Unit tests for GPS synchronization.
- `test_post_processing.py`: Unit tests for post-processing.

### Unit Testing

Run the following commands from `RoadWatch/PA4/processing`:

```powershell
python -m unittest test_gps_sync -v
python -m unittest test_post_processing -v
```

All 16 unit tests passed (8 GPS synchronization tests and 8 post-processing tests).

### Integration Status

GPS synchronization and post-processing were successfully tested locally with PotholeDetector using a RouteKeep Cam video and its corresponding GPS CSV file. The test produced a formatted detection record and successfully saved its representative image. The detection was a false positive, but it allowed the processing workflow to be verified.

Duplicate removal currently uses a distance threshold of 5 meters and a time threshold of 2 seconds. These thresholds may be adjusted after further testing.

Integration through app.py, backend integration, shared file storage, Docker verification, and testing with actual pothole recordings remain to be completed.