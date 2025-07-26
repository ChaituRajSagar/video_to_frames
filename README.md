# Video Frame Extractor

This Python script uses OpenCV to extract frames from multiple video files located in a specified directory and saves them as individual image files into an organized output structure.

## Features

* **Batch Processing**: Extracts frames from all video files within a designated input folder.
* **Configurable Paths**: Input and output directories are easily configured using a `.env` file.
* **Customizable Frame Rate**: Control the density of extracted frames (e.g., 1 frame per second, or every frame).
* **Organized Output**: Creates a dedicated subfolder for each video within the output directory to keep extracted frames neatly separated.
* **Dummy Video Creation**: Includes an optional feature to create a small dummy video for testing if no videos are found in the source directory (requires `moviepy`).

## Prerequisites

Before you begin, ensure you have Python installed (Python 3.6+ is recommended).

### 1. Create a Python Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage project dependencies.

```python

python -m venv venv

```

### 2. Activate the Virtual Environment

```python

Windows:

.\venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

```

(You'll see (venv) at the beginning of your terminal prompt, indicating the virtual environment is active.)

```python
(venv) C:\Users\root_folder\video_frame_extractor> python .\video_frame_extractor.py
```

### 3. Install Dependencies

Install the necessary Python libraries using pip:

```python

pip install -r requirements.txt
requirements.txt content:
opencv-python
python-dotenv
moviepy # Only required if you use the dummy video creation feature

```

### Setup and Configuration

#### 1. Project Structure

```python

Your project directory (video_frame_extractor) should be structured as follows:

video_frame_extractor/
├── .env                 <-- Environment variables (create this file)
├── .gitignore           <-- Git ignore rules (create this file)
├── video_frame_extractor.py <-- The main script (your Python code)
├── requirements.txt     <-- Python dependencies
├── venv/                <-- Python virtual environment (created by `python -m venv venv`)
├── frames/              <-- Output directory for extracted frames (created by script)
└── videos/              <-- Input directory for your video files (create this folder)

```

#### 2. Environment Variables

Create a file named .env in the root of your video_frame_extractor directory. This file will store your configuration paths.

.env content:
Code snippet
.env file for Video Frame Extractor

```python
# .env file for Video Frame Extractor

#   Path to the directory containing your source video files
# Use double backslashes (\\) or forward slashes (/) for Windows paths

VIDEO_SOURCE_DIR="C:\\Users\\your_folder_where_videos_stored\\videos"

# Base directory where extracted frames will be stored (subfolders created per video)
# Use double backslashes (\\) or forward slashes (/) for Windows paths
OUTPUT_BASE_DIR="C:\\Users\\your_folder_where_videos_stores_frames\\frames"

# Desired frame rate for extraction (e.g., 1 for 1 frame per second)
Set to 0 or leave empty to extract all frames

DESIRED_FRAME_RATE=0
# Important: Replace the example paths with the actual paths on your system.
```

#### 3. Place Your Videos

Put your video files (e.g., .mp4, .avi, .mov) into the directory specified by VIDEO_SOURCE_DIR in your .env file. Based on the example, this is: C:\Users\your_folder_where_videos_stored\videos

How to Run the Script:

Activate your virtual environment (if you haven't already):

```python

Windows: .\venv\Scripts\activate
```

```python
macOS/Linux: source venv/bin/activate
```

```python
Navigate to the project's root directory in your terminal:

cd "C:\Users\your_root_folder\video_frame_extractor"

```

```python
Run the script:

(venv) C:\Users\root_folder\video_frame_extractor> python video_frame_extractor.py

```

The script will print progress messages to the console, indicating which videos are being processed and where their frames are being saved.

#### Output Structure

After execution, your OUTPUT_BASE_DIR (e.g., C:\Users\your_folder_where_videos_stores_frames\frames) will contain subfolders, one for each processed video:

```

frames/
├── video_file_1_name/
│   ├── frame_000000.jpg
│   ├── frame_000001.jpg
│   └── ...
└── video_file_2_name/
    ├── frame_000000.jpg
    ├── frame_000001.jpg
    └── ...

    ```