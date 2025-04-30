import os
import subprocess
import time

def process_video(video_folder, video_file):
    video_path = os.path.join(video_folder, video_file)
    print(f"Processing file: {video_file}")
    
    # Define the command for processing the video
    command = f'auto-editor "{video_path}"'

    # Execute the command and display output in real-time
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read and print stdout line by line
        for line in iter(process.stdout.readline, ''):
            print(f"[{video_file}] {line.strip()}")
        
        # Read and print stderr line by line
        for line in iter(process.stderr.readline, ''):
            print(f"[{video_file}] {line.strip()}")

        # Wait for the process to complete
        process.wait()

    except subprocess.CalledProcessError as e:
        print(f"Command execution failed for file {video_file}: {e}")

def delete_original_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted original file: {file_path}")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def main():
    # Get the current working directory
    video_folder = os.getcwd()

    # Get a list of all video files in the folder
    video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]

    # Filter out files that have already been altered and Python scripts
    video_files = [f for f in video_files if "_ALTERED" not in f and not f.endswith('.py')]

    # Record the start time
    start_time = time.time()

    for video_file in video_files:
        try:
            process_video(video_folder, video_file)
            print(f"Completed processing file: {video_file}")
        except Exception as exc:
            print(f"Exception occurred while processing file {video_file}: {exc}")

    # Delete all original files after processing, excluding Python scripts
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        delete_original_file(video_path)

    # Record the end time
    end_time = time.time()

    # Calculate and print the total time taken
    total_time = end_time - start_time
    print(f"All videos have been edited successfully in {total_time:.2f} seconds.")

if __name__ == '__main__':
    main()

