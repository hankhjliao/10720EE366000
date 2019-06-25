# modified from https://www.github.com/ghallak/jpeg-python/

import os
import huffman
import time

uint_to_binstr = (lambda number, size: bin(number)[2:][-size:].zfill(size))
binstr_flip = (lambda binstr: ''.join(map(lambda c: '0' if c == '1' else '1', binstr)))
flatten = (lambda lst: [item for sublist in lst for item in sublist])


def int_to_binstr(n):
    if n == 0:
        return ''
    binstr = bin(abs(n))[2:]
    # change every 0 to 1 and vice verse when n is negative
    return binstr if n > 0 else binstr_flip(binstr)


def huffman_table(dc, ac):
    DC0 = huffman.HuffmanTree(dc[0])
    DC1 = huffman.HuffmanTree(dc[1])
    DC2 = huffman.HuffmanTree(dc[2])
    AC0 = huffman.HuffmanTree(flatten(ac[0]))
    AC1 = huffman.HuffmanTree(flatten(ac[1]))
    AC2 = huffman.HuffmanTree(flatten(ac[2]))
    tables = {'DC0': DC0.value_to_bitstring_table(),
              'DC1': DC1.value_to_bitstring_table(),
              'DC2': DC2.value_to_bitstring_table(),
              'AC0': AC0.value_to_bitstring_table(),
              'AC1': AC1.value_to_bitstring_table(),
              'AC2': AC2.value_to_bitstring_table()}
    return tables


def write_to_binstr(filepath, row, dc, ac, RLdata):
    start = time.process_time_ns()

    try:
        f = open(filepath, 'wb')
    except FileNotFoundError as e:
        raise FileNotFoundError(
                "No such directory: {}".format(
                    os.path.dirname(filepath))) from e

    tables = huffman_table(dc, ac)

    col = len(dc[0]) // (row // 8) * 8

    out = ''
    out += uint_to_binstr(688380, 64)

    for table_name in ['DC0', 'DC1', 'DC2', 'AC0', 'AC1', 'AC2']:
        # 16 bits for 'table_size'
        out += uint_to_binstr(len(tables[table_name]), 16)

        for key, value in tables[table_name].items():
            if table_name in {'DC0', 'DC1', 'DC2'}:
                out += uint_to_binstr(key, 16)
                out += uint_to_binstr(len(value), 16)
                out += value
            else:
                out += uint_to_binstr(key, 8)
                out += uint_to_binstr(len(value), 8)
                out += value

    # 32 bits for 'row' and 'col'
    out += uint_to_binstr(row//8, 32)
    out += uint_to_binstr(col//8, 32)

    # DC terms
    for k in range(3):
        if k == 0:
            dc_table = tables['DC0']
        elif k == 1:
            dc_table = tables['DC1']
        else:
            dc_table = tables['DC2']
        for i in range(len(dc[0])):
            out += dc_table[dc[k][i]]

    # AC terms
    for k in range(3):
        if k == 0:
            ac_table = tables['AC0']
        elif k == 1:
            ac_table = tables['AC1']
        else:
            ac_table = tables['AC2']
        for i in range(row//8):
            for j in range(col//8):
                for l in range(len(ac[k][i*col//8+j])):
                    out += ac_table[ac[k][i*col//8+j][l]]
                    out += int_to_binstr(RLdata[k][i*col//8+j][l])
    if len(out) % 64 != 0:
        out += '0' * (64 - (len(out) % 64))
    for i in range(len(out)//64):
        f.write(int(out[i*64:i*64+64], 2).to_bytes(8, 'big'))
    f.close()

    end = time.process_time_ns()
    print("[INFO] Saved:", end - start, "ns")


class JPEGFileReader:
    TABLE_SIZE_BITS = 16
    BLOCKS_COUNT_BITS = 32

    DC_CODE_LENGTH_BITS = 16
    CATEGORY_BITS = 16

    AC_CODE_LENGTH_BITS = 8
    RUN_LENGTH_BITS = 8
    # SIZE_BITS = 4

    def __init__(self, filepath):
        try:
            f = open(filepath, 'rb')
        except FileNotFoundError as e:
            raise FileNotFoundError(
                    "No such directory: {}".format(
                        os.path.dirname(filepath))) from e
        self.__string = ''
        byte = f.read(8)
        if int.from_bytes(byte, 'big') != 688380:
            print('[ERROR] Invalid binary file.')
            exit(1)
        byte = f.read(8)
        while byte != b"":
            b = bin(int.from_bytes(byte, 'big'))[2:]
            if len(b) % 64 != 0:
                b = '0' * (64 - (len(b) % 64)) + b
            self.__string += b
            byte = f.read(8)
        self.__string_index = 0

    def read_int(self, size):
        if size == 0:
            return 0

        # the most significant bit indicates the sign of the number
        bin_num = self.__read_str(size)
        if bin_num[0] == '1':
            return self.__int2(bin_num)
        else:
            return self.__int2(binstr_flip(bin_num)) * -1

    def read_dc_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            category = self.__read_uint(self.CATEGORY_BITS)
            code_length = self.__read_uint(self.DC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = category
        return table

    def read_ac_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)

        for _ in range(table_size):
            run_length = self.__read_uint(self.RUN_LENGTH_BITS)
            code_length = self.__read_uint(self.AC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = run_length
        return table

    def read_blocks_count(self):
        return self.__read_uint(self.BLOCKS_COUNT_BITS)

    def read_huffman_code(self, table):
        prefix = ''
        # TODO: break the loop if __read_char is not returing new char
        while prefix not in table:
            prefix += self.__read_char()
        return table[prefix]

    def __read_uint(self, size):
        if size <= 0:
            raise ValueError("size of unsigned int should be greater than 0")
        return self.__int2(self.__read_str(size))

    def __read_str(self, length):
        output = self.__string[self.__string_index:self.__string_index + length]
        self.__string_index += length
        return output

    def __read_char(self):
        return self.__read_str(1)

    def __int2(self, bin_num):
        return int(bin_num, 2)


def read_image_file(filepath):
    start = time.process_time_ns()

    reader = JPEGFileReader(filepath)

    tables = dict()
    for table_name in ['DC0', 'DC1', 'DC2', 'AC0', 'AC1', 'AC2']:
        if 'DC' in table_name:
            tables[table_name] = reader.read_dc_table()
        else:
            tables[table_name] = reader.read_ac_table()

    row = reader.read_blocks_count()
    col = reader.read_blocks_count()

    dc = [[], [], []]
    ac = [[], [], []]
    RLdata = [[], [], []]

    # DC terms
    for k in range(3):
        if k == 0:
            dc_table = tables['DC0']
        elif k == 1:
            dc_table = tables['DC1']
        else:
            dc_table = tables['DC2']
        for i in range(row*col):
            dc[k].append(reader.read_huffman_code(dc_table))

    # AC terms
    for k in range(3):

        if k == 0:
            ac_table = tables['AC0']
        elif k == 1:
            ac_table = tables['AC1']
        else:
            ac_table = tables['AC2']
        for i in range(row):
            for j in range(col):
                data = []
                ac_tmp = []
                cells_count = 0

                while cells_count <= 63:
                    run_length = reader.read_huffman_code(ac_table)
                    size = run_length % 16
                    run_length = run_length // 16

                    if run_length == 0 and size == 0:
                        ac_tmp.append(0)
                        value = reader.read_int(size)
                        data.append(0)
                        break
                    else:
                        for i in range(run_length):
                            ac.append(0)
                            cells_count += 1
                        if size == 0:
                            ac_tmp.append(0)
                        else:
                            value = reader.read_int(size)
                            ac_tmp.append(int(run_length*16+size))
                            data.append(value)
                        cells_count += 1
                ac[k].append(ac_tmp)
                RLdata[k].append(data)

    end = time.process_time_ns()
    print("[INFO] Load:", end - start, "ns")
    return (row * 8, dc, ac, RLdata)
