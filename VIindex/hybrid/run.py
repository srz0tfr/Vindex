from PIL import Image
import pytesseract
import numpy as np
import heading_box
import pytesseract

# takes location of original file and segmentation file and returns box coordinates (will be modified for text)
# need to update where to save file at line 42
# note it returns -1 when there is no box
def run_hybrid(org_image, seg_image, draw_box = 1):

    image_segmented = Image.open(seg_image)
    segmented_np = np.array(image_segmented)
    
    # count 
    # for i in segmented_np:
    #     for j in i:
    
    original_image = Image.open(org_image)
    temp = pytesseract.image_to_data(original_image,output_type= pytesseract.Output.DICT)
    # print(temp['level'])

    maxi = 0
    for i in temp['level']:
        maxi = max(maxi,i)

    line_level = maxi - 1

    box_location = []

    for i in range(len(temp['level'])):
        if temp['level'][i] == line_level:
            # print(temp['left'][i])
            box_location.append([temp['left'][i],temp['top'][i],temp['width'][i],temp['height'][i]])


    coordinates = heading_box.heading_box(segmented_np,box_location)
    if coordinates==-1:
        return ""
    

    if draw_box == 1:
        heading_box.draw_rectangle(original_image,coordinates,"hi")

    cropped_image = original_image.crop((coordinates[0],coordinates[1],coordinates[2],coordinates[3]))
    text = pytesseract.image_to_string(cropped_image)
    
    return coordinates

# example
print(run_hybrid("images/10355421_slide-023.jpg","static/10355421_slide-023.png"))