import argparse
import sys
from connection import Connection
import card

SERVER_IP = "10.100.102.76"
SERVER_PORT = 5000

###########################################################
####################### YOUR CODE #########################
###########################################################

def send_data(name, creator, riddle, solution, path):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    mycard = card.Card.create_from_path(name, creator, riddle, solution, path)
    mycard.image.encrypt(solution)
    ser = mycard.serialize()

    with Connection.connect(SERVER_IP, SERVER_PORT) as con:
        con.send_message(ser)
        print("Sending " + repr(mycard))
    

###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('name', type=str,
                        help='the name of the cardaz')
    parser.add_argument('creator', type=str,
                        help='the creator of the cardaz')
    parser.add_argument('riddle', type=str,
                        help='the riddle of the cardaz')
    parser.add_argument('solution', type=str,
                        help='the solution of the cardaz')
    parser.add_argument('path', type=str,
                        help='the path for the cardaz picture')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.name, args.creator, args.riddle, args.solution, args.path)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
