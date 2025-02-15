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

    def get_heroes_data(self):
        heroes_data = "```"

        heroes_data += "AGI HEROES\n"
        heroes_data += "\n".join([f"{key}: {value}" for key, value in self.agiHero.items()])

        heroes_data += "\n\nSTR HEROES\n"
        heroes_data += "\n".join([f"{key}: {value}" for key, value in self.strHero.items()])

        heroes_data += "\n\nINT HEROES\n"
        heroes_data += "\n".join([f"{key}: {value}" for key, value in self.intHero.items()])

        heroes_data += "\n\nUNIVERSAL HEROES\n"
        heroes_data += "\n".join([f"{key}: {value}" for key, value in self.uniHero.items()])

        heroes_data += "```"
        return heroes_data
    
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


    #next step is to create a function that will get individual win loss information
    #we will use the dictionary we already made and we can use heroID and heroName
    #the user should provide a heroName, and we can then look through the dictionary keys (I guess we need to look through all 4?)
    #once we find it, we can provide relevant information
    #We can use the same API key from the getWinsLosses function
    def getWinsLosses(self, heroName):
        #use the hero name to get the ID
        hero_dicts = [self.agiHero, self.strHero, self.intHero, self.uniHero]
        id = None
        for hero_dict in hero_dicts:
            for hero_id, name in hero_dict.items():
                if name == heroName:
                    id = hero_id
                    break
        if id == None:
            print("Hero not found")
            return
        #have the id, make api call now on that id
        print(f"ID for {heroName} is {id}\n")
        matchup_url = f"https://api.opendota.com/api/players/66957927/heroes"
        response = requests.get(matchup_url)

        if response.status_code == 200:
            data = response.json()
            for matchups in data:
                heroID = matchups.get('hero_id')
                if id == heroID:
                    wins = matchups.get('win')
                    games = matchups.get('games')
                    winrate = wins / games

                    print(f"Hero: {heroName}\nWins: {wins}\nTotal Games Played: {games}\nWinrate: {winrate: .2f}")
        
    def get_winloss_data(self, hero: str)->str:
        hero_dicts = [self.agiHero, self.strHero, self.intHero, self.uniHero]
        id = None
        for hero_dict in hero_dicts:
            for hero_id, name in hero_dict.items():
                if name == hero:
                    id = hero_id
                    break
        if id == None:
            return 'Hero not found'            
        matchup_url = f"https://api.opendota.com/api/players/66957927/heroes"
        response = requests.get(matchup_url)      

        if response.status_code == 200:
            data = response.json()
            for matchups in data:
                heroID = matchups.get('hero_id')
                if id == heroID:
                    wins = matchups.get('win')
                    games = matchups.get('games')
                    winrate = wins / games

                    return f"Hero: {hero}\nWins: {wins}\nTotal Games Played: {games}\nWinrate: {winrate: .2f}"


    def __init__(self, api):
        self.create_attr_dicts(api)
        #self.printDicts()

#api_call = Dota("https://api.opendota.com/api/heroes")
#api_call.getWinsLossesAgi("https://api.opendota.com/api/players/66957927/heroes")
#hero = input("Enter hero: ")
#api_call.getWinsLosses(hero)
