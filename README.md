# Introduction



# Instructions

1. `git clone https://github.com/https://github.com/srz0tfr/Vindex.git
2. `cd OCR`
3. `sudo apt-get install tesseract-ocr`
4. `pip install pytesseract`
5. `pip install opencv-python`
6. `pip install pillow`
7. `python video.py -v <path-to-video> -i <sampling-interval> -e <stop-timestamp> -o <path-to-output-folder>`<br />
  `Suggested to make a model based on your requirements.`


# Command line arguments to video.py

- `-v` or `--video`: Path to the video file. Required.
- `-i` or `--interval`: Sampling interval in ms. Default value is `actual`, in which each frame is processed.
- `-e` or `--end`: Time in ms upto which the video should be processed. Default value is `actual`, in which entire video is processed.
- `-o` or `--output`: Path to output folder, where output txt file will be stored. Default value is './results/'

# Utilities

- To conveniently download a YouTube video, use the script 'yt_downloader.py' provided in the 'utils' folder: `python yt_downloader.py -u <url-of-video>`
- To extract frame(s) from a given video as .png images, use the script 'ext_frame.py' provided in the 'utils' folder: `python ext_frame.py -v <path-to-video> -t <list-of-timestamps-in-seconds-of-frames-to-be-extracted> -o <path-of-output-folder>`
- To display tesseract bounding boxes for an image, use the script 'bounding_boxes.py' in 'OCR' folder: `python bounding_boxes.py -i <path-to-image>`
