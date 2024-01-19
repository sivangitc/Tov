import argparse
import sys
from listener import Listener
import threading
import card

def run_server(server_ip, server_port):
    """
    open server socket and start accepting client requests
    """

    lock = threading.Lock()
    with Listener(server_port, server_ip) as listener:
        while True:
            with listener.accept() as connection:
                t = threading.Thread(target=handle_client, args=(connection, lock))
                t.start()


def handle_client(connection, lock):
    """
    recieve and print message from client
    """
    lock.acquire()
    
    msg = connection.receive_message()
    rec_card = card.Card.deserialize(msg)
    print("Recieved " + repr(rec_card))

    lock.release()


def get_args():
    parser = argparse.ArgumentParser(description='Start server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from client.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
