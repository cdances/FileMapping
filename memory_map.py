"""
author: Chris Dances
date: 3/19/2020

https://docs.python.org/2/library/mmap.html
"""

# Memory Mapping
##  https://docs.python.org/3/library/mmap.html

import struct
import mmap


def value_to_hex(v):
    if type(v) is float:
        return hex(struct.unpack('>I', struct.pack('>f', v))[0])
    elif type(v) is int:
        return hex(v)


def value_to_bytes(v):
    if type(v) is float:
        return bytes(struct.pack('>f', value))
    elif type(v) is int:
        return v.to_bytes(size, endian)


def bytes_to_value(b_in, v):
    if type(v) is float:
        return float(struct.unpack('>f', read_data)[0])
    elif type(v) is int:
        return int.from_bytes(read_data, byteorder=endian)


if __name__ == '__main__':

    file_name = "memory.data"

    endian = "big"

    value = 12345
    # value = 789.1234

    file_size = 1000
    file_data = bytes(file_size)
    offset = 100  # Offset Size
    size = 4  # Number of Bytes
    data = value_to_bytes(value)
    print(value, offset, size, data, data.hex('-'))

    # Create an initial file that is empty except for data with size and offset
    with open(file_name, "wb") as f:
        f.write(file_data)
        f.seek(offset)
        f.write(data)

    # Manipulate the Data as a mapped memory file
    with open(file_name, "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)

        print(mm[offset-size:offset+size*2])  # prints the raw bytes of the file

        read_data = mm[offset:offset+size]

        read_value = bytes_to_value(read_data, value)

        print(data, read_data)
        print(value_to_hex(value), value_to_hex(read_value))
        print(value, read_value)
        # close the map
        mm.close()


