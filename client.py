import argparse
import sys
import socket
import struct


###########################################################
####################### YOUR CODE #########################
###########################################################

def pack_msg(msg):
    """
    prepare msg to send in format <length:msg>
    """
    msgb = msg.encode()
    packed = struct.pack("<I%ds" % len(msgb), len(msgb), msgb)
    return packed


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''

    sock = socket.socket()
    sock.connect((server_ip, server_port))

    packed = pack_msg(data)
    sock.send(packed)
    sock.close()

    print("sending data:")
    print(data)
    

###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
