import requests
import json
import pprint

class Dota:

    #Create the empty dictionaries for the separate attributes
    agiHero = dict()
    strHero = dict()
    intHero = dict()
    uniHero = dict()

    #function to populate the dictionaries
    def create_attr_dicts(self, api):

        #response object to make request to api
        response = requests.get(f"{api}")

        #if response is 200 (good)
        if response.status_code == 200:
            
            #create data object that corresponds json information
            data = response.json()
            for hero in data:

                if hero['primary_attr'] == 'agi':
                    self.agiHero[hero['id']] = {"name":hero['localized_name'], "attribute":hero['primary_attr']} 
            
                elif hero['primary_attr'] == 'str':
                    self.strHero[hero['id']] = {"name":hero['localized_name'], "attribute":hero['primary_attr']} 

                elif hero['primary_attr'] == 'int':
                    self.intHero[hero['id']] = {"name":hero['localized_name'], "attribute":hero['primary_attr']} 

                elif hero['primary_attr'] == 'all':
                    self.uniHero[hero['id']] = {"name":hero['localized_name'], "attribute":hero['primary_attr']} 

        else:
            print(f"Hello person, there's a {response.status_code} error with your request")
    
    #print function to print the dictionaries of heroes 
    def printDicts(self):
        
        print("*****AGI HEROES*****")
        pprint.pprint(list(self.agiHero.items()))
        print('\n')

        print("*****STR HEROES*****")
        pprint.pprint(list(self.strHero.items()))
        print('\n')

        print("*****INT HEROES*****")
        pprint.pprint(list(self.intHero.items()))
        print('\n')

        print("*****UNIVERSAL HEROES*****")
        pprint.pprint(list(self.uniHero.items()))
        print('\n')

        print(self.agiHero[1].get('name'))

    def getWinsLossesAgi(self, api):
        response = requests.get(f"{api}")

        if response.status_code == 200:
            data = response.json()
            for hero in data:

                if hero['hero_id'] in self.agiHero.keys():
                    print("Hero name: %s \nGames Played: %s \nWins: %s\n" % (self.agiHero[int(hero['hero_id'])].get('name'), hero['games'], hero['win']))



    def __init__(self, api):
        self.create_attr_dicts(api)
        # self.printDicts()

        

api_call = Dota("https://api.opendota.com/api/heroes")
api_call.getWinsLossesAgi("https://api.opendota.com/api/players/66957927/heroes")

