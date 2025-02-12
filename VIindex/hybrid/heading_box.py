import numpy as np

def draw_rectangle(resized_im,coordinates,file_box):

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
    plt.savefig(file_box)


def heading_box(array, box_location):
    rows = len(array)
    cols = len(array[0])
    max_row = 0
    max_col = 0
    min_row = 100000
    min_col = 100000
    # print(rows,cols)
    # return []
    prefix_rect = np.zeros((rows,cols))
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if array[i][j] == 1:
                cnt += 1    
            else:
                array[i][j] = 0
    # print(cnt)
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
    # print(box_location)
    for curr_box in box_location:
        done = False
        for row in range(curr_box[1],curr_box[1]+curr_box[3]):
            for col in range(curr_box[0],curr_box[0]+curr_box[2]):
                count_ones = 0
                if row + 10 < rows and col + 10 < cols:
                    count_ones = prefix_rect[row+10][col+10] + prefix_rect[row][col] - prefix_rect[row+10][col] - prefix_rect[row][col+10]
                # print(count_ones)
                if count_ones>=10:
                    max_row = max(max_row,curr_box[1]+curr_box[3])
                    max_col = max(max_col,curr_box[0]+curr_box[2])
                    min_row = min(min_row,curr_box[1])
                    min_col = min(min_col,curr_box[0])
                    done = True
                if done:
                    break
            if done:
                break

    # print([min_col,min_row,max_col,max_row])
    if [min_col,min_row,max_col,max_row]==[100000, 100000, 0, 0]:
        return -1
    return [min_col,min_row,max_col,max_row]
