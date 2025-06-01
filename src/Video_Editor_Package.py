import os
import subprocess
import time
import re
from PIL import Image, ImageDraw, ImageFont

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
        #'-async', '-2',        ## To Sync audio lagging with video, Issue is limited to extraction from 2nd video only
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
### Function to add water mark to Video
##################################################
def add_watermark(output_dir,video_file):
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
    ext = out_filename[-1]
    out_filename = out_filename[-2].split('/')
    video_file_name = output_dir + "/"  + out_filename[-1] + "_watermark" + "." + ext
    #print(f"--- Video file :", video_file_name)

    ffmpeg_command = (
            f"ffmpeg -y -i \"{video_file}\" -i \"{logo_file}\" "
            f"-filter_complex \"[1:v]scale=150:-1[logo];[0:v][logo]overlay=x={x}:y={y},"
            f"drawtext=fontfile='{font_file}':text='{watermark_text}':"
            f"fontcolor=white@1.0:fontsize=30:x=w-tw-10:y=h-th-10\" "
            f"{video_encoder} -pix_fmt yuv420p -c:a copy \"{video_file_name}\""
        )
    print(f"Add Watermark : Running Command:",ffmpeg_command)
    os.system(ffmpeg_command)


##################################################
### Function to draw Thumbnail Text 
##################################################
def draw_text(draw, text, position, font, max_width, line_spacing):
    # Initialize variables
    lines = []
    words = text.split()

    # Word wrapping
    while words:
        line = ''
        while words and draw.textbbox((position[0], 0), line + words[0], font=font)[2] <= max_width:
            line = line + (words.pop(0) + ' ')
        lines.append(line)

    # Calculate line height for spacing
    line_height = draw.textbbox((position[0], position[1]), 'A', font=font)[3] - draw.textbbox((position[0], position[1]), 'A', font=font)[1]

    # Draw lines on image with consistent line spacing
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill="#dddddd")  # Updated text color to #dddddd
        y += line_height + line_spacing  # Apply consistent spacing


####################################################
### Function to create Thumbnail image  
####################################################
def create_thumbnail(video_file,thumbnail_text=''):

    ## Image details to use
    thumbnail_base_image = "../input/thumbnail/base_thumbnail.png"
    font_file = "/Library/Fonts/Arial Bold.ttf"
    #font_file = "../input/Lobster.ttf"

    out_filename = video_file.split('.')
    ext = out_filename[-1]
    out_filename = out_filename[-2].split('/')
    thumbnail_image_file = output_dir + "/"  + out_filename[-1] +  ".jpg" 

    if (thumbnail_text == ''):
        thumbnail_text = str(out_filename[-1])

    #print(f"--- Thumbnail file :", thumbnail_image_file, ", thumbnail_text:" , thumbnail_text)

    # Open the image
    img = Image.open(thumbnail_base_image).convert("RGB")  # Convert to RGB to remove alpha channel

    # Get a font (Arial Bold)
    font_size = 60  # Adjust font size as needed
    font = ImageFont.truetype(font_file, font_size)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Define text position, maximum width, and line spacing
    text_position_x = 100  # Adjust horizontal position as needed
    text_position_y = int(img.height * 0.18)  # Start printing 15% below the top of the image
    max_width = img.width - text_position_x - 50  # Adjust max width as needed
    line_spacing = 50  # Adjust line spacing as needed

    # Add text to image with word wrapping
    draw_text(draw, thumbnail_text, (text_position_x, text_position_y), font, max_width, line_spacing)

    # Save the image
    img.save(thumbnail_image_file, "JPEG")

    return(thumbnail_image_file)


####################################################
### Function to convert Thumbnail Image to Video
####################################################
def convert_thumbnail_image_to_video(output_dir,thumbnail_image):
    video_file = thumbnail_image.split('.')
    #print(f"--- 1 ---",video_file)
    video_file = video_file[-2].split('/')
    #print(f"--- 2 ---",video_file)
    video_file_1 = output_dir + "/" + video_file[-1] + "_tmp.mp4"
    video_file_2 = output_dir + "/" + video_file[-1] + ".mp4"

    ## Below command without audio is causing problem while merging final one that is having video & audio
    #ffmpeg_command = f"ffmpeg -loop 1 -y -i {thumbnail_image}  -shortest -t 2 {video_file_1}"
    # Below command fixes when merged 
    ffmpeg_command = f"ffmpeg -loop 1 -y -i {thumbnail_image} -i ../input/thumbnail/stopwatch-sounds-269019.mp3 -shortest -t 2 {video_file_1}"
    print(f"Creating Thumbnail Video from Image : Running Command:",ffmpeg_command)
    os.system(ffmpeg_command)

    ## Rescaling the video with the size of actual tutorial vidoes (using higher resolution of Mac M1)
    ffmpeg_command = f"ffmpeg -y -i {video_file_1} -vf scale=1920:950,setsar=1 -vcodec h264 {video_file_2}"
    print(f"Recreating Thumbnail Video with proper scaling : Running Command:",ffmpeg_command)
    os.system(ffmpeg_command)

    ## Removing temp file
    os.remove(video_file_1)


####################################################
### Function to combine Thumbnail & Watermark Video
####################################################
def combine_thumbnail_watermark_videos(thumbnail_video,watermark_video,output_dir,filename):
    #print(f" ---- 1 -----", thumbnail_video, "--",watermark_video)
    #print(f" -----2 -----", output_dir, "--", filename)
    output_dir_abs = os.path.abspath(output_dir)
    ts1 = output_dir_abs + "/" + filename + "_1.ts"
    ts2 = output_dir_abs + "/" + filename + "_2.ts"
    ffmpeg_thumbnail_ts = f"ffmpeg -i {thumbnail_video} -c copy {ts1}"
    print("Processing command 1: ", ffmpeg_thumbnail_ts)
    os.system(ffmpeg_thumbnail_ts)

    ffmpeg_video_ts = f"ffmpeg -i {watermark_video} -c copy {ts2}"
    print("Processing command 2: ", ffmpeg_video_ts)
    os.system(ffmpeg_video_ts)

    ffmpeg_final_video_file = output_dir_abs + "/" + filename + "_final.mp4"
    ffmpeg_final_video = f"ffmpeg -i \"concat:{ts1}|{ts2}\" -c copy \"{ffmpeg_final_video_file}\""
    print("Processing command 3: ", ffmpeg_final_video)
    os.system(ffmpeg_final_video)
    os.remove(ts1)
    os.remove(ts2)



####################################################
### START OF MAIN EXECUTION
####################################################
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
        thumbmail_input = input("Enter Thumbnail header message: ").strip()
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
                    extraction_dict[i]['thumbnail_header'] = thumbmail_input
                    extraction_dict[i]['start_time'] = start_time_input
                    extraction_dict[i]['duration'] = duration
                    extraction_dict[i]['output_file'] = output_filename
                    break
                else:
                    print(f"Error! Enter proper end time to extract the video!")
            else:
                print(f" Error! InValid end time..")
    #print_dictionary(extraction_dict)
    #print(extraction_dict)
    
    if( len(extraction_dict) > 0) :
        for key in extraction_dict:
            #print(f" {key}-> {extraction_dict[key]}")

            ## Calling function to extract video
            extract_video(input_video_file,extraction_dict[key]['output_file'],extraction_dict[key]['start_time'],extraction_dict[key]['duration'])

            ## Calling function to add water mark
            add_watermark(output_dir,extraction_dict[key]['output_file'])
    
            ## Deleting the extracted file after creating new video with watermark
            os.remove(extraction_dict[key]['output_file'])

            ## Creating Thumbnail for the Video 
            thumbnail_image_file=create_thumbnail(extraction_dict[key]['output_file'],extraction_dict[key]['thumbnail_header'])
            print(f" Thumbnail Image: ", thumbnail_image_file)

            convert_thumbnail_image_to_video(output_dir,thumbnail_image_file)

            thumbnail_dir =  thumbnail_image_file.split('/')[-1] 
            thumbnail_video =  output_dir + "/" + thumbnail_dir.split('.')[-2] + ".mp4"
            watermark_video =  output_dir + "/" + thumbnail_dir.split('.')[-2] + "_watermark.mp4"
            combine_thumbnail_watermark_videos(thumbnail_video, watermark_video,output_dir,thumbnail_dir.split('.')[-2])

            os.remove(thumbnail_image_file)
            os.remove(thumbnail_video)
            os.remove(watermark_video)

            # End timing and print the time taken
            end_time_process = time.time()
            time_taken = end_time_process - start_time_process

            formatted_time = format_time(time_taken)
            print(f"Time taken for the process: {formatted_time}")
            time.sleep(2)
    else:
        add_watermark(output_dir,input_video_file)
        thumbnail_image_file=create_thumbnail(input_video_file)
        convert_thumbnail_image_to_video(output_dir,thumbnail_image_file)
            
        thumbnail_dir =  thumbnail_image_file.split('/')[-1] 
        thumbnail_video =  output_dir + "/" + thumbnail_dir.split('.')[-2] + ".mp4"
        watermark_video =  output_dir + "/" + thumbnail_dir.split('.')[-2] + "_watermark.mp4"
            
        combine_thumbnail_watermark_videos(thumbnail_video, watermark_video,output_dir,thumbnail_dir.split('.')[-2])
        os.remove(thumbnail_image_file)
        os.remove(thumbnail_video)
        os.remove(watermark_video)
