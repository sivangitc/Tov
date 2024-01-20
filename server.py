import argparse
import sys
from listener import Listener
import threading
import card
import pathlib

def run_server(server_ip, server_port, dirpath):
    """
    open server socket and start accepting client requests
    """

    path = pathlib.Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)

    lock = threading.Lock()
    with Listener(server_port, server_ip) as listener:
        while True:
            with listener.accept() as connection:
                t = threading.Thread(target=handle_client, args=(connection, lock, dirpath))
                t.start()


def handle_client(connection, lock, unsolved_dir):
    """
    recieve and print message from client
    """
    lock.acquire()
    
    msg = connection.receive_message()
    save_unsolved(msg, unsolved_dir)
    rec_card = card.Card.deserialize(msg)
    print("Recieved " + repr(rec_card))

    lock.release()

def save_unsolved(card_ser, dirpath):
    i = 0
    dirp = pathlib.Path(dirpath)
    p = dirp / str(i)
    while pathlib.Path.exists(p):
        i += 1
        p = (dirp / str(i))
    
    with open(p, mode='wb') as f:
        f.write(card_ser)


def get_args():
    parser = argparse.ArgumentParser(description='Start server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('unsolved_dir', type=str,
                        help='path to save unsolved cards')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from client.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port, args.unsolved_dir)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
