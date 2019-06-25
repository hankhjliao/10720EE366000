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

3. Decrypt image. Note: It may take at most 5 min to load.
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
   1. Load the image that wants to encrypt
      ![](photo/readme/1.png)
      ![](photo/readme/2.png)
   2. Click on "Encrypt".
      ![](photo/readme/3.png)
   3. Load Key Image.
      ![](photo/readme/4.png)
   4. Show the result.
      ![](photo/readme/5.png)
   5. Save the result.
      ![](photo/readme/6.png)

2. Decrypt Image
   1. Load binary file.  
      (It may take at most 5 min to load)
      ![](photo/readme/1.png)
      ![](photo/readme/7.png)
   1. Click on "Decrypt".
      ![](photo/readme/8.png)
   2. Load Key Image.
      ![](photo/readme/9.png)
   3. Save the result.
      ![](photo/readme/10.png)
