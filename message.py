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
    (slen,) = struct.unpack("I", packed[:4])
    (msg,) = struct.unpack("%ds" % slen, packed[4:])
    msg = msg.decode()
    return msg
