import os
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImagePalette

# %tensorflow_version 1.x
import tensorflow as tf

from numpy import asarray
import numpy as np

# import heading_box

LABEL_NAMES = []
FULL_COLOR_MAP = []

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.compat.v1.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.compat.v1.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
        image: A PIL.Image object, raw input image.

        Returns:
        resized_image: RGB image resized from original input image.
        seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map


def create_pascal_label_colormap():
    """Creates a label colormap used in PASCAL VOC segmentation benchmark.

    Returns:
        A Colormap for visualizing segmentation results.
    """
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
            ind >>= 3

    return colormap


def label_to_color_image(label):
    """Adds color defined by the dataset colormap to the label.

    Args:
        label: A 2D array with integer type, storing the segmentation label.

    Returns:
        result: A 2D array with floating type. The element of the array
        is the color indexed by the corresponding element in the input label
        to the PASCAL color map.

        Raises:
        ValueError: If label is not of rank 2 or its value is larger than color
          map maximum entry.
    """
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')

    # colormap = create_pascal_label_colormap()
    colormap = np.array(Image.open('2007_000032.png').getpalette())
    colormap.resize((256, 3))

    # for i in colormap:
    #     print(i)

    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')
    return colormap[label]


def vis_segmentation(image, seg_map,file_vis,file_box):
    """Visualizes input image, segmentation map and overlay view."""

    plt.figure(figsize=(15, 5))

    grid_spec = gridspec.GridSpec(1, 2, width_ratios=[6, 2])
    for i in seg_map:
        print(i)
    # plt.subplot(grid_spec[0])
    # plt.imshow(image)
    # plt.axis('off')
    # plt.title('input image')

    # plt.subplot(grid_spec[1])
    seg_image = label_to_color_image(seg_map).astype(np.uint8)
    # plt.imshow(seg_image)
    # plt.axis('off')
    # plt.title('segmentation map')

    plt.subplot(grid_spec[0])
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.7)
    plt.axis('off')
    plt.title('segmentation overlay')

    unique_labels = np.unique(seg_map)
    ax = plt.subplot(grid_spec[1])
    plt.imshow(
        FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
    plt.yticks(fontsize = 13)
    plt.xticks([], [])
    ax.tick_params(width=0.0)
    plt.grid('off')
    # plt.show()

    plt.savefig('./static/' + file_vis)

def draw_rectangle(resized_im,coordinates,file_vis,file_box):

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(resized_im)

    # Create a Rectangle patch
    rect = patches.Rectangle((coordinates[0], coordinates[1]), coordinates[2]-coordinates[0], coordinates[3]-coordinates[1], linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.axis('off')
    plt.savefig('./static/' + file_box)


# def run_visualization(image_name, save_visul,MODEL,file_vis,file_box):
#     image_path = './static/' + image_name
#     im = image_name
#     if save_visul == 1:
#         im = Image.open(image_path)  

#     resized_im, seg_map = MODEL.run(im)
#     box_coordinates = heading_box.heading_box(np.copy(seg_map))
    
#     if save_visul == 1:
#         vis_segmentation(resized_im, seg_map, file_vis, file_box)
#         draw_rectangle(resized_im, box_coordinates, file_vis, file_box)

#     return box_coordinates
    

def heading_box(array):
    rows = len(array)
    cols = len(array[0])
    max_row = 0
    max_col = 0
    min_row = 100000
    min_col = 100000
    # print(rows,cols)
    # return []
    prefix_rect = np.zeros((rows,cols))

    for i in range(rows):
        for j in range(cols):
            if array[i][j] == 1:
                pass
            else:
                array[i][j] = 0

    # precompute
    prefix_rect[0][0] = array[0][0]
    for i in range(1,cols):
        prefix_rect[0][i] = prefix_rect[0][i-1] + array[0][i]
    
    for i in range(1,rows):
        for j in range(cols):
            if j == 0:
                prefix_rect[i][j] = prefix_rect[i-1][j] + array[i][j]
            else:
                prefix_rect[i][j] = prefix_rect[i-1][j] + prefix_rect[i][j-1] - prefix_rect[i-1][j-1] + array[i][j]

    # print(prefix_rect)
    # for i in range(rows):
    #     print(i)
    #     print(prefix_rect[i])
    

    for i in range(rows):
        for j in range(cols):
            
            if max_row != 0 and i - max_row >= 50:
                break
            count_ones = 0
            if i + 10 < rows and j + 10 < cols:
                count_ones = prefix_rect[i+10][j+10] + prefix_rect[i][j] - prefix_rect[i+10][j] - prefix_rect[i][j+10]

            # for len1 in range(10):
            #     for len2 in range(10):
            #         if i+len1<rows and j+len2<cols:
            #           if array[i+len1][j+len2]==1 or array[i+len1][j+len2]==2:
            #             count_ones+=1
            # if 
            # if i >= 80 and j>=80 and i<=90 and j <= 90:
                # print(i,j,count_ones)
            if count_ones >= 20:
                max_row = max(max_row,i+9)
                max_col = max(max_col,j+9)
                min_row = min(min_row,i)
                min_col = min(min_col,j)

        if max_row != 0 and i - max_row >= 50:
            break

    return [min_col,min_row,max_col,max_row]
      

def get_segmentation(image,model):
    global FULL_COLOR_MAP
    global LABEL_NAMES

    LABEL_NAMES = np.asarray([
        'background', 'heading'
    ])


    FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
    FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)

    MODEL_NAME = ''
    # MODEL_NAME = 'mobilenetv2_coco_voctrainaug'  # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']
    if model == "Wise":
        MODEL_NAME = 'wise_heading.tar.gz'
    elif model == "Sparse":
        MODEL_NAME = 'sparse_heading.tar.gz'
    elif model == "WiseW":
        MODEL_NAME = 'wise_heading_weighted.tar.gz'
    else:
        MODEL_NAME = 'sparse_heading_weighted.tar.gz'


    model_path = './models/'+ MODEL_NAME
    MODEL = DeepLabModel(model_path)
    # print('model loaded successfully!')

    # SAMPLE_IMAGE = 'image1'  # @param ['image1', 'image2', 'image3']
    # IMAGE_URL = ''  #@param {type:"string"}

    # _SAMPLE_URL = ('https://github.com/tensorflow/models/blob/master/research/'
    #             'deeplab/g3doc/img/%s.jpg?raw=true')
    resized_im, seg_map = MODEL.run(image)

    # return run_visualization(image_name,save_visul,MODEL,file_vis,file_box)
    return [resized_im,seg_map]

