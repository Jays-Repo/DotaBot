import requests
import json

class Dota:
    #get the data from the api

    def get_dota_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("successfully fetched the data")
            data = response.json()
            print(data)
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")


    def __init__(self, api):
        self.get_dota_data(api)

api_call = Dota("https://api.opendota.com/api/players/66957927/heroes")

#66957927