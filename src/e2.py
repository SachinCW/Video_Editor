import os
import subprocess
import time


def convert_time_to_seconds(time_str):
    """Convert HH:MM:SS format to seconds."""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def format_time(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def trim_video(input_path, output_path, start_time, duration):
    """
    Trim video from start_time for the specified duration and save to output_path using FFmpeg.
    Optimized for speed by copying streams without re-encoding.
    """
    command = [
        'ffmpeg',
        '-ss', start_time,     # Fast seek before loading input
        '-i', input_path,      # Input file
        '-t', duration,        # Duration of the clip
        '-c:v', 'copy',        # Copy video stream without re-encoding
        '-c:a', 'copy',        # Copy audio stream without re-encoding
        '-threads', '0',       # Use all available CPU threads
        '-y',                  # Overwrite output file if it exists
        output_path
    ]
    
    print("Running command:", " ".join(command))  # Debugging statement to verify the command
    subprocess.run(command, check=True)


def find_first_video_file(directory):
    """Find the first video file in the directory."""
    for file in os.listdir(directory):
        if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add more extensions if needed
            return os.path.join(directory, file)
    return None


if __name__ == "__main__":
    # Start timing
    start_time_process = time.time()

    # Take user input instead of command-line arguments
    start_time_input = input("Enter start time (HH:MM:SS): ").strip()
    end_time_input = input("Enter end time (HH:MM:SS): ").strip()
    output_name_input = input("Enter output filename (without extension): ").strip()

    # Calculate the duration between start_time and end_time
    start_time_seconds = convert_time_to_seconds(start_time_input)
    end_time_seconds = convert_time_to_seconds(end_time_input)
    duration_seconds = end_time_seconds - start_time_seconds

    if duration_seconds <= 0:
        print("Error: End time must be greater than start time.")
        exit(1)

    duration = format_time(duration_seconds)

    # Get the current working directory
    video_directory = os.getcwd()

    # Find the first video file in the current directory
    input_video = find_first_video_file(video_directory)

    if input_video:
        # Create an 'output' directory if it doesn't exist
        output_directory = os.path.join(video_directory, "output")
        os.makedirs(output_directory, exist_ok=True)

        # Define the output path for the trimmed video
        output_video = os.path.join(output_directory, f"{output_name_input}.mp4")

        # Call the trim_video function
        trim_video(input_video, output_video, start_time_input, duration)

        print(f"Video trimmed successfully and saved as {output_video}")
        print(f"Original video preserved: {input_video}")

    else:
        print("No video file found in the directory.")

    # End timing and print the time taken
    end_time_process = time.time()
    time_taken = end_time_process - start_time_process

    formatted_time = format_time(time_taken)
    print(f"Time taken for the process: {formatted_time}")
