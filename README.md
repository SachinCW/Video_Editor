### Install the package by running the command
pip3 install pyffmpeg 

ffmpeg will be installed in user directory at .pyffmpeg/bin/ffmpeg

Verify by running the command <br>
ls -ltr $HOME/.pyffmpeg/bin/ffmpeg <br>

### Execute script 
python3 add_watermark.py
025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - FFmpeg Initialising<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - Save directory: .<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - Checking GitHub Activeness: True<br>
2025-05-01 12:39:52,768 - pyffmpeg.misc.Paths - INFO - bin folder: /Users/rajesh/.pyffmpeg/bin<br>
2025-05-01 12:39:52,768 - pyffmpeg.misc.Paths - INFO - Inside load_ffmpeg_bin<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - FFmpeg file: /Users/rajesh/.pyffmpeg/bin/ffmpeg<br>
 Enter video (full path) : ../input/Spark_Course_Intro.mp4<br>
 Enter logo (full path) : ../input/RADE.png<br>
 Enter the location choice (top,right,bottom,center) :top<br>

This will generate file in output directory.
