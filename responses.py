from random import choice, randint
from DotaBot import Dota

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "Well, you're awfully silent..."
    elif 'hello' in lowered: 
        return 'Hello there!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    else:
        return choice(['Hi Cora',
                       'What are you doin',
                       'Did this work'])
    
def get_heroes_message(dota_bot):

    hero_data = dota_bot.get_heroes_data()

    return f"{hero_data}"

def get_winloss(dota_bot, hero: str):

    winloss_data = dota_bot.get_winloss_data(hero)

    return winloss_data