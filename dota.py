"""Class for the DotaBot backend functionality.

DotaBot is meant to provide the user with the ability
to obtain data with their accountID. At this point this
includes: 

    Creating dictionaries for each type of hero attribute
    Printing out every hero with ID per each hero attribute
    Getting Win/Loss and Winrate information on unique heroes
"""

import requests


class Dota:
    """This class contains methods and attributes with relevant hero and user information.

    Functions:
    create_attr_dicts(self, api)
    printDicts(self)
    get_heroes_data(self)
    getWinsLossesAgi(self, api)
    getWinsLosses(self, heroName)
    get_winloss_data(self, hero)

    Attributes:
    Dictionaries for agility, strength, intelligence, and universal heroes

    """

    # Create the empty dictionaries for the separate attributes
    agiHero = {}
    strHero = {}
    intHero = {}
    uniHero = {}

    # function to populate the dictionaries
    def create_attr_dicts(self, api):
        """Function creating the hero dictionaries"""

        # response object to make request to api
        response = requests.get(f"{api}", timeout=20)

        # if response is 200 (good)
        if response.status_code == 200:

            # create data object that corresponds json information
            data = response.json()
            for hero in data:

                hero_name = hero.get("localized_name")
                hero_id = hero.get("id")
                primary_attr = hero.get("primary_attr")

                if hero_name and hero_id is not None:
                    if primary_attr == "agi":
                        self.agiHero[hero_id] = hero_name
                    if primary_attr == "str":
                        self.strHero[hero_id] = hero_name
                    if primary_attr == "int":
                        self.intHero[hero_id] = hero_name
                    if primary_attr == "all":
                        self.uniHero[hero_id] = hero_name
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request"
            )

    # print function to print the dictionaries of heroes
    def print_dicts(self):
        """Function to print all of the dictionaries for each hero attribute.

        Takes in https://api.opendota.com/api/heroes in method signature
        Void return value.

        """

        print("*****AGI HEROES*****")
        print(self.agiHero)
        print("\n")

        print("*****STR HEROES*****")
        print(self.strHero)
        print("\n")

        print("*****INT HEROES*****")
        print(self.intHero)
        print("\n")

        print("*****UNIVERSAL HEROES*****")
        print(self.uniHero)
        print("\n")

    # function to get the win loss ratio on every agi hero
    # this is a test, to get practice working with the JSON file
    # and extracting information correctly

    def get_heroes_data(self) -> str:
        """This function gets ALL hero data organized by attribute,
        and is returned to the DotaBot.

        Return value: String
        Function arguement: Self

        """
        heroes_data = "```"

        heroes_data += "AGI HEROES\n"
        heroes_data += "\n".join(
            [f"{key}: {value}" for key, value in self.agiHero.items()]
        )

        heroes_data += "\n\nSTR HEROES\n"
        heroes_data += "\n".join(
            [f"{key}: {value}" for key, value in self.strHero.items()]
        )

        heroes_data += "\n\nINT HEROES\n"
        heroes_data += "\n".join(
            [f"{key}: {value}" for key, value in self.intHero.items()]
        )

        heroes_data += "\n\nUNIVERSAL HEROES\n"
        heroes_data += "\n".join(
            [f"{key}: {value}" for key, value in self.uniHero.items()]
        )

        heroes_data += "```"
        return heroes_data

    def get_wins_losses_agi(self, api):
        """This was a test function to get the win/loss for every agility hero.

        Return value: void
        Arguements: self, api

        """

        response = requests.get(f"{api}", timeout=10)

        if response.status_code == 200:
            data = response.json()
            for hero in data:

                hero_id = hero.get("hero_id")
                wins = hero.get("win")
                games = hero.get("games")
                if games != 0:
                    winrate = wins / games
                else:
                    winrate = 0

                if hero_id in self.agiHero:
                    print(
                        f"Hero name: {self.agiHero[hero_id]} \nGames Played: {wins} \nWins: {games}"
                    )
                    print(f"Win rate: {winrate: %.2f}\n")

    def get_wins_losses(self, hero_name):
        """Function to get the wins and losses on an individual hero.

        A search is performed on the values in all the dictionaries.
        If found, an ID is set and used to get win/loss data.
        If not found, error message reported.

        Return value: void
        Function Arguements: Self, hero_name provided by the user

        """
        # use the hero name to get the ID
        hero_dicts = [self.agiHero, self.strHero, self.intHero, self.uniHero]
        ID = None
        for hero_dict in hero_dicts:
            for hero_id, name in hero_dict.items():
                if name == hero_name:
                    ID = hero_id
                    break
        if ID is None:
            print("Hero not found")
            return
        # have the id, make api call now on that id
        print(f"ID for {hero_name} is {ID}\n")
        matchup_url = "https://api.opendota.com/api/players/66957927/heroes"
        response = requests.get(matchup_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            for matchups in data:
                hero_id = matchups.get("hero_id")
                if ID == hero_id:
                    wins = matchups.get("win")
                    games = matchups.get("games")
                    winrate = wins / games

                    print(
                        f"Hero: {hero_name}\nWins: {wins}\nTotal Games Played: {games}\nWinrate: {winrate: .2f}"
                    )

    def get_winloss_data(self, hero: str) -> str:
        """Gets win loss data for the dota bot and gives it back to the user in the discord."""

        hero_dicts = [self.agiHero, self.strHero, self.intHero, self.uniHero]
        ID = None
        for hero_dict in hero_dicts:
            for hero_id, name in hero_dict.items():
                if name == hero:
                    ID = hero_id
                    break
        if ID is None:
            return "Hero not found"
        matchup_url = "https://api.opendota.com/api/players/66957927/heroes"
        response = requests.get(matchup_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            for matchups in data:
                hero_id = matchups.get("hero_id")
                if ID == hero_id:
                    wins = matchups.get("win")
                    games = matchups.get("games")
                    winrate = wins / games

                    return f"Hero: {hero}\nWins: {wins}\nTotal Games Played: {games}\nWinrate: {winrate: .2f}"

    def __init__(self, api):
        self.create_attr_dicts(api)
        # self.printDicts()


# api_call = Dota("https://api.opendota.com/api/heroes")
# api_call.getWinsLossesAgi("https://api.opendota.com/api/players/66957927/heroes")
# hero = input("Enter hero: ")
# api_call.getWinsLosses(hero)
