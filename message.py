import struct

def pack_msg(msg):
    """
    prepare msg to send in format <length:msg>
    """
    msgb = msg.encode()
    packed = struct.pack("<I%ds" % len(msgb), len(msgb), msgb)
    return packed


def unpack_msg(packed):
    """
    parse byted message in format <length,msg>
    """
    return unpack_str(packed)[0]

def unpack_str(packed):
    (slen,) = struct.unpack("I", packed[:4])
    (msg,) = struct.unpack("%ds" % slen, packed[4:4 + slen])
    return msg.decode(), packed[4 + slen:]

def unpack_serialized(packed):
    name, packed = unpack_str(packed)
    creator, packed = unpack_str(packed)

    height, width = struct.unpack("II", packed[:8])
    packed = packed[8:]
    
    img_size = 3 * height * width
    (img,) = struct.unpack("%ds" % img_size, packed[:img_size])
    packed = packed[img_size:]

    (key_hash,) = struct.unpack("32s", packed[:32])
    packed = packed[32:]
    
    riddle, packed = unpack_str(packed)

    return name, creator, height, width, img, key_hash, riddle