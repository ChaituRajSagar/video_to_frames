import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    """
    Extracts frames from a video and saves them as image files locally.

    Args:
        video_path (str): The path to the input video file.
        output_folder (str): The directory where the extracted frames will be saved.
        frame_rate (int): The number of frames to skip between captures.
                          A frame_rate of 1 means every frame is captured.
                          A frame_rate of 30 means 1 frame per second (if video is 30fps).
    Returns:
        bool: True if frames were extracted successfully, False otherwise.
    """

    # Ensure the output folder exists. Create it if it doesn't.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}. Skipping.")
        return False

    frame_count = 0
    saved_frame_count = 0
    
    # Get the original frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Processing '{os.path.basename(video_path)}':")
    print(f"  Resolution: {video_width}x{video_height}, FPS: {fps:.2f}, Total Frames: {total_frames}")

    # Calculate the frame skip based on the desired frame_rate
    frames_to_skip = round(fps / frame_rate) if frame_rate > 0 else 1
    if frames_to_skip < 1:
        frames_to_skip = 1

    print(f"  Extracting frames at approximately {frame_rate} frames per second (skipping {frames_to_skip - 1} frames).")

    while True:
        ret, frame = cap.read()

        if not ret:
            break  # End of video

        if frame_count % frames_to_skip == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    print(f"  Finished processing '{os.path.basename(video_path)}'.")
    print(f"  Total frames processed: {frame_count}")
    print(f"  Total frames saved: {saved_frame_count}\n")
    return True

if __name__ == "__main__":
    # --- Configuration ---
    # Read configuration from .env file
    video_source_directory = os.getenv("VIDEO_SOURCE_DIR")
    output_base_directory = os.getenv("OUTPUT_BASE_DIR")
    
    # Convert DESIRED_FRAME_RATE to integer, default to 1 if not set or invalid
    try:
        desired_frame_rate_str = os.getenv("DESIRED_FRAME_RATE")
        desired_frame_rate = int(desired_frame_rate_str) if desired_frame_rate_str else 1
    except ValueError:
        print("Warning: DESIRED_FRAME_RATE in .env is not an integer. Defaulting to 1.")
        desired_frame_rate = 1

    # Add error checking for paths (important when reading from .env)
    if not video_source_directory:
        print("Error: VIDEO_SOURCE_DIR not found in .env. Please set it.")
        exit()
    if not output_base_directory:
        print("Error: OUTPUT_BASE_DIR not found in .env. Please set it.")
        exit()

    # List of common video file extensions to filter
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm')

    # Ensure the output base directory exists
    if not os.path.exists(output_base_directory):
        os.makedirs(output_base_directory)
        print(f"Created base output directory: {output_base_directory}")

    # --- Dummy video creation for testing (optional) ---
    # This block now uses a hardcoded path for the dummy video if needed,
    # as the source_directory is for existing videos.
    dummy_video_path = os.path.join(video_source_directory, "dummy_input_video.mp4")
    if not os.path.exists(dummy_video_path):
        print(f"Creating a dummy video file '{dummy_video_path}' for demonstration purposes...")
        try:
            from moviepy.editor import ColorClip, concatenate_videoclips
            clip1 = ColorClip((640, 480), color=(255, 0, 0), duration=1) # Red for 1 second
            clip2 = ColorClip((640, 480), color=(0, 255, 0), duration=1) # Green for 1 second
            clip3 = ColorClip((640, 480), color=(0, 0, 255), duration=1) # Blue for 1 second
            final_clip = concatenate_videoclips([clip1, clip2, clip3], method="compose")
            final_clip.write_videofile(dummy_video_path, fps=24) # Write at 24 fps
            print(f"Dummy video '{dummy_video_path}' created successfully.")
        except ImportError:
            print("Warning: moviepy not installed. Cannot create dummy video. Please provide your own videos in the source directory.")
            print("To install moviepy: pip install moviepy")
            # exit() # Don't exit here, just skip dummy creation if moviepy is missing
        except Exception as e:
            print(f"Error creating dummy video: {e}")
            # exit() # Don't exit here, just skip dummy creation if error occurs
    
    # --- Process all videos in the source directory ---
    print(f"Scanning videos in: {video_source_directory}\n")

    processed_count = 0
    skipped_count = 0

    if not os.path.isdir(video_source_directory):
        print(f"Error: Video source directory '{video_source_directory}' does not exist or is not a directory. Please check your .env file.")
        exit()

    for filename in os.listdir(video_source_directory):
        if filename.lower().endswith(video_extensions):
            video_full_path = os.path.join(video_source_directory, filename)
            
            # Create a unique output subfolder for each video
            video_name_without_ext = os.path.splitext(filename)[0]
            current_video_output_folder = os.path.join(output_base_directory, video_name_without_ext)

            print(f"Found video: {filename}")
            if extract_frames(video_full_path, current_video_output_folder, frame_rate=desired_frame_rate):
                processed_count += 1
            else:
                skipped_count += 1
        else:
            print(f"Skipping non-video file: {filename}")

    print("\n--- Summary ---")
    print(f"Total videos processed: {processed_count}")
    print(f"Total files skipped (non-video or error): {skipped_count}")
    print(f"All extracted frames are located in subfolders within: {os.path.abspath(output_base_directory)}")
