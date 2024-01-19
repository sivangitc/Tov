import crypt_image
import struct
import message

class Card:
    def __init__(self, name, creator, riddle, solution, image):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        #return f"{self.name} {self.creator} {self.riddle} {self.solution} {self.image}"
        return f"<Card name={self.name}, creator={self.creator}>"
    
    def __str__(self):
        sol_string = self.solution if self.solution else "unsolved"
        return f"Card {self.name} by {self.creator}\nriddle: {self.riddle}\nsolution: {sol_string}"

    @classmethod
    def create_from_path(cls, name, creator, riddle, solution, path):
        # to complete
        image = crypt_image.CryptImage.create_from_path(path)
        return cls(name=name, creator=creator, image=image, riddle=riddle, solution=solution)

    def serialize(self):
        nameb = self.name.encode()
        creatorb = self.creator.encode()
        riddleb = self.riddle.encode()
        
        print(self.image.height, self.image.width)

        # ¿Ser o no ser?
        ser = struct.pack(f"<I{len(nameb)}sI{len(creatorb)}sII{3 * self.image.width * self.image.height}s32sI{len(riddleb)}s", \
                          len(nameb), nameb, \
                          len(creatorb), creatorb, \
                          self.image.height, self.image.width, self.image.image_to_bytes(), self.image.key_hash, \
                          len(riddleb), riddleb)
        return ser
    
    @classmethod
    def deserialize(cls, ser):
        name, creator, height, width, imb, key_hash, riddle = message.unpack_serialized(ser)
        image = crypt_image.CryptImage.image_from_bytes(imb, height, width) # this is a PIL image
        image = crypt_image.CryptImage(image, key_hash) # this is a CryptImage
        return cls(name=name, creator=creator, image=image, riddle=riddle, solution=None)

