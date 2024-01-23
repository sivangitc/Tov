import pathlib
import card
import json
import pymongo

class FileSystemDriver():
    def __init__(self, path) -> None:
        path = path.split('://')[1]
        self.path = pathlib.Path(path)

    def save(self, metadata_dict):
        file_name = metadata_dict['name']
        save_path = self.path / f"{file_name}.json"
        with open(save_path, "w") as f:
            f.write(json.dumps(metadata_dict))

class MongoDBDriver():
    def __init__(self, location):
        client = pymongo.MongoClient(location)
        my_db = client['mydatabase']
        self.col = my_db['cardazim']
    
    def save(self, metadata_dict):
        self.col.insert_one(metadata_dict)
        

DRIVERS = {'filesystem': FileSystemDriver, 'mongodb': MongoDBDriver}

class Saver():
    def __init__(self, url, big_data_path) -> None:
        big_data_path = pathlib.Path(big_data_path)
        big_data_path.mkdir(parents=True, exist_ok=True)
        parts = url.split('://')
        if len(parts) != 2:
            raise(Exception("Bad format for driver"))
        self.driver = DRIVERS[parts[0]](url)
        self.big_data_path = big_data_path

    def save(self, solv_card: card.Card):
        metadata_dict = solv_card.parse_card()
        impath = self.big_data_path / f'{solv_card.name}.jpg'
        metadata_dict['image_path'] = str(impath)
        solv_card.save_image_to_path(impath)
        self.driver.save(metadata_dict)
