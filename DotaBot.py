import requests
import json
import pprint

class Dota:

    #Create the empty dictionaries for the separate attributes
    agiHero = {}
    strHero = {}
    intHero = {}
    uniHero = {}

    #function to populate the dictionaries
    def create_attr_dicts(self, api):

        #response object to make request to api
        response = requests.get(f"{api}")

        #if response is 200 (good)
        if response.status_code == 200:
            
            #create data object that corresponds json information
            data = response.json()
            for hero in data:

                hero_name = hero.get('localized_name')
                hero_id = hero.get('id')
                primary_attr = hero.get('primary_attr')

                if hero_name and hero_id is not None:
                    if primary_attr == 'agi':
                        self.agiHero[hero_id] = hero_name
                    if primary_attr == 'str':
                        self.strHero[hero_id] = hero_name
                    if primary_attr == 'int':
                        self.intHero[hero_id] = hero_name
                    if primary_attr == 'all':
                        self.uniHero[hero_id] = hero_name
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")
    
    #print function to print the dictionaries of heroes 
    def printDicts(self):
        
        print("*****AGI HEROES*****")
        print(self.agiHero)
        print('\n')

        print("*****STR HEROES*****")
        print(self.strHero)
        print('\n')

        print("*****INT HEROES*****")
        print(self.intHero)
        print('\n')

        print("*****UNIVERSAL HEROES*****")
        print(self.uniHero)
        print('\n')

    #function to get the win loss ratio on every agi hero 
    #this is a test, to get practice working with the JSON file and extracting information correctly
    def getWinsLossesAgi(self, api):
        
        response = requests.get(f"{api}")

        if response.status_code == 200:
            data = response.json()
            for hero in data:

                hero_id = hero.get('hero_id')
                wins = hero.get('win')
                games = hero.get('games')
                if games != 0:
                    winrate = wins/games
                else:
                    winrate = 0

                if hero_id in self.agiHero:
                    print("Hero name: %s \nGames Played: %d \nWins: %d" % (self.agiHero[hero_id], wins, games))
                    print("Win rate: %.2f\n" % winrate)



    def __init__(self, api):
        self.create_attr_dicts(api)
        #self.printDicts()

        

api_call = Dota("https://api.opendota.com/api/heroes")
api_call.getWinsLossesAgi("https://api.opendota.com/api/players/66957927/heroes")

