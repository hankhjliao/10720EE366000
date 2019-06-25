# Image Encrypting and Decrypting of JPEG

## Test Environment
1. Ubuntu 19.04 + Python 3.7.3
2. macOS 10.14.5 + Python 3.7.3

## Set up the environment

1. Install pip3.
`$ sudo apt install python3-pip`

2. Install the required packages.
`$ pip3 install -r requirements.txt`

## Usage

### CLI
1. List usage.
`$ python3 JEPGcrypto.py --help`
![](photo/readme/2019-06-25-21-44-43.png)

2. Encrypt image.
`$ python3 JEPGcrypto.py <path/to/orignal_image> <path/to/key_image>`
![](photo/readme/2019-06-25-21-19-10.png)

3. Decrypt image.
`$ python3 JEPGcrypto.py <path/to/orignal_image> <path/to/key_image> -d`
![](photo/readme/2019-06-25-21-47-25.png)

1. Save result.
   - For encrypt mode:
     `$ python3 JEPGcrypto.py <path/to/orignal_image> <path/to/key_image> -o <path/to/result>`
   - For decrypt mode:
     `$ python3 JEPGcrypto.py <path/to/orignal_image> <path/to/key_image> -o <path/to/result> -d`
     ![](photo/readme/2019-06-25-21-46-41.png)

### GUI
`$ python3 gui.py`
1. Encrypt Image
   
2. Decrypt Image
