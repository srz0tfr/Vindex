import cv2
from PIL import Image
import os
import pytesseract
import enum
import json
import numpy as np

# parses timestamp in ms into HH::MM::SS format
def parse_timestamp(ts, sep='::'):
    seconds = int(ts // 1000)
    minutes = int(seconds // 60)
    seconds = seconds % 60
    hours = int(minutes // 60)
    minutes = minutes % 60

    if seconds < 10:
        seconds = f'0{seconds}'
    else:
        seconds = f'{seconds}'

    if minutes < 10:
        minutes = f'0{minutes}'
    else:
        minutes = f'{minutes}'

    return f'{hours}{sep}{minutes}{sep}{seconds}'


def preprocess(image, method='thresh'):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if method == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif method == "blur":
        gray = cv2.medianBlur(gray, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    image = Image.open(filename)
    os.remove(filename)
    return image

# to get heading box
def heading_box(array):
    rows = len(array)
    cols = len(array[0])
    max_row = 0
    max_col = 0
    min_row = 100000
    min_col = 100000
    print(rows,cols)
    # return []
    for i in range(rows):
        for j in range(cols):
            count_ones = 0
            for len1 in range(10):
                for len2 in range(10):
                    if i+len1<rows and j+len2<cols and array[i+len1][j+len2]==1:
                        count_ones+=1
            if count_ones >=50:
                max_row = max(max_row,i+9)
                max_col = max(max_col,j+9)
                min_row = min(min_row,i)
                min_col = min(min_col,j)
    return [min_col,min_row,max_col,max_row]

def image_to_text(image, preprocess_method="thresh"):
    image = preprocess(image, method=preprocess_method)
    
    """
    Code where we are calling our trained model
    """
    
    
    # the array must be numpy array containing 1s and 0s
    crop_size = heading_box(array)
    cropped_image = image.crop((crop_size[0],crop_size[1],crop_size[2],crop_size[3]))
    text = pytesseract.image_to_string(cropped_image)
    return text

# img = Image.open(r"../q1_2.png")
# wid,height = img.size
# x = np.zeros((height,wid))
# for i in range(100):
#     for j in range(100):
#         x[i][j] = 1

# re = heading_box(x)
# im = img.crop((re[0],re[1],re[2],re[3]))
# im.show()
# text = pytesseract.image_to_string(im)
# print(text)

def parse_bounding_boxes_util(bounding_boxes, i, lvl):

    if i >= len(bounding_boxes['level']):
        return None

    if bounding_boxes['level'][i] == 5:
        contents = []
        while i < len(bounding_boxes['level']) and bounding_boxes['level'][i] == 5:
            contents.append(bounding_boxes['text'][i])
            i += 1
        lvl -= 1
        return contents, i, lvl
    else:
        contents = []
        while i < len(bounding_boxes['level']) and bounding_boxes['level'][i] == lvl:
            box = {'content_type': bounding_boxes['level'][i],
                   'left': bounding_boxes['left'][i],
                   'top': bounding_boxes['top'][i],
                   'width': bounding_boxes['width'][i],
                   'height': bounding_boxes['height'][i]
                   }
            lvl += 1
            i += 1
            box['content'], i, lvl = parse_bounding_boxes_util(bounding_boxes, i, lvl)
            contents.append(box)
        lvl -= 1
        return contents, i, lvl


def parse_bounding_boxes(bounding_boxes):
    return parse_bounding_boxes_util(bounding_boxes, 0, 1)[0]


# location_threshold means the fraction of page height to search for the heading
def get_heading_from_image(image, preprocess_method='thresh', location_threshold=0.6):
    image = preprocess(image, method=preprocess_method)
    bounds = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    # TODO: Implementation remaining

    print(json.dumps(parse_bounding_boxes_util(bounds, 0, 1)[0], skipkeys=True, indent=4))

    return parse_bounding_boxes_util(bounds, 0, 1)
    # print(bounds)
