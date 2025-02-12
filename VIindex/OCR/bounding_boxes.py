import pytesseract
from pytesseract import Output
from utils import *
import cv2
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
args = vars(ap.parse_args())

img = cv2.imread(args['image'])
img = preprocess(img, method='thresh')

d = pytesseract.image_to_data(img, output_type=Output.DICT)
print(d)
n_boxes = len(d['level'])

for k in d['level']:
    img = cv2.imread(args['image'])

    for i in range(n_boxes):
        if d['level'][i] != k:
            continue
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow(f'img{k}', img)


cv2.waitKey(0)