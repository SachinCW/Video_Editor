import os
import subprocess
import time
import re

##################################################
### Function to convert time into Seconds
##################################################
def convert_time_to_seconds(time_str):
    """Convert HH:MM:SS format to seconds."""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


##################################################
### Function to format time 
##################################################
def format_time(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


##################################################
### Function to add water mark to Video
##################################################
def add_watermark(video_file):
    # Overlay position (top-left)
    x = "10"
    y = "10"

    # Font and watermark text
    logo_file = "../input/overlays/logo.png"
    font_file = "../input/Lobster.ttf"
    watermark_text = "Sachin Chandrashekhar"

    # Always use software encoding (libx264)
    video_encoder = "-c:v libx264"

    out_filename = video_file.split('.')
    print(out_filename,len(out_filename))
    video_file_name = '..' + out_filename[-2] + "_watermark" + "." + out_filename[-1]

    ffmpeg_command = (
            f"ffmpeg -y -i \"{video_file}\" -i \"{logo_file}\" "
            f"-filter_complex \"[1:v]scale=150:-1[logo];[0:v][logo]overlay=x={x}:y={y},"
            f"drawtext=fontfile='{font_file}':text='{watermark_text}':"
            f"fontcolor=white@1.0:fontsize=30:x=w-tw-10:y=h-th-10\" "
            f"{video_encoder} -pix_fmt yuv420p -c:a copy \"{video_file_name}\""
        )
    print(f"Add Watermark : Running Command:",ffmpeg_command)
    os.system(ffmpeg_command)

    #print(f"Running Command:", " ".join(command))  # Debugging statement to verify the command
    #subprocess.run(command, check=True)


##################################################
### Function to Extract Video from Main Video
##################################################
#def trim_video(input_path, output_path, start_time, duration):
def extract_video(input_path, output_path, start_time, duration):
    """
    Extract video from start_time for the specified duration and save to output_path using FFmpeg.
    Optimized for speed by copying streams without re-encoding.
    """
    command = [
        'ffmpeg',
        '-async', '-1',
        '-ss', start_time,     # Fast seek before loading input
        '-i', input_path,      # Input file
        '-t', duration,        # Duration of the clip
        '-c:v', 'copy',        # Copy video stream without re-encoding
        '-c:a', 'copy',        # Copy audio stream without re-encoding
        '-threads', '0',       # Use all available CPU threads
        '-y',                  # Overwrite output file if it exists
        output_path
    ]
    
    print(f"Trim Video : Running Command:", " ".join(command))  # Debugging statement to verify the command
    subprocess.run(command, check=True)



##################################################
### START OF MAIN EXECUTION
##################################################
if __name__ == "__main__":
    # Start timing
    start_time_process = time.time()

    # Take user input instead of command-line arguments
    while True:
        try:
            input_video_file = input("Enter Video file for Extraction : ").strip()
            if (os.path.exists(input_video_file)):
                break
            else:
                print(f"Error! Enter valid Input video file for extraction")
        except:
            print(f"Error! Not a video input file.")

    output_dir = input("Enter output directory to store extracted videos : ").strip()
    os.makedirs(output_dir,exist_ok=True)

    while True:
        try:
            input_loop = int(input("Enter number of extractions required from this video : "))
            break
        except:
            print(f"Error! Not a valid option! Enter number..")

    extraction_dict = {}
    input_timer_regex = r'[0-9][0-9]+\:[0-9][0-9]+\:[0-9][0-9]'

    ## Looping to take user inputs for video timers
    for i in range(input_loop):
        print(f" Enter Inputs for Timer slot: {i+1}")
        ## Read User input until user enter timer in proper format - StartTime
        while True:
            start_time_input = input("Enter start time (HH:MM:SS): ").strip()
            if (re.match(input_timer_regex,start_time_input)):

                ## Handling when filename is passed with relative directory ../input/video/01.mp4
                input_filenames = input_video_file.split('.')
                output_file = input_filenames[-2].split('/')
                output_filename = output_dir + "/" + output_file[-1] + "_" + str(int(i+1)) + "." + input_filenames[-1]
                break
            else:
                print(f" Error! InValid start time..")

         ## Read User input until user enter timer in proper format - EndTime
        while True :
            end_time_input = input("Enter end time (HH:MM:SS): ").strip()
            if (re.match(input_timer_regex,end_time_input)):
                # Calculate the duration between start_time and end_time
                start_time_seconds = convert_time_to_seconds(start_time_input)
                end_time_seconds = convert_time_to_seconds(end_time_input)
                duration_seconds = end_time_seconds - start_time_seconds

                #print(f" {start_time_seconds} - {end_time_seconds} - {duration_seconds}") 
       
                if duration_seconds > 0:
                    duration = format_time(duration_seconds)

                    ## Building dictionary to hold the values
                    extraction_dict[i]={}
                    extraction_dict[i]['start_time'] = start_time_input
                    extraction_dict[i]['duration'] = duration
                    extraction_dict[i]['output_file'] = output_filename
                    break
                else:
                    print(f"Error! Enter proper end time to extract the video!")
            else:
                print(f" Error! InValid end time..")

#print_dictionary(extraction_dict)
print(extraction_dict)

for key in extraction_dict:
    #print(f" {key}-> {extraction_dict[key]}")
    extract_video(input_video_file,extraction_dict[key]['output_file'],extraction_dict[key]['start_time'],extraction_dict[key]['duration'])
    add_watermark(extraction_dict[key]['output_file'])
    
    # End timing and print the time taken
    end_time_process = time.time()
    time_taken = end_time_process - start_time_process

    formatted_time = format_time(time_taken)
    print(f"Time taken for the process: {formatted_time}")
    time.sleep(2)
