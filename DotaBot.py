import requests
import json
import pprint

class Dota:

    #Create the empty dictionaries for the separate attributes
    agiHero = dict()
    strHero = dict()
    intHero = dict()
    uniHero = dict()
    count = 0

    #function to populate the dictionaries
    def create_attr_dicts(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            #print("successfully fetched the data")
            data = response.json()
            for hero in data:

                if hero['primary_attr'] == 'agi':
                    self.agiHero[self.count] = [[hero['id']], [[hero['localized_name']], [hero['primary_attr']]]]
                    self.count = self.count+1
            
                elif hero['primary_attr'] == 'str':
                    self.strHero[self.count] = [[hero['id']], [[hero['localized_name']], [hero['primary_attr']]]]
                    self.count = self.count+1

                elif hero['primary_attr'] == 'int':
                    self.intHero[self.count] = [[hero['id']], [[hero['localized_name']], [hero['primary_attr']]]]
                    self.count = self.count+1

                elif hero['primary_attr'] == 'all':
                    self.uniHero[self.count] = [[hero['id']], [[hero['localized_name']], [hero['primary_attr']]]]
                    self.count = self.count+1
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")
    
    def printDicts(self):
        
        print("*****AGI HEROES*****")
        pprint.pprint(list(self.agiHero.values()))
        print('\n')

        print("*****STR HEROES*****")
        pprint.pprint(list(self.strHero.values()))
        print('\n')

        print("*****INT HEROES*****")
        pprint.pprint(list(self.intHero.values()))
        print('\n')

        print("*****UNIVERSAL HEROES*****")
        pprint.pprint(list(self.uniHero.values()))
        print('\n')


    def __init__(self, api):
        self.create_attr_dicts(api)
        # self.printDicts()

        

api_call = Dota("https://api.opendota.com/api/heroes")
api_call.printDicts()
