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


def dtw_path(matrix):
    # start at 0,0
    x_values = []
    y_values = []


    traverse(0,0, x_values, y_values, matrix)

    return x_values, y_values


def traverse(x, y, x_values, y_values, matrix):
    if ((x+1 < len(matrix[0])) or (y+1 < len(matrix))):
    # append current point
        x_values.append(x)
        y_values.append(y)

        if ((x+1 < len(matrix[0])) and (y+1 < len(matrix))):
            diag = matrix[x+1][y+1]
            below = matrix[x+1][y]
            right = matrix[x][y+1]
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


def line_start(x_values, y_values):
    if len(x_values) == len(y_values):
        slope_match_count = 0
        slope_start_x = None
        slope_start_y = None

        for i in range(1, len(x_values)-50):  # len-1 because calculations include i+1 below
            print "i: ", i
            print "slope match count: ", slope_match_count
            if slope_match_count > consec_matches:
                print "diff in sec: ", float(slope_start_x-slope_start_y)/float(44.1)
                print slope_start_x, slope_start_y
                return slope_start_x*1000, slope_start_y*1000
            
            rise = float(y_values[i+50]) - float(y_values[i])
            run = float(x_values[i+50]) - float(x_values[i])
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






# a = [10, 20, 30]
# b = [1, 12, 3]
# d, m = dtw_dist(a,b)
# x, y = dtw_path(m)

# dist, costs = dtw.dtw_dist(r5, s5)
# x_values, y_values = dtw.dtw_path(costs)
