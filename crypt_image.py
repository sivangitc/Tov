from PIL import Image
import numpy
import hashlib
from Crypto.Cipher import AES

class CryptImage():

    def __init__(self, image, key_hash):
        self.image = image
        self.key_hash = key_hash

    def encrypt(self, key):
        key = hashlib.sha256(key.encode()).digest()
        self.key_hash = hashlib.sha256(key).digest()
        self.cipher_image("enc", key)

    def decrypt(self, key):
        key = hashlib.sha256(key.encode()).digest()
        if self.key_hash != hashlib.sha256(key).digest():
            return False
        self.key_hash = None
        
        self.cipher_image("dec", key)
        return True

    def show(self):
        self.image.show()

    def image_to_bytes(self):
        """
        PIL image -> list of bytes
        """
        pixels = list(self.image.getdata())
        return bytes(CryptImage.flattenpixels(pixels))
    
    @classmethod
    def image_from_bytes(self, blist, height, width):
        """
        list of bytes -> PIL image
        """
        rebuilded = CryptImage.rebuildspixels(blist)    
        twodpixels = CryptImage.unflattenpixels(rebuilded, height, width)
        array = numpy.array(twodpixels, dtype=numpy.uint8)
        return Image.fromarray(array, mode="RGB")

    @property
    def width(self):
        return self.image.width
    
    @property
    def height(self):
        return self.image.height

    def cipher_image(self, mode, key):
        """
        decrypt/encrypt image with key
        :param mode: dec - decrypt, enc - encrypt
        """
        onedpixels = self.image_to_bytes()

        cipher = AES.new(key, AES.MODE_EAX, nonce=b'arazim')
        if mode == "enc":
            ciphered = list(cipher.encrypt(onedpixels))
        else:
            ciphered = list(cipher.decrypt(onedpixels))
        self.image = self.image_from_bytes(ciphered, self.image.height, self.image.width)

    @classmethod
    def unflattenpixels(self, pixels, height, width):
        """
        1d list of 3tuple representing pixels to 2d
        """
        twodpixels = []
        for row in range(height):
            start_row = row * width
            twodpixels.append(pixels[start_row:start_row + width])
        return twodpixels
    
    @classmethod
    def rebuildspixels(self, pixels):
        """
        from list of numbers to list of 3tuple representing pixels
        """
        new_pixels = []
        for i in range(0, len(pixels), 3):
            new_pixels.append(tuple(pixels[i:i+3]))
        return new_pixels
    
    @classmethod
    def flattenpixels(self, pixels):
        """
        from list of 3tuple to 1d list of numbers
        """
        l = []
        for p in pixels:
            for v in p:
                l.append(v)
        return l

    @classmethod
    def create_from_path(cls, path):
        im = Image.open(path)
        return cls(im, None)
    
    def save_to_path(self, path):
        self.image.save(path)
