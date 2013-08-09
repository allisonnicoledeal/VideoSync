# DTW
# http://en.wikipedia.org/wiki/Dynamic_time_warping

consec_matches = 10
slope_err = float(0.1)

# array1 is M is rows, array2 is columns
def dtw_dist(array1, array2):
    m = len(array1)
    n = len(array2)

    # Create matrix
    DTW = []

    for i in range(m):
        new_row = [float("inf")] * n  # revisit and use list append instead of pre-populating matrix
        DTW.append(new_row)

    DTW[0][0] = 0

    # Populate matrix with cost values
    for i in range(1, m):
        for j in range(1, n):
            cost = abs(array1[i-1]-array2[j-1])
            min_val = min(DTW[i-1][j], DTW[i][j-1], DTW[i-1][j-1])
            DTW[i][j] = cost + min_val

    return DTW[m-1][n-1], DTW


# def dtw_path(matrix): # == REPLACED WITH ITERATIVE FXN =========
#     # start at 0,0
#     x_values = []
#     y_values = []

#     traverse(0,0, x_values, y_values, matrix)

#     return x_values, y_values


def traverse(x, y, x_values, y_values, matrix):
    if ((x+1 < len(matrix[0])) or (y+1 < len(matrix))):
    # append current point
        x_values.append(x)
        y_values.append(y)
        print "len x values:", len(x_values)
        print "len y values:", len(y_values)
        print ""

        if ((x+1 < len(matrix[0])) and (y+1 < len(matrix))):
            diag = matrix[y+1][x+1]
            below = matrix[y+1][x]
            right = matrix[y][x+1]
            min_neighbour = min(diag, below, right)
            if diag == min_neighbour:
                traverse(x+1, y+1, x_values, y_values, matrix)
            elif below == min_neighbour:
                traverse(x+1, y, x_values, y_values, matrix)
            else:  # right is min neighb
                traverse(x, y+1, x_values, y_values, matrix)

        elif (x+1 < len(matrix[0])):
            # min_neighbour = matrix[x+1][y]
            traverse(x+1, y, x_values, y_values, matrix)
        else:  # implied y+1 < len(matrix)
            # min_neighbour = matrix[x][y+1]
            traverse(x, y+1, x_values, y_values, matrix)


def dtw_path(matrix):
    # start at 0,0
    x = 0
    y = 0
    x_values = []
    y_values = []

    while ((x+1 < len(matrix[0])) or (y+1 < len(matrix))):
        x_values.append(x)
        y_values.append(y)

        if ((x+1 < len(matrix[0])) and (y+1 < len(matrix))):
            diag = matrix[y+1][x+1]
            below = matrix[y+1][x]
            right = matrix[y][x+1]
            min_neighbor = min(diag, below, right)
            if diag == min_neighbor:
                x += 1
                y += 1
            elif below == min_neighbor:
                y += 1
            else:  # right is min neighb
                x += 1

        elif (x+1 < len(matrix[0])):
            x += 1
        else:  # implied y+1 < len(matrix)
            y += 1

    return x_values, y_values


def line_start(x_values, y_values, sample_len):
    samp_len = sample_len/1000
    if len(x_values) == len(y_values):
        slope_match_count = 0
        slope_start_x = None
        slope_start_y = None

        for i in range(1, len(x_values)-sample_len):  # len-1 because calculations include i+1 below
            print "i: ", i
            print "slope match count: ", slope_match_count
            if slope_match_count > consec_matches:
                print "diff in sec: ", float(slope_start_x-slope_start_y)/float(44.1)
                print slope_start_x, slope_start_y
                return slope_start_x*1000, slope_start_y*1000
            
            rise = float(y_values[i+sample_len]) - float(y_values[i])
            run = float(x_values[i+sample_len]) - float(x_values[i])
            if run > 0:
                slope = rise/run
                print "slope: ", slope

                if (slope < (float(1)+slope_err)) and (slope > (float(1)-slope_err)):
                    slope_match_count += 1

                    if slope_start_x is None:  # and slope start y == None
                        slope_start_x = x_values[i]
                        slope_start_y = y_values[i]

                else:  # reset
                    slope_match_count = 0
                    slope_start_x = None
                    slope_start_y = None




# ==========TEST ======================

# a = [10, 20, 30, 5, 2]
# b = [1, 12, 3, 5, 2]
# d, m = dtw_dist(a,b)
# x, y = dtw_path(m)

# dist, costs = dtw.dtw_dist(r5, s5)
# x_values, y_values = dtw.dtw_path(costs)
# plt.plot(y_values, x_values)
# plt.show()
