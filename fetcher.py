import json
import pymongo
import pathlib
import os

class FileSystemDriver():
    def __init__(self, path) -> None:
        path = path.split('://')[1]
        self.path = pathlib.Path(path)
    
    def cards_from_creator(self, creator):
        cards = []
        for filename in os.scandir(self.path):
            print(filename)
            p = self.path / filename
            meta = json.loads(p.read_text())
            if meta['creator'] == creator:
                cards.append(meta)
        return cards

    def get_creators(self):
        creators = []
        for filename in os.scandir(self.path):
            print(filename)
            p = self.path / filename
            meta = json.loads(p.read_text())
            creators.append(meta['creator'])
        return list(set(creators))


class MongoDBDriver():
    def __init__(self, location):
        client = pymongo.MongoClient(location)
        db = client['mydatabase']
        self.col = db['cardazim']
    
    def cards_from_creator(self, creator):
        return list(self.col.find({'creator': creator}, {'_id': 0}))
        

    def get_creators(self):
        return self.col.distinct('creator')


DRIVERS = {'filesystem': FileSystemDriver, 'mongodb': MongoDBDriver}

class Fetcher():
    def __init__(self, url):
        parts = url.split('://')
        if len(parts) != 2:
            raise(Exception("Bad format for driver"))
        self.driver = DRIVERS[parts[0]](url)

    def cards_from_creator(self, creator):
        return self.driver.cards_from_creator(creator)

    def get_creators(self):
        return self.driver.get_creators()
    
    def get_card(self, creator, name):
        possible_cards = self.cards_from_creator(creator)
        for card in possible_cards:
            if card['name'] == name:
                return card
        raise(Exception('Card not found'))