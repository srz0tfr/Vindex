import numpy as np

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

# array = np.zeros((100,100))
# for i in range(41,50):
#     for j in range(42,50):
#         array[i][j] = 1 

# for i in range(90,100):
#     for j in range(90,100):
#         array[i][j] = 1

# coordinates = heading_box(array)
# print(coordinates)
