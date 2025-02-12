import cv2
import utils
import os
import argparse


def not_there(headings, heading):
    for i in headings:
        if i == heading:
            return False
    return True


def get_annotation(video_name,model):

    # ap = argparse.ArgumentParser()
    # ap.add_argument("-v", "--video", required=True,
    #                 help="path to input video to be OCR'd")
    # ap.add_argument("-i", "--interval", required=False, default="actual",
    #                 help="interval in ms to leave between successive samples")
    # ap.add_argument("-e", "--end", required=False, default="actual",
    #                 help="time in ms upto which video is processed")
    # ap.add_argument("-o", "--output", required=False, default="./results/",
    #                 help="path to output folder")
    # args = vars(ap.parse_args())

    # if not os.path.exists(args['output']):
    #     os.makedirs(args['output'])

    # OUTPUT_FILENAME = os.path.basename(args['video']) + '-index.txt'
    # OUTPUT_FILE_PATH = os.path.join(args['output'], OUTPUT_FILENAME)

    # out_file = open(OUTPUT_FILE_PATH, 'w')
    video_path = video_name
    v_cap = cv2.VideoCapture(video_path)

    indexing = []
    interval = 1000

    frames = []
    headings = []
    timestamps = []

    currentframe = 0

    while v_cap.isOpened():
        frame_exists, curr_frame = v_cap.read()
        if frame_exists:
            ts = v_cap.get(cv2.CAP_PROP_POS_MSEC)
            # if args['end'] != 'actual' and ts >= float(args['end']):
            #     break   
            if len(timestamps) == 0 or interval == "actual" or \
                    ts - timestamps[-1] >= float(interval):

                timestamps.append(ts)
                frames.append(curr_frame)

                contents = utils.image_to_text(curr_frame, model)
                # print(contents)
                lines = contents.split('\n')
                # print(lines)
                # break

                heading = None
                for l in lines:
                    if len(l) > 0 and not l.isspace():
                        heading = l
                        break
                # if heading != None:
                #     print(ord(heading[0]))
                if heading is not None and (len(headings) == 0 or not_there(headings,heading)) and heading != "" \
                    and heading != " " and heading != "\t":
                    # if len(headings) > 0:
                    indexing.append(utils.parse_timestamp(ts) + ' : ' + heading)
                    # indexing.append(utils.parse_timestamp(ts) + ' - ')
                    headings.append(heading)
                # name = './data/frame' + str(currentframe) + '.jpg'
                # print ('Creating...' + name) 
                # print(ts)

                # # writing the extracted images 
                # cv2.imwrite(name, curr_frame) 

                currentframe += 1
        else:
            break
    
    # indexing.append(utils.parse_timestamp(ts) + ' : ' + headings[-1])

    # out_file.close()
    v_cap.release()
    return indexing

# print(get_annotation("Presentation.mp4","Hi"))