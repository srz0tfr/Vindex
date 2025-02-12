import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="Path to video")
ap.add_argument("-t", "--timestamps", type=int, nargs='+', required=True,
                help="Time stamps in seconds (sorted)")
ap.add_argument("-o", "--output", default="../OCR/images/",
                help="Output path")
args = vars(ap.parse_args())

VIDEO_NAME = os.path.basename(args['video'])

v_cap = cv2.VideoCapture(args['video'])

if not os.path.exists(args['output']):
    os.makedirs(args['output'])

current = 0

while v_cap.isOpened():
    if current >= len(args['timestamps']):
        break
    frame_exists, curr_frame = v_cap.read()
    if frame_exists:
        ts = v_cap.get(cv2.CAP_PROP_POS_MSEC)
        if ts // 1000 == args['timestamps'][current]:
            cv2.imwrite(os.path.join(args['output'], f"{VIDEO_NAME}-frame-{ts//1000}s.png"), curr_frame)
            current += 1
    else:
        break

v_cap.release()
