import argparse
import cv2
import JEPGIO
import numpy as np
import time

rnd_seed = 2128

quatization_matrix = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 99]])


def zig_zag(x):
    '''
    zig_zag(x) -> zig_zag_code\n\n
    This function will use the zig-zag scan to encode the input to a one
    dimention vector.\n
    ## Parameter
    x: The input 8*8 array.\n
    ## Parameter
    zig_zag_code: The 1*64 vector after zig-zag scan.
    '''
    zig_zag_code = [
        x[0, 0],
        x[1, 0], x[0, 1],
        x[0, 2], x[1, 1], x[2, 0],
        x[3, 0], x[2, 1], x[1, 2], x[0, 3],
        x[0, 4], x[1, 3], x[2, 2], x[3, 1], x[4, 0],
        x[5, 0], x[4, 1], x[3, 2], x[2, 3], x[1, 4], x[0, 5],
        x[0, 6], x[1, 5], x[2, 4], x[3, 3], x[4, 2], x[5, 1], x[6, 0],
        x[7, 0], x[6, 1], x[5, 2], x[4, 3], x[3, 4], x[2, 5], x[1, 6], x[0, 7],
        x[1, 7], x[2, 6], x[3, 5], x[4, 4], x[5, 3], x[6, 2], x[7, 1],
        x[7, 2], x[6, 3], x[5, 4], x[4, 5], x[3, 6], x[2, 7],
        x[3, 7], x[4, 6], x[5, 5], x[6, 4], x[7, 3],
        x[7, 4], x[6, 5], x[5, 6], x[4, 7],
        x[5, 7], x[6, 6], x[7, 5],
        x[7, 6], x[6, 7],
        x[7, 7]]
    return zig_zag_code


def zig_zag_inv(x):
    '''
    zig_zag_inv(x) -> output\n\n
    This function will reverse the input which encoded by zig-zag scan
    to a 8*8 array.\n
    ## Parameters
    x: The input which encoded by zig-zag scan.\n
    ## Return
    output: The 8*8 array.\n
    '''
    output = [[x[0],  x[2],  x[3],  x[9],  x[10], x[20], x[21], x[35]],
              [x[1],  x[4],  x[8],  x[11], x[19], x[22], x[34], x[36]],
              [x[5],  x[7],  x[12], x[18], x[23], x[33], x[37], x[48]],
              [x[6],  x[13], x[17], x[24], x[32], x[38], x[47], x[49]],
              [x[14], x[16], x[25], x[31], x[39], x[46], x[50], x[57]],
              [x[15], x[26], x[30], x[40], x[45], x[51], x[56], x[58]],
              [x[27], x[29], x[41], x[44], x[52], x[55], x[59], x[62]],
              [x[28], x[42], x[43], x[53], x[54], x[60], x[61], x[63]]]
    return output


def run_len_encode(x):
    '''
    run_len_encode(x) -> [RLcode, RLdata]\n\n
    Run length encode. This method encodes all AC term, and each cell contain
    three information.\n
    ## Parameter
    x: The zig_zag_code.\n
    ## Returns
    RLcode: Run length encode.\n
    RLdata: The data after zero.\n
    '''
    RLcode = []
    RLdata = []
    num_zero = 0
    for i in range(1, 64):
        if i == 63 and x[i] == 0:
            RLcode.append(0)
            RLdata.append(0)
        elif x[i] == 0:
            num_zero += 1
            if num_zero == 15:
                if np.count_nonzero(x[i:]) == 0:
                    RLcode.append(0)
                    RLdata.append(0)
                    return (RLcode, RLdata)
                else:
                    RLcode.append(int(num_zero * 16 + 1))
                    RLdata.append(0)
                    num_zero = 0
        else:
            size = np.floor(np.log2(np.abs(x[i]))) + 1
            RLcode.append(int(num_zero * 16 + size))
            RLdata.append(int(x[i]))
            num_zero = 0
    return (RLcode, RLdata)


def run_len_decode(dc, RLencode, RLdata):
    '''
    run_len_decode(dc, RLencode, RLdata) -> vector\n\n
    Run length decode. This method decodes all the terms using dc and ac
    terms.\n
    ## Parameters
    dc: The DC term.\n
    RLcode: Run length encode.\n
    RLdata: The data after zero.\n
    ## Return
    vector: The vector before run length encode.\n
    '''
    matrix = np.zeros((8, 8))
    for j in range(8):
        for i in range(8):
            if i == 0 and j == 0:
                matrix[0][0] = dc
            else:
                if RLencode[0] == 0:
                    matrix = np.reshape(matrix.T, 64)
                    return matrix
                (value, RLencode, RLdata) = select_val(RLencode, RLdata)
                matrix[i][j] = value
    matrix = np.reshape(matrix.T, 64)
    return matrix


def select_val(RLencode, RLdata):
    '''
    select_val(RLencode, RLdata) -> [value, RLencode, RLdata]\n\n
    This function select the value to fill back the matrix.
    There are three case:
    1. (0, 0, 0):   All value should be 0.
    2. (X, Y, Z): There are X zeros before Z.
    3. (0, Y, Z): Fill Z back.
    ## Parameter
    RLcode: Run length encode.\n
    RLdata: The data after zero.\n
    ## Returns
    value: The value to fill back the matrix.\n
    RLcode: The remain part of run length encode.\n
    RLdata: The remain part of the data after zero.\n
    '''
    if RLencode[0] >= 16:
        value = 0
        RLencode[0] = RLencode[0] - 16
    else:
        value = RLdata[0]
        RLdata = RLdata[1:]
        RLencode = RLencode[1:]
    return (value, RLencode, RLdata)


def encrypt(img, key_img):
    '''
    encrypt(img, key_img) -> [row, DC_matrix, RLencode, RLdata]\n\n
    Encrypt the image.
    ## Parameter
    img: The orignal image\n
    key_img: The key image.\n
    ## Returns
    row: The row of the image.\n
    DC_matrix: The DC terms of the image.\n
    RLencode: Run length encode.\n
    RLdata: The data part of the Run length encode.\n
    '''
    # calculate time
    start = time.process_time_ns()

    # noise
    np.random.seed(rnd_seed)
    noise = np.random.rand(8, 8)
    noise[7, 7] = 0

    # colorspace transform (BGR2YCrCb)
    img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype('float')
    key_img = cv2.cvtColor(key_img, cv2.COLOR_BGR2YCrCb).astype('float')

    (row, col, channel) = img_YUV.shape
    row, col = row // 8 * 8, col // 8 * 8
    img_YUV = cv2.resize(img_YUV, (col, row))
    key_img = cv2.resize(key_img, (col, row))

    RLencode = [[], [], []]
    RLdata = [[], [], []]
    DC_matrix = [[], [], []]

    # slice each part into 8*8 matrix, do dct,quantization,encode
    for i in range(row//8):
        for j in range(col//8):
            for k in range(channel):
                img_downsample = img_YUV[8*i:8*i+8, 8*j:8*j+8, k]
                key_downsample = key_img[8*i:8*i+8, 8*j:8*j+8, k]
                img_dct = cv2.dct(img_downsample)
                key_dct = cv2.dct(key_downsample)
                encrypt_dct = img_dct * 0.1 + key_dct * 0.9
                img_qua = np.round(encrypt_dct / quatization_matrix + noise)
                zig_zag_code = zig_zag(img_qua)
                RLcode, data = run_len_encode(zig_zag_code)
                DC_matrix[k].append(zig_zag_code[0].astype('uint'))
                RLencode[k].append(RLcode)
                RLdata[k].append(data)

    end = time.process_time_ns()
    print("[INFO] Encrypt:", end - start, "ns")
    return (row, DC_matrix, RLencode, RLdata)


def decode(row, DC_matrix, RLencode, RLdata):
    '''
    decode(row, DC_matrix, RLencode, RLdata, key_img) -> result_img\n\n
    Decode the image.
    ## Parameter
    row: The row of the image.\n
    DC_matrix: The DC terms of the image.\n
    RLencode: Run length encode.\n
    RLdata: The data part of the Run length encode.\n
    key_img: The key image.\n
    ## Returns
    result_img: The decoded image\n
    '''
    # calculate time
    start = time.process_time_ns()

    col = len(DC_matrix[0]) // (row // 8) * 8
    channel = 3

    result_img = np.zeros((row, col, channel))

    for k in range(channel):
        DC_cell = np.array(DC_matrix[k])
        AC_cell = np.array(RLencode[k])
        RLdata_cell = np.array(RLdata[k])
        for i in range(row//8):
            for j in range(col//8):
                RLdecode = run_len_decode(
                    DC_cell[i*col//8+j], AC_cell[i*col//8+j],
                    RLdata_cell[i*col//8+j])
                decode_temp = zig_zag_inv(RLdecode)
                decode_temp = decode_temp * quatization_matrix
                result_img[8*i:8*i+8, 8*j:8*j+8, k] = cv2.idct(decode_temp)

    result_img = result_img.astype('uint8')
    result_img = cv2.cvtColor(result_img, cv2.COLOR_YCrCb2BGR)

    end = time.process_time_ns()
    print("[INFO] Decode:", end - start, "ns")
    return result_img


def decrypt(row, DC_matrix, RLencode, RLdata, key_img):
    '''
    decrypt(row, DC_matrix, RLencode, RLdata, key_img) -> recover_img\n\n
    Decrypt the image.
    ## Parameter
    row: The row of the image.\n
    DC_matrix: The DC terms of the image.\n
    RLencode: Run length encode.\n
    RLdata: The data part of the Run length encode.\n
    key_img: The key image.\n
    ## Returns
    recover_img: The decrypt image\n
    '''
    # calculate time
    start = time.process_time_ns()

    col = len(DC_matrix[0]) // (row // 8) * 8
    channel = 3

    # noise
    np.random.seed(rnd_seed)
    noise = np.random.rand(8, 8)
    noise[7, 7] = 0

    key_img = cv2.cvtColor(key_img, cv2.COLOR_BGR2YCrCb).astype('float')
    key_img = cv2.resize(key_img, (col, row))

    recover_img = np.zeros((row, col, channel))

    for k in range(channel):
        DC_cell = np.array(DC_matrix[k])
        AC_cell = np.array(RLencode[k])
        RLdata_cell = np.array(RLdata[k])
        for i in range(row//8):
            for j in range(col//8):
                RLdecode = run_len_decode(
                    DC_cell[i*col//8+j], AC_cell[i*col//8+j],
                    RLdata_cell[i*col//8+j])
                decode_temp = zig_zag_inv(RLdecode)
                key_downsample = key_img[8*i:8*i+8, 8*j:8*j+8, k]
                key_dct = cv2.dct(key_downsample)
                decode_temp = (decode_temp - noise) * quatization_matrix
                recover_img[8*i:8*i+8, 8*j:8*j+8, k] = cv2.idct((
                    decode_temp - 0.9 * key_dct) * 10)

    recover_img = recover_img.astype('uint8')
    recover_img = cv2.cvtColor(recover_img, cv2.COLOR_YCrCb2BGR)

    end = time.process_time_ns()
    print("[INFO] Decrypt:", end - start, "ns")
    return recover_img


if __name__ == "__main__":

    class FiletypeErrorException(Exception):
        '''An exception raises when the filetype is wrong.'''
        def __init__(self, filename):
            Exception.__init__(self)
            self.filename = filename

    parser = argparse.ArgumentParser(description='Encrypt and decrypt the \
                                                  image.')
    parser.add_argument('filepath', metavar='filepath', type=str,
                        help='the path to the orignal image or the encrypted \
                              file.')
    parser.add_argument('key_filepath', type=str,
                        help='the path to the key image')
    parser.add_argument('-d', '--decrypt_mode', action="store_true",
                        help='Decrypt mode.')
    parser.add_argument('-o', '--output_path', type=str, default='',
                        help='Output file path')
    args = parser.parse_args()

    filepath = args.filepath
    key_filepath = args.key_filepath

    if args.decrypt_mode:
        # try to open the file
        try:
            key = cv2.imread(key_filepath)
            if isinstance(key, type(None)):
                raise FiletypeErrorException(key_filepath)
        except FiletypeErrorException as ex:
            print("[ERROR] Cannot open '{0}'. "
                  "It might not be an image file.".format(ex.filename))
            exit(1)
        (row, DC_matrix, RLencode, RLdata) = JEPGIO.read_image_file(filepath)
        recover_img = decrypt(row, DC_matrix, RLencode, RLdata, key)
        cv2.imshow("recover_img", recover_img)
        if args.output_path != '':
            cv2.imwrite(args.output_path, recover_img)
    else:
        # try to open the file
        try:
            img = cv2.imread(filepath)
            if isinstance(img, type(None)):
                raise FiletypeErrorException(filepath)
            key = cv2.imread(key_filepath)
            if isinstance(key, type(None)):
                raise FiletypeErrorException(key_filepath)
        except FiletypeErrorException as ex:
            print("[ERROR] Cannot open '{0}'. "
                  "It might not be an image file.".format(ex.filename))
            exit(1)

        (row, DC_matrix, RLencode, RLdata) = encrypt(img, key)
        result_img = decode(row, DC_matrix, RLencode, RLdata)
        cv2.imshow("orignal_img", img)
        cv2.imshow("result_img", result_img)
        if args.output_path != '':
            JEPGIO.write_to_binstr(args.output_path, row, DC_matrix, RLencode,
                                   RLdata)

    # show the images
    cv2.imshow("key_img", key)
    while True:
        # press 'q' to quit
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
