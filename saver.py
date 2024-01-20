import pathlib
import card
import json
from PIL import Image

class Saver():
    @classmethod
    def save(self, solv_card: card.Card, dir_path='.'):
        path = pathlib.Path(dir_path) / solv_card.name
        path.mkdir(parents=True, exist_ok=True)

        image_path = path / 'image.jpg'
        solv_card.image.image.save(image_path)
        propdict = {'name':solv_card.name, 'creator': solv_card.creator, 'riddle': solv_card.riddle, \
                    'solution': solv_card.solution, 'image_path': str(image_path)}
        json_path = path / 'metadata.json'
        with open(json_path, mode='w') as f:
            f.write(json.dumps(propdict))
