import os

import numpy as np

from grid import Grid

if __name__ == '__main__':
    grids_path = 'D:\\example\\input_grids'  # path for package with *.grd files
    out_grid_path = 'D:\\example\\example.grd'  # path for out *.grd file
    normalization = True  # True - data will be normalized; False - not

    out_grid = Grid()
    out_grid.read_file(grids_path + '\\' + os.listdir(grids_path)[0])

    grids = []

    for i in os.listdir(grids_path):
        grids.append(Grid())  # creating Grid object
        grids[-1].read_file(grids_path + '\\' + i)  # reading file

    # data normalization
    if normalization:
        for i in grids:
            for x in range(i.number_columns):
                for y in range(i.number_rows):
                    if i.data[x][y] != i.blank_value:
                        i.data[x][y] -= (i.high_z + i.low_z) / 2
            i.set_low_high_z()

    # create array data structure
    data = np.zeros((len(grids), grids[0].number_columns, grids[0].number_rows), float)
    for i in range(len(grids)):
        data[i] = grids[i].data
    data = data.swapaxes(0, 2)
    data = data.swapaxes(0, 1)

    # sign classification
    for x in range(out_grid.number_columns):
        for y in range(out_grid.number_rows):
            if out_grid.blank_value in data[x][y]:
                out_grid.data = out_grid.blank_value
            else:
                value = 0
                for i in data[x][y]:
                    if i > 0:
                        value += 1
                    value <<= 1
                value >>= 1
                out_grid.data[x][y] = value

    out_grid.set_low_high_z()
    out_grid.write_binary_surfer7(out_grid_path)
