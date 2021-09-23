import struct

import numpy as np


class Grid:
    """Class for working with Surfer Grids (*.grd)"""

    def __init__(self):
        self.__number_columns: int = 1
        self.__number_rows: int = 1
        self.__low_x: float = 0
        self.__high_x: float = 0
        self.__low_y: float = 0
        self.__high_y: float = 0
        self.__low_z: float = 0
        self.__high_z: float = 0
        self.__step_x: float = 0
        self.__step_y: float = 0
        self.__blank_value: float = 1701410009187828E23
        self.__data = np.zeros((1, 1))

    def set_low_high_z(self):
        """Find and set lowest and highest values of values matrix."""
        low_z = None
        high_z = None
        temp = False
        for x in range(self.__number_columns):
            for y in range(self.__number_rows):
                if self.__data[x][y] != self.__blank_value:
                    if temp:
                        if low_z > self.__data[x][y]:
                            low_z = self.__data[x][y]
                        if high_z < self.__data[x][y]:
                            high_z = self.__data[x][y]
                    else:
                        low_z = self.__data[x][y]
                        high_z = self.__data[x][y]
                        temp = True
        self.__low_z = low_z
        self.__high_z = high_z

    def read_txt_surfer6(self, path: str):
        """Read data from Surfer 6 ASCII file."""
        with open(path, "r") as file:
            file.readline()
            arr = list(map(int, file.readline().split()))
            self.__number_columns = arr[0]
            self.__number_rows = arr[1]
            arr = list(map(float, file.readline().split()))
            self.__low_x = arr[0]
            self.__high_x = arr[1]
            arr = list(map(float, file.readline().split()))
            self.__low_y = arr[0]
            self.__high_y = arr[1]
            arr = list(map(float, file.readline().split()))
            self.__low_z = arr[0]
            self.__high_z = arr[1]
            self.__data = np.zeros((self.__number_columns, self.__number_rows), float)
            arr = list(map(float, file.read().split()))
            for i in range(self.__number_rows):
                for j in range(self.__number_columns):
                    self.__data[j][i] = arr[i * self.__number_columns + j]
            self.__step_x = (self.__high_x - self.__low_x) / self.__number_columns
            self.__step_y = (self.__high_y - self.__low_y) / self.__number_rows
            self.__blank_value = 1701410009187828E23

    def write_txt_surfer6(self, path: str):
        """Write data to Surfer 6 ASCII file."""
        with open(path, "w") as file:
            file.write('DSAA\n')
            file.write(str(self.__number_columns) + ' ' + str(self.__number_rows) + '\n')
            file.write(str(self.__low_x) + ' ' + str(self.__high_x) + '\n')
            file.write(str(self.__low_y) + ' ' + str(self.__high_y) + '\n')
            file.write(str(self.__low_z) + ' ' + str(self.__high_z))
            for i in range(self.__number_rows):
                file.write('\n')
                for j in range(self.__number_columns):
                    if self.__data[j][i] != self.__blank_value:
                        file.write(str(self.__data[j][i]) + ' ')
                    else:
                        file.write(str(1701410009187828E23) + ' ')

    def read_binary_surfer6(self, path: str):
        """Read from Surfer 6 Binary file."""
        with open(path, "rb") as file:
            all_bytes = file.read()

        self.__number_columns = int.from_bytes(all_bytes[4:6], 'little')
        self.__number_rows = int.from_bytes(all_bytes[6:8], 'little')
        self.__low_x = struct.unpack('<d', all_bytes[8:16])[0]
        self.__high_x = struct.unpack('<d', all_bytes[16:24])[0]
        self.__low_y = struct.unpack('<d', all_bytes[24:32])[0]
        self.__high_y = struct.unpack('<d', all_bytes[32:40])[0]
        self.__low_z = struct.unpack('<d', all_bytes[40:48])[0]
        self.__high_z = struct.unpack('<d', all_bytes[48:56])[0]
        self.__data = np.zeros((self.__number_columns, self.__number_rows), float)
        for x in range(self.__number_columns):
            for y in range(self.__number_rows):
                self.__data[x][y] = struct.unpack('<f',
                                                  all_bytes[(56 + ((y * self.__number_columns) + x) * 4):
                                                            (56 + ((y * self.__number_columns) + x) * 4) + 4])[0]
        self.__step_x = (self.__high_x - self.__low_x) / (self.__number_columns - 1)
        self.__step_y = (self.__high_y - self.__low_y) / (self.__number_rows - 1)
        self.__blank_value = 1701410009187828E23

    def write_binary_surfer6(self, path: str):
        """Write to Surfer 6 Binary file."""
        with open(path, "wb") as file:
            file.write(bytes('DSBB', 'ascii'))
            file.write(struct.pack('<h', self.__number_columns))
            file.write(struct.pack('<h', self.__number_rows))
            file.write(struct.pack('<d', self.__low_x))
            file.write(struct.pack('<d', self.__high_x))
            file.write(struct.pack('<d', self.__low_y))
            file.write(struct.pack('<d', self.__high_y))
            file.write(struct.pack('<d', self.__low_z))
            file.write(struct.pack('<d', self.__high_z))

            for y in range(self.__number_rows):
                for x in range(self.__number_columns):
                    if self.__data[x][y] != self.__blank_value:
                        file.write(struct.pack('<f', self.__data[x][y]))
                    else:
                        file.write(struct.pack('<f', 1701410009187828E23))

    def read_binary_surfer7(self, path: str):
        """Read from Surfer 7 Binary file."""
        with open(path, "rb") as file:
            all_bytes = file.read()

        self.__number_columns = int.from_bytes(all_bytes[24:28], 'little')
        self.__number_rows = int.from_bytes(all_bytes[20:24], 'little')
        self.__low_x = struct.unpack('<d', all_bytes[28:36])[0]
        self.__low_y = struct.unpack('<d', all_bytes[36:44])[0]
        self.__low_z = struct.unpack('<d', all_bytes[60:68])[0]
        self.__high_z = struct.unpack('<d', all_bytes[68:76])[0]
        self.__step_x = struct.unpack('<d', all_bytes[44:52])[0]
        self.__step_y = struct.unpack('<d', all_bytes[52:60])[0]
        self.__blank_value = struct.unpack('<d', all_bytes[84:92])[0]
        self.__data = np.zeros((self.__number_columns, self.__number_rows), float)
        for x in range(self.__number_columns):
            for y in range(self.__number_rows):
                self.__data[x][y] = struct.unpack('<d',
                                                  all_bytes[(100 + ((y * self.__number_columns) + x) * 8):
                                                            (100 + ((y * self.__number_columns) + x) * 8) + 8])[0]
        self.__high_x = self.__low_x + self.__step_x * (self.__number_columns - 1)
        self.__high_y = self.__low_y + self.__step_y * (self.__number_rows - 1)

    def write_binary_surfer7(self, path: str):
        """Write to Surfer 7 Binary file."""
        with open(path, "wb") as file:
            file.write(struct.pack('<l', 0x42525344))
            file.write(struct.pack('<l', 4))
            file.write(struct.pack('<l', 2))
            file.write(struct.pack('<l', 0x44495247))
            file.write(struct.pack('<l', 72))
            file.write(struct.pack('<l', self.__number_rows))
            file.write(struct.pack('<l', self.__number_columns))
            file.write(struct.pack('<d', self.__low_x))
            file.write(struct.pack('<d', self.__low_y))
            file.write(struct.pack('<d', self.__step_x))
            file.write(struct.pack('<d', self.__step_y))
            file.write(struct.pack('<d', self.__low_z))
            file.write(struct.pack('<d', self.__high_z))
            file.write(struct.pack('<d', 0))
            file.write(struct.pack('<d', self.__blank_value))
            file.write(struct.pack('<l', 0x41544144))
            file.write(struct.pack('<l', self.__number_rows * self.__number_columns * 8))

            for y in range(self.__number_rows):
                for x in range(self.__number_columns):
                    file.write(struct.pack('<d', self.__data[x][y]))

    def read_file(self, path: str):
        """Read *.grd file"""
        with open(path, "rb") as file:
            grd_id = file.read()[0:4]
        if grd_id == bytes('DSBB', 'ascii'):
            self.read_binary_surfer6(path)
        elif grd_id == bytes('DSAA', 'ascii'):
            self.read_txt_surfer6(path)
        elif grd_id == bytes('DSRB', 'ascii'):
            self.read_binary_surfer7(path)

    # getters and setters
    @property
    def number_columns(self):
        return self.__number_columns

    @number_columns.setter
    def number_columns(self, number_columns):
        self.__number_columns = number_columns

    @property
    def number_rows(self):
        return self.__number_rows

    @number_rows.setter
    def number_rows(self, number_rows):
        self.__number_rows = number_rows

    @property
    def low_x(self):
        return self.__low_x

    @low_x.setter
    def low_x(self, low_x):
        self.__low_x = low_x

    @property
    def high_x(self):
        return self.__high_x

    @high_x.setter
    def high_x(self, high_x):
        self.__high_x = high_x

    @property
    def low_y(self):
        return self.__low_y

    @low_y.setter
    def low_y(self, low_y):
        self.__low_y = low_y

    @property
    def high_y(self):
        return self.__high_y

    @high_y.setter
    def high_y(self, high_y):
        self.__high_y = high_y

    @property
    def low_z(self):
        return self.__low_z

    @low_z.setter
    def low_z(self, low_z):
        self.__low_z = low_z

    @property
    def high_z(self):
        return self.__high_z

    @high_z.setter
    def high_z(self, high_z):
        self.__high_z = high_z

    @property
    def step_x(self):
        return self.__step_x

    @step_x.setter
    def step_x(self, step_x):
        self.__step_x = step_x

    @property
    def step_y(self):
        return self.__step_y

    @step_y.setter
    def step_y(self, step_y):
        self.__step_y = step_y

    @property
    def blank_value(self):
        return self.__blank_value

    @blank_value.setter
    def blank_value(self, blank_value):
        self.__blank_value = blank_value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data
