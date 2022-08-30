#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import json, os

def create_json():
    '''
    Creates a JSON file named games.json if it doesn't exist already. 
    '''
    try:
        my_file = open(os.path.join('Assets','games.json'), 'r')
        game = json.loads(my_file.read())
        my_file.close()

        return game
    except FileNotFoundError:
        data = {"Games": [{"Player_Name": "Boy Wonder", "Player_Level" : 0, "Player_Life_amount" : "9"}]}

        my_file = open(os.path.join('Assets','games.json'), 'w')
        my_file.write(json.dumps(data, indent = 4))
        my_file.close()

        return {}