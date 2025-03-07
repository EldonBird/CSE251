"""
Course: CSE 251 
Lesson: L02 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Make threaded API calls with the Playing Card API http://deckofcardsapi.com

Instructions:

- Review instructions in Canvas.
"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_Thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        # threading.Thread.__init__(self)
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = 0

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        self.status_code = response.status_code
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle

        r = Request_Thread(rf'https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/')
        r.start()
        r.join()




    def draw_card(self):
        # TODO add call to get a card

        r = Request_Thread(rf'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
        r.start()
        r.join()

        if(r.status_code == 200):
            self.remaining = r.response["remaining"]
            return r.response['cards'][0]['code']



    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '1ccuymn2vy3j'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<
