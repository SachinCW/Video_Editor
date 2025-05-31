import os
import subprocess
import time

import logging
import logging.handlers

import re

##################################################
### Function to define and enable Logging
##################################################
def enable_logging(logFile,logLevel):
   logsize = 100*1000000
   logger = logging.getLogger("")
   logger.setLevel(logLevel)
   logging.basicConfig(filename=logFile, 
        style="{",  
        format=f"{asctime} - {levelname} - {module}:{funcName} - {message} ", 
        datefmt="%d-%m-%Y %H:%M:%S", 
        filemode="a")

   ## Setting logFile rotation on reaching its defined size of 100 MB
   handler=logging.handlers.RotatingFileHandler(logFile, mode='a',maxBytes=logsize, backupCount=20)


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
    
    logging.info("Running Command :".join(command))  # Debugging statement to verify the command
    print(f"Running Command:", " ".join(command))  # Debugging statement to verify the command
    subprocess.run(command, check=True)



def find_first_video_file(directory):
    """Find the first video file in the directory."""
    for file in os.listdir(directory):
        if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add more extensions if needed
            return os.path.join(directory, file)
    return None


def print_dictionary(dict):
    for key,value in dict.items():
        if isinstance(value,dict):
            print(f"Key:", key)
            print_dictionary(value)
        else:
            print(f"****",key,value)


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
    time.sleep(10)
    
#    # Get the current working directory
#    video_directory = os.getcwd()
#
#    # Find the first video file in the current directory
#    input_video = find_first_video_file(video_directory)
#
#    if input_video:
#        # Create an 'output' directory if it doesn't exist
#        output_directory = os.path.join(video_directory, "output")
#        os.makedirs(output_directory, exist_ok=True)
#
#        # Define the output path for the trimmed video
#        output_video = os.path.join(output_directory, f"{output_name_input}.mp4")
#
#        # Call the trim_video function
#        trim_video(input_video, output_video, start_time_input, duration)
#
#        print(f"Video trimmed successfully and saved as {output_video}")
#        print(f"Original video preserved: {input_video}")
#
#    else:
#        print("No video file found in the directory.")
#
#    # End timing and print the time taken
#    end_time_process = time.time()
#    time_taken = end_time_process - start_time_process
#
#    formatted_time = format_time(time_taken)
#    print(f"Time taken for the process: {formatted_time}")
