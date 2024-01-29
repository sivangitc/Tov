import flask
import server
import fetcher
import json

app = flask.Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000
SOLVED_URL = 'filesystem:///home/user/Desktop/solved'
SOLVED_URL = 'mongodb://127.0.0.1:27017'
#UNSOLVED_PATH = '/home/user/Desktop/unsolved'
fet = fetcher.Fetcher(SOLVED_URL)

@app.route('/creators')
def get_creators():
    # return list of creators
    return fet.get_creators()


@app.route('/creators/<creator>')
def get_creator_cards(creator):
    # return all cards from <creator>
    return fet.cards_from_creator(creator)


@app.route('/creators/<creator>/cards/<cardname>')
def get_card(creator, cardname):
    # get card
    possible_cards = get_creator_cards(creator)
    for card in possible_cards:
        if card['name'] == cardname:
            return json.dumps(card)
    raise(Exception('Card not found'))


@app.route('/creators/<creator>/cards/<cardname>/image.jpg')
def get_image(creator, cardname):
    # get image of a card
    card_dict = json.loads(get_card(creator, cardname))
    impath = card_dict['image_path'].split('/')    
    return flask.send_from_directory('/'.join(impath[:-1]), impath[-1], as_attachment=False)


def run_api_server(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    run_api_server(HOST, PORT)