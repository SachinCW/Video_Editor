Install the package by running the command<br>
	pip3 install pyffmpeg<br>
<br>
<br>
ffmpeg will be installed in user directory at .pyffmpeg/bin/ffmpeg<br>
<br>
Verify by running the command <br>
	ls -ltr $HOME/.pyffmpeg/bin/ffmpeg<br>
<br>
Execute as shown below<br>
<br>
python3 add_watermark.py <br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - FFmpeg Initialising<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - Save directory: .<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - Checking GitHub Activeness: True<br>
2025-05-01 12:39:52,768 - pyffmpeg.misc.Paths - INFO - bin folder: /Users/rajesh/.pyffmpeg/bin<br>
2025-05-01 12:39:52,768 - pyffmpeg.misc.Paths - INFO - Inside load_ffmpeg_bin<br>
2025-05-01 12:39:52,768 - pyffmpeg.FFmpeg - INFO - FFmpeg file: /Users/rajesh/.pyffmpeg/bin/ffmpeg<br>
 Enter video (full path) : ../input/Spark_Course_Intro.mp4<br>
 Enter logo (full path) : ../input/RADE.png<br>
 Enter the location choice (top,right,bottom,center) :top<br>
----> ../output<br>
ffmpeg version N-108453-gb0c7352cd4-tessus Copyright (c) 2000-2022 the FFmpeg developers<br>
  built with Apple clang version 11.0.0 (clang-1100.0.33.17)<br>
  configuration: --cc=/usr/bin/clang --prefix=/opt/ffmpeg --extra-version=tessus --enable-avisynth --enable-fontconfig --enable-gpl --enable-libaom --enable-libass --enable-libbluray --enable-libdav1d --enable-libfreetype --enable-libgsm --enable-libmodplug --enable-libmp3lame --enable-libmysofa --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenh264 --enable-libopenjpeg --enable-libopus --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvmaf --enable-libvo-amrwbenc --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-version3 --pkg-config-flags=--static --disable-ffplay<br>
  libavutil      57. 38.100 / 57. 38.100<br>
  libavcodec     59. 49.100 / 59. 49.100<br>
  libavformat    59. 33.100 / 59. 33.100<br>
  libavdevice    59.  8.101 / 59.  8.101<br>
  libavfilter     8. 49.100 /  8. 49.100<br>
  libswscale      6.  8.112 /  6.  8.112<br>
  libswresample   4.  9.100 /  4.  9.100<br>
  libpostproc    56.  7.100 / 56.  7.100<br>
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '../input/Spark_Course_Intro.mp4':<br>
  Metadata:<br>
    major_brand     : isom<br>
    minor_version   : 512<br>
    compatible_brands: isomiso2avc1mp41<br>
    encoder         : Lavf61.1.100<br>
  Duration: 00:00:29.00, start: 0.000000, bitrate: 1520 kb/s<br>
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1280x720, 1414 kb/s, 25.03 fps, 25 tbr, 12800 tbn (default)<br>
    Metadata:<br>
      handler_name    : VideoHandler<br>
      vendor_id       : [0][0][0][0]<br>
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 99 kb/s (default)<br>
    Metadata:<br>
      handler_name    : SoundHandler<br>
      vendor_id       : [0][0][0][0]<br>
Input #1, png_pipe, from '../input/RADE.png':<br>
  Duration: N/A, bitrate: N/A<br>
  Stream #1:0: Video: png, rgba(pc), 74x80 [SAR 3780:3780 DAR 37:40], 25 fps, 25 tbr, 25 tbn<br>
Stream mapping:<br>
  Stream #0:0 (h264) -> overlay<br>
  Stream #1:0 (png) -> overlay<br>
  overlay:default -> Stream #0:0 (libx264)<br>
  Stream #0:1 -> #0:1 (copy)<br>
Press [q] to stop, [?] for help<br>
[libx264 @ 0x7fe6d2907080] using cpu capabilities: MMX2 SSE2Fast SSSE3 SSE4.2<br>
[libx264 @ 0x7fe6d2907080] profile High, level 3.1, 4:2:0, 8-bit<br>
[libx264 @ 0x7fe6d2907080] 264 - core 164 r3099 e067ab0 - H.264/MPEG-4 AVC codec - Copyleft 2003-2022 - http://www.videolan.org/x264.html - options: cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=15 lookahead_threads=2 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop=0 weightp=2 keyint=250 keyint_min=25 scenecut=40 intra_refresh=0 rc_lookahead=40 rc=crf mbtree=1 crf=23.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00<br>
Output #0, mp4, to '../output/Spark_Course_Intro.mp4':<br>
  Metadata:<br>
    major_brand     : isom<br>
    minor_version   : 512<br>
    compatible_brands: isomiso2avc1mp41<br>
    encoder         : Lavf59.33.100<br>
  Stream #0:0: Video: h264 (avc1 / 0x31637661), yuv420p(progressive), 1280x720, q=2-31, 25 fps, 12800 tbn<br>
    Metadata:<br>
      encoder         : Lavc59.49.100 libx264<br>
    Side data:<br>
      cpb: bitrate max/min/avg: 0/0/0 buffer size: 0 vbv_delay: N/A<br>
  Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 99 kb/s (default)<br>
    Metadata:<br>
      handler_name    : SoundHandler<br>
      vendor_id       : [0][0][0][0]<br>
frame=  725 fps=205 q=-1.0 Lsize=    3934kB time=00:00:28.97 bitrate=1112.2kbits/s speed=8.19x    <br>
video:3556kB audio:353kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.641339%<br>
[libx264 @ 0x7fe6d2907080] frame I:3     Avg QP:13.22  size: 40411<br>
[libx264 @ 0x7fe6d2907080] frame P:192   Avg QP:20.42  size: 12491<br>
[libx264 @ 0x7fe6d2907080] frame B:530   Avg QP:28.32  size:  2115<br>
[libx264 @ 0x7fe6d2907080] consecutive B-frames:  1.9%  1.1%  2.1% 94.9%<br>
[libx264 @ 0x7fe6d2907080] mb I  I16..4: 43.6% 35.4% 21.0%<br>
[libx264 @ 0x7fe6d2907080] mb P  I16..4:  3.4%  3.0%  0.5%  P16..4: 16.3%  7.8%  3.7%  0.0%  0.0%    skip:65.3%<br>
[libx264 @ 0x7fe6d2907080] mb B  I16..4:  0.4%  0.4%  0.0%  B16..8: 19.7%  1.5%  0.3%  direct: 0.5%  skip:77.2%  L0:46.7% L1:43.6% BI: 9.7%<br>
[libx264 @ 0x7fe6d2907080] 8x8 transform intra:43.4% inter:67.4%<br>
[libx264 @ 0x7fe6d2907080] coded y,uvDC,uvAC intra: 23.1% 42.8% 9.5% inter: 5.6% 6.2% 0.3%<br>
[libx264 @ 0x7fe6d2907080] i16 v,h,dc,p: 25% 17% 10% 48%<br>
[libx264 @ 0x7fe6d2907080] i8 v,h,dc,ddl,ddr,vr,hd,vl,hu: 38% 19% 25%  3%  3%  3%  3%  3%  3%<br>
[libx264 @ 0x7fe6d2907080] i4 v,h,dc,ddl,ddr,vr,hd,vl,hu: 40% 16%  9%  5%  6% 10%  6%  5%  4%<br>
[libx264 @ 0x7fe6d2907080] i8c dc,h,v,p: 52% 20% 21%  8%<br>
[libx264 @ 0x7fe6d2907080] Weighted P-Frames: Y:0.0% UV:0.0%<br>
[libx264 @ 0x7fe6d2907080] ref P L0: 60.9% 15.2% 19.4%  4.5%<br>
[libx264 @ 0x7fe6d2907080] ref B L0: 90.3%  8.4%  1.2%<br>
[libx264 @ 0x7fe6d2907080] ref B L1: 96.8%  3.2%<br>
[libx264 @ 0x7fe6d2907080] kb/s:1004.35<br>
 Updated the Video : ../input/Spark_Course_Intro.mp4 with logo : ../input/RADE.png! New vedio : ../output/Spark_Course_Intro.mp4<br>
