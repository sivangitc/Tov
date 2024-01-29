import flask
import fetcher
import json
import argparse

app = flask.Flask(__name__)
HOST = '127.0.0.1'
PORT = 5001
fet = None

@app.route('/')
@app.route('/creators')
def get_creators():
    # return list of creators
    return flask.render_template('creators.html', creators=fet.get_creators())


@app.route('/creators/<creator_name>')
def get_creator_cards(creator_name):
    # return all cards from <creator>
    cards_dict = fet.cards_from_creator(creator_name)
    card_names = [card['name'] for card in cards_dict]
    return flask.render_template('cards.html', creator=creator_name, cards=card_names)


@app.route('/creators/<creator>/cards/<cardname>')
def get_card(creator, cardname):
    # get card
    card = fet.get_card(creator, cardname)
    return flask.render_template('card.html', name=card['name'], creator=card['creator'], \
                                    riddle=card['riddle'], solution=card['solution'])
    #return json.dumps(card)


@app.route('/creators/<creator>/cards/<cardname>/image.jpg')
def get_image(creator, cardname):
    # get image of a card
    card_dict = fet.get_card(creator, cardname)
    impath = card_dict['image_path'].split('/')    
    return flask.send_from_directory('/'.join(impath[:-1]), impath[-1], as_attachment=False)


def get_args():
    parser = argparse.ArgumentParser(description='Start API')
    parser.add_argument('database_url', type=str,
                        help='where to save solved')
    return parser.parse_args()

def run_api_server(host, port, database_url='mongodb://127.0.0.1:27017'):
    global fet
    fet = fetcher.Fetcher(database_url)
    app.run(host=host, port=port)


if __name__ == '__main__':
    db_url = get_args().database_url
    run_api_server(HOST, PORT, db_url)
