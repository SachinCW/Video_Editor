from pyffmpeg import FFmpeg
import os
import glob
import time
import platform

ff = FFmpeg()

# Paths
base_dir = '/Users/sachin/Data/G/Data Engineering Hub/Automation/Video Editors/Video_Editor'
input_dir = os.path.join(base_dir, 'input')
overlay_dir = os.path.join(input_dir, 'overlays')
output_dir = os.path.join(base_dir, 'output')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Overlay position (top-left)
x = "10"
y = "10"

# Font and watermark text
font_file = os.path.join(input_dir, 'Lobster.ttf')
watermark_text = "Sachin Chandrashekhar"

# Get all .mp4 videos and overlay images
video_files = glob.glob(os.path.join(input_dir, "*.mp4"))
overlay_files = glob.glob(os.path.join(overlay_dir, "*.*"))

# Always use software encoding (libx264)
video_encoder = "-c:v libx264"

# Total combinations to process
total_tasks = len(video_files) * len(overlay_files)
task_count = 0

# Start the timer
start_time = time.time()

# Process each video with each overlay
for video_path in video_files:
    video_name = os.path.basename(video_path)
    video_basename, _ = os.path.splitext(video_name)

    for overlay_path in overlay_files:
        task_count += 1
        remaining = total_tasks - task_count

        overlay_name = os.path.splitext(os.path.basename(overlay_path))[0]
        output_filename = f"{video_basename}_{overlay_name}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        print(f"\n🟡 [{task_count}/{total_tasks}] Processing:")
        print(f"     🎥 Video  : {video_name}")
        print(f"     🖼️  Overlay: {overlay_name}")
        print(f"     📦 Output : {output_filename}")
        print(f"     ⏳ Videos left to process: {remaining}")

        # FFmpeg command with auto-overwrite (-y) and software encoding
        ffmpeg_command = (
            f"$HOME/.pyffmpeg/bin/ffmpeg -y -i \"{video_path}\" -i \"{overlay_path}\" "
            f"-filter_complex \"[1:v]scale=150:-1[logo];[0:v][logo]overlay=x={x}:y={y},"
            f"drawtext=fontfile='{font_file}':text='{watermark_text}':"
            f"fontcolor=white@1.0:fontsize=30:x=w-tw-10:y=h-th-10\" "
            f"{video_encoder} -pix_fmt yuv420p -c:a copy \"{output_path}\""
        )

        os.system(ffmpeg_command)
        print(f"✅ Done: {output_filename}")

# End the timer and calculate total time
end_time = time.time()
elapsed = end_time - start_time
mins, secs = divmod(int(elapsed), 60)

# Print total time taken
print(f"\n🎉 All videos processed in {mins} min {secs} sec ({elapsed:.2f} seconds).")
