import cv2
import texter
import os
import argparse


def not_there(headings, heading):
    for i in headings:
        if i == heading:
            return False
    return True


def get_annotation(video_name,curr_model,full,interval):

    video_path = './videos/' + video_name
    v_cap = cv2.VideoCapture(video_path)

    indexing = []
    # interval = 3000

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
                print("At timestamp " + str(ts / 1000) + "s")
                timestamps.append(ts)
                frames.append(curr_frame)
                if full == 0:
                    import segmentation
                    model_temp = model.split('_')
                    resized_im, seg_map = segmentation.get_segmentation(curr_frame,model_temp[1])
                    # frame_location = 
                # else:



                heading  = texter.image_to_text(curr_frame, curr_model,full)
                # lines = contents.split('\n')
                # heading = None
                # for l in lines:
                #     if len(l) > 0 and not l.isspace():
                #         heading = l
                #         break
                # if heading != None:
                #     print(ord(heading[0]))
                if heading is not None and not_there(headings,heading) and heading != "" \
                    and heading != " " and heading != "\t":
                    # if len(headings) > 0:
                    indexing.append(texter.parse_timestamp(ts) + ' : ' + heading)
                    headings.append(heading)

                    # indexing.append(texter.parse_timestamp(ts) + ' - ')
                # name = './data/frame' + str(currentframe) + '.jpg'
                # print ('Creating...' + name) 
                # print(ts)

                # # writing the extracted images 
                # cv2.imwrite(name, curr_frame) 

                currentframe += 1
        else:
            break

    # indexing.append(texter.parse_timestamp(ts) + ' : ' + headings[-1])

    # out_file.close()
    v_cap.release()
    if full==0:
        print(indexing)
        return

    video_temp = video_name.split('.')
    ouput_indexing_path = "models_output/"+ curr_model + "/" + video_temp[0] + ".txt"
    f = open(ouput_indexing_path,"w")
    for index in indexing:
        f.write(index + '\n')
    f.close()
    return 
    

full = 1

# model_list = ["Tesseract","Model_Wise","Model_Sparse","Model_WiseW","Model_SparseW","Hybrid_Wise","Hybrid_Sparse","Hybrid_WiseW","Hybrid_SparseW"]
# model_list = ["Tesseract","Model_Wise","Model_WiseW","Hybrid_Wise","Hybrid_WiseW"]

#model_list = ["Hybrid_Wise"]
#model_list = ["Model_Wise"]

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-f','--file', help='Description for foo argument', required=True)
parser.add_argument('-i','--interval', help='Description for bar argument', type=float, required=False, default=1000)
parser.add_argument('-m','--model', help='Description for bar argument', required=False, default="Tesseract")

args = vars(parser.parse_args())

get_annotation(args['file'],args['model'],full, args['interval'])
run_segmenatation = 0
    