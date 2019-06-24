import numpy as np
import cv2
import sys
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
    run_len_encode(x) -> [num, size, val]\n\n
    Run length encode. This method encodes all AC term, and each cell contain
    three information.\n
    (0,0) represents the array contains 0 to the end of `8*8 - 1` matrix
    (without DC).\n
    ## Parameter
    x: The zig_zag_code.\n
    ## Returns
    num: Number of zeros before this nonzero element.\n
    size: Number of bits needed to represent element value.\n
    val: Actual value of the element.\n
    '''
    RLcode = []
    num_zero = 0
    for i in range(1, 64):
        if i == 63 and x[i] == 0:
            RLcode.append([0, 0])
        elif x[i] == 0:
            num_zero += 1
        else:
            size = np.floor(np.log2(np.abs(x[i]))) + 1
            RLcode.append([num_zero, size, x[i]])
            num_zero = 0
    return RLcode


def run_len_decode(dc, ac):
    '''
    run_len_decode(x) -> matrix\n\n
    Run length decode. This method decodes all the terms using dc and ac
    terms.\n
    ## Parameters
    dc: The DC term.\n
    ac: The AC term array.\n
    ## Return
    matrix: The matrix before run length encode.\n
    '''
    matrix = np.zeros((8, 8))
    for j in range(8):
        for i in range(8):
            if i == 0 and j == 0:
                matrix[0][0] = dc
            else:
                (value, ac) = select_val(ac)
                matrix[i][j] = value
    matrix = np.reshape(matrix.T, 64)
    return matrix


def select_val(ac):
    '''
    select_val(ac) -> [value, ac]\n\n
    This function select the value to fill back the matrix.
    There are three case:
    1. (0,0):   All value should be 0.
    2. (X,Y,Z): There are X zeros before Z.
    3. (0,Y,Z): Fill Z back.

    ## Parameter
    ac: The AC term array.\n
    ## Returns
    value: The value to fill back the matrix.\n
    ac: The remain AC term array.\n
    '''
    if ac[0][0] == 0 and ac[0][1] == 0:
        value = 0
    else:
        if ac[0][0] > 0:
            value = 0
            ac[0][0] = ac[0][0] - 1
        else:
            value = ac[0][2]
            ac = ac[1:]
    return (value, ac)


def encrypt(img, key_img):
    # TODO output bin file
    start = time.process_time_ns()

    np.random.seed(rnd_seed)
    noise = np.random.rand(8, 8)
    noise[7, 7] = 0

    # colorspace transform (BGR2YCrCb)
    img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype('float')
    key_img = cv2.cvtColor(key_img, cv2.COLOR_BGR2YCrCb).astype('float')

    (row, col, channel) = img_YUV.shape
    key_img = cv2.resize(key_img, (col, row))
    RLencode = [[], [], []]
    DC_matrix = [[], [], []]

    # key_YUV = cv2.resize(key_YUV, (row, col))

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
                # zig_zag_code = zig_zag(img_qua)
                img_qua = np.reshape(img_qua, 64)
                RLcode = run_len_encode(img_qua)
                DC_matrix[k].append(img_qua[0])
                RLencode[k].append(RLcode)

    end = time.process_time_ns()
    print("[INFO] Encrypt:", end - start, "ns")
    return (row, col, channel, DC_matrix, RLencode)


def decrypt(row, col, channel, DC_matrix, RLencode, key_img):
    # TODO input bin file
    start = time.process_time_ns()

    np.random.seed(rnd_seed)
    noise = np.random.rand(8, 8)
    noise[7, 7] = 0

    key_img = cv2.cvtColor(key_img, cv2.COLOR_BGR2YCrCb).astype('float')
    key_img = cv2.resize(key_img, (col, row))

    recover_img = np.zeros((row, col, channel))

    for k in range(channel):
        DC_cell = np.array(DC_matrix[k])
        AC_cell = np.array(RLencode[k])
        for i in range(row//8):
            for j in range(col//8):
                RLdecode = run_len_decode(
                    DC_cell[i*col//8+j], AC_cell[i*col//8+j])
                # decode_temp = zig_zag_inv(RLdecode)
                key_downsample = key_img[8*i:8*i+8, 8*j:8*j+8, k]
                key_dct = cv2.dct(key_downsample)
                decode_temp = np.reshape(RLdecode, (8, 8))
                decode_temp = (decode_temp - noise) * quatization_matrix
                recover_img[8*i:8*i+8, 8*j:8*j+8, k] = cv2.idct(
                    decode_temp - 0.9 * key_dct) * 10

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

    # get the file path
    if len(sys.argv) == 1:
        print("[ERROR] Please input the path to the file.")
        exit(1)
    else:
        filepath = sys.argv[1]
        key_filepath = sys.argv[2]

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

    (row, col, channel, DC_matrix, RLencode) = encrypt(img, key)
    recover_img = decrypt(row, col, channel, DC_matrix, RLencode, key)

    # show the images
    cv2.imshow("ori_img", img)
    cv2.imshow("recover_img", recover_img)
    while True:
        # press 'q' to quit
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
