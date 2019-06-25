import base64
import cv2
import JEPGcrypto
import JEPGIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys


class FiletypeErrorException(Exception):
    '''An exception raises when the filetype is wrong.'''
    def __init__(self, filename):
        Exception.__init__(self)
        self.filename = filename


class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()
        self.title = "JPEG Encrypt & Decrypt"
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.imagePath = ''
        self.keyImagePath = ''
        self.encryptMessage = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(self)
        self.image = QPixmap()
        self.image.loadFromData(base64.b64decode('/9j/4AAQSkZJRgABAQAAAQABAAD//gA+Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2NjIpLCBkZWZhdWx0IHF1YWxpdHkK/9sAQwAIBgYHBgUIBwcHCQkICgwUDQwLCwwZEhMPFB0aHx4dGhwcICQuJyAiLCMcHCg3KSwwMTQ0NB8nOT04MjwuMzQy/9sAQwEJCQkMCwwYDQ0YMiEcITIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy/8AAEQgB9AH0AwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A9/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKSloAKKSigBaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKSloAKKKKACiiigAooooAKKKKACiiigBKWiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooASloooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKRmCjmoWkLewoAlLqOpppl9BUVFAD/ADW9BR5re1MooAkEp7inCVT14qGigCyCD0oqsCQeDUqy54bigCSiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKa7hR70M20ZqAkk5NAASScmiijvzQAAEngU8RHucVIu3b8vSnUAR+UvqaXyl96fRQBGYvQ0woy9qnooArUVM0YbkcGoSCDg0APR9vB6VN1qtT43wdp6UATUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU1zhSaAIpGy3sKbRQBkgUAHbNFT7Rt29qhZSpoAFYqfapwQwyKr0qsVNAFiikBBGRS0AFFFFABTXXcPenUUAVjxxRUkq/xfnUdAE6NuX3p1QRnDY9anoAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKSloAKKSigBaSlooAKKKKACiiigAooooAKKSloAKKKKACiiigAooooAKKKKACopT0FS1DL978KAI6kiHJNR1NF938aAJKQgEYNLRQBXZSppKsEAjBqBlKn2oAFYqfapwQRkVWpysVPtQBYopAQRkUtABRRRQAhGVIqvVmq7cOfrQAg4OasVWqwv3B9KAFpaKKACikpaACiiigAooooAKKKKACiiigApKWigApKWigAooooASlpKWgAooooAKKKKAEpaKKACiiigBKWiigBKWiigAooooAKKKKAEpaKKACiiigAooooAKKKKACiiigAqGX79TVDKORQBHU8f3KhqWI8EUASUUUUAFIQCMGlooArspU+1JVggEYNQMpU0ACsVNTggjIqvSqxU+1AFiikBBGRS0AFV3++asVWPJJoAKnT7gqCrAGFAoAWiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKjlGVz6VJSEZGKAK9OQ4b600jBxRQBZopiNuHvT6ACiiigApCARg0tFAFdlKmkqwQCMGoGUqfagAVipqcEEZFV6VWKmgCWQ4X61DTnbcfam0AKoywFWKiiXvUtABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEcq/xD8aiqzUDptOR0oAaCVORU6sGFQUA4ORQBZoqNZf71PBB6GgBaKKKACkIDDBpaaXUd80AQspU0lOZy30ptABSgbjik6nHep0XaPegBQMDApaKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACjrRRQBC8eOR0plWaY0Yb2NAENFOMbD3pvSgBQ7DuaXe3rTaKAAknqaKKUKT0FACUoBY4Ap6xf3jUgAAwBQAiIF+tOoooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKTGe1LRQA3Yv90UbF9KdRQAgUDoBS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAIzKgyzBR6k4oBDDKkEHuKx/ELFoLe3B5llH+f1FGgTEQzWkh+eBz+X/680Aa4dWYqGBI6gHpTqw9DZWN9eyEKrP949hyf61M3iCzD8LMyZxvCcUAa1MeSOPHmOq5OBuOMmiORJolkjYMjDII71nan9jnvLa2uBKZCcps6c+v5UAalFZ8usWsM0sTlw0fXjqfQUyLXbOWORiXTZ/Cw5P0xQBp0VQstWt76Voow6uozhxjIp13qltZv5bszSf3EGTQBdoqhZatBezmFI5VcDJDqBTLjWrSCUxDfK46iMZxQBpUVTstSgv1dot67Mbt4xj/ADiq8mvWiOQqyyKpwXRflFAGpRTIZUniWWNtyMMg0+gAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDEv8A9/4hsoeojG8/z/oKr6iTp2rPOvCTxN+eP8cfnWwthGNSa9LsXK7dp6Ci/wBPi1CJUkZl2nIZetAHPTboPDtug4E0hZv6fyFbN+sFpockYC7PL2qPU9j/AFqxJp0Etglo4JRAAD3BHeqkegwhl86eaZE+6jHgUAS6Gjx6TEG4zkgexNUx/pHionqIE/p/ia3AAAABgDoKpw6bHBc3E4kcvNnJP8OfSgDO0SNbm+u71hk7yEJ7Zyf8KTTIkudbvbkqCI3IX6k9f0rVsLGOwgMUbMwLbiW60lhYR2COqOzl23Et1oAyon/4nuoXKjiGNvzAA/oak0FI/s81/MwMjMdzt2Her9rpsVq1w25nM5y278f8arRaDbxyE+bK0ROfKJ4P19aAMuCdjDql8mQzYVT6Bj/+qtLSxDY6J9p4yylmb1PYVMtlaafZzrNITDKfnLe/0rGu4dOt7dlt7h7iR+ETOQue/HegAhLw+HbiUZ3TS7Sfb/OatwWepTacluhtord1HI5JBrRtdPQaRHaTrkFfmHoSc1XTQUUbPtlx5X9wNgUAaFpbLaWkcCkkIOp71PRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFADJIo5kKSIrqezDIqKKxtYH3xW8at6heasUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH//2Q=='))
        self.label.setPixmap(self.image.scaled(640, 480, Qt.KeepAspectRatio))
        horizontalLayout = QHBoxLayout()
        self.loadButton = QPushButton("Load")
        horizontalLayout.addWidget(self.loadButton)
        self.encryptButton = QPushButton("Encrypt")
        horizontalLayout.addWidget(self.encryptButton)
        self.decryptButton = QPushButton("Decrypt")
        horizontalLayout.addWidget(self.decryptButton)
        self.saveButton = QPushButton("Save")
        horizontalLayout.addWidget(self.saveButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label)
        mainLayout.addStretch()
        mainLayout.addLayout(horizontalLayout)

        self.loadButton.clicked.connect(self.loadImage)
        self.encryptButton.clicked.connect(self.encryptImage)
        self.decryptButton.clicked.connect(self.decryptImage)
        self.saveButton.clicked.connect(self.saveImage)

        self.loadButton.setEnabled(True)
        self.encryptButton.setEnabled(False)
        self.decryptButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        self.setLayout(mainLayout)
        self.show()

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, ext = QFileDialog.getOpenFileName(
                        self, "Load", "",
                        "TIFF File(*.tiff);;Binary File(*.bin)",
                        options=options)
        if fileName:
            if ext == 'Binary File(*.bin)':
                self.bin = JEPGIO.read_image_file(fileName)
                row, DC_matrix, RLencode, RLdata = self.bin
                self.resultImg = JEPGcrypto.decode(row, DC_matrix, RLencode,
                                                   RLdata)
                self.updateImage('decode')
                self.loadButton.setEnabled(True)
                self.encryptButton.setEnabled(False)
                self.decryptButton.setEnabled(True)
                self.saveButton.setEnabled(False)
            else:
                try:
                    img = cv2.imread(fileName)
                    if isinstance(img, type(None)):
                        raise FiletypeErrorException(self.imagePath)
                except FiletypeErrorException as ex:
                    print("[ERROR] Cannot open '{0}'. "
                          "It might not be an image file.".format(ex.filename))
                    exit(1)
                self.imagePath = fileName
                self.updateImage('file')
                self.loadButton.setEnabled(True)
                self.encryptButton.setEnabled(True)
                self.decryptButton.setEnabled(False)
                self.saveButton.setEnabled(False)
        print("[INFO] Opened:", fileName)

    def updateImage(self, src):
        if src == 'file':
            self.label.setPixmap(QPixmap(self.imagePath).scaled(500, 500,
                                 Qt.KeepAspectRatio))
        elif src == 'decrypt':
            rgbImage = cv2.cvtColor(self.decryptImg, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1],
                                       rgbImage.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(convertToQtFormat).scaled(
                                 500, 500, Qt.KeepAspectRatio))
        elif src == 'decode':
            rgbImage = cv2.cvtColor(self.resultImg, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1],
                                       rgbImage.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(convertToQtFormat).scaled(
                                 500, 500, Qt.KeepAspectRatio))

    def encryptImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
                      self, "Load Key Image", "", "TIFF File(*.tiff)",
                      options=options)
        if fileName:
            self.keyImagePath = fileName
            try:
                img = cv2.imread(self.imagePath)
                if isinstance(img, type(None)):
                    raise FiletypeErrorException(self.imagePath)
                key = cv2.imread(self.keyImagePath)
                if isinstance(key, type(None)):
                    raise FiletypeErrorException(self.keyImagePath)
            except FiletypeErrorException as ex:
                print("[ERROR] Cannot open '{0}'. "
                      "It might not be an image file.".format(ex.filename))
                exit(1)
            self.encryptMessage = JEPGcrypto.encrypt(img, key)
            row, DC_matrix, RLencode, RLdata = self.encryptMessage
            self.resultImg = JEPGcrypto.decode(row, DC_matrix, RLencode,
                                               RLdata)
            self.updateImage('decode')
            self.loadButton.setEnabled(True)
            self.encryptButton.setEnabled(True)
            self.decryptButton.setEnabled(False)
            self.saveButton.setEnabled(True)
        print("[INFO] Encrypted using", fileName)

    def decryptImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
                      self, "Load Key Image", "", "TIFF Files(*.tiff)",
                      options=options)
        if fileName:
            self.keyImagePath = fileName
            try:
                key = cv2.imread(self.keyImagePath)
                if isinstance(key, type(None)):
                    raise FiletypeErrorException(self.keyImagePath)
            except FiletypeErrorException as ex:
                print("[ERROR] Cannot open '{0}'. "
                      "It might not be an image file.".format(ex.filename))
                exit(1)
            row, DC_matrix, RLencode, RLdata = self.bin
            self.decryptImg = JEPGcrypto.decrypt(row, DC_matrix, RLencode,
                                                 RLdata, key)
            self.encryptButton.setEnabled(False)
            self.decryptButton.setEnabled(True)
            self.saveButton.setEnabled(True)
            self.updateImage('decrypt')
        print("[INFO] Decrypted using", fileName)

    def saveImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if self.encryptButton.isEnabled():
            fileName, _ = QFileDialog.getSaveFileName(
                          self, "Save Binary File", "", "Binary File(*.bin)",
                          options=options)
            if fileName:
                if fileName[-4:] != '.bin':
                    fileName = fileName + '.bin'
                row, DC_matrix, RLencode, RLdata = self.encryptMessage
                JEPGIO.write_to_binstr(fileName, row, DC_matrix, RLencode,
                                       RLdata)

        elif self.decryptButton.isEnabled():
            fileName, _ = QFileDialog.getSaveFileName(
                          self, "Save Image", "", "TIFF File(*.tiff)",
                          options=options)
            if fileName:
                if fileName[-5:] != '.tiff':
                    fileName = fileName + '.tiff'
                cv2.imwrite(fileName, self.decryptImg)

        print("[INFO] Saved:", fileName)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
