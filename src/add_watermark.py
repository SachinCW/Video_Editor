from pyffmpeg import FFmpeg
import os
ff = FFmpeg()

video_path = input(f" Enter video (full path) : ")
logo_path = input(f" Enter logo (full path) : ")
location_choice = input(f" Enter the location choice (top,right,bottom,center) :")

outputdir = "../output"
print(f"----> {outputdir}")
# Ensure output directory exists
os.makedirs(outputdir, exist_ok=True)

output_filename =  os.path.basename(video_path)
output  = outputdir + "/" + output_filename 

if location_choice == "top":
    x="10"
    y="10"
elif location_choice == "right":
    x="main_w-overlay_w-10"
    y="(main_h-overlay_h)/2"
elif location_choice == "bottom":
    x="(main_w-overlay_w)/2"
    y="main_h-overlay_h)-10"
elif location_choice == "center":
    x="(main_w-overlay_w)/2"
    y="(main_h-overlay_h)/2"
else:
    print(f" Invalid location provided! Exiting...")
    exit(0)

text_x="main_w-overlay_w-10"
text_y="(main_h-overlay_h)/2"
#ff.options("-i {video_path} -i {logo_path} -filter_complex overlay={x}:{y} output.mp4")

#ffmepeg_command = f"$HOME/.pyffmpeg/bin/ffmpeg  -i {video_path} -i {logo_path} -filter_complex \"[0:v][1:v]overlay=x={x}:y={y}\"  -pix_fmt yuv420p -c:a copy {output}"
ffmepeg_command = f"$HOME/.pyffmpeg/bin/ffmpeg  -i {video_path} -i {logo_path} -filter_complex \"[0:v][1:v]overlay=x={x}:y={y},drawtext=fontfile=../input/Lobster.ttf:text='Sachin Chandrashekhar':fontcolor=white@1.0:fontsize=30:y=h-35:x=w-350'\"  -pix_fmt yuv420p -c:a copy {output}"
os.system(ffmepeg_command)
print(f" Updated the Video : {video_path} with logo : {logo_path}! New vedio : {output}")
