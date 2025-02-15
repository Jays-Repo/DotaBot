"""Responses.py returns messages to the user when slash commands are performed."""

from random import choice, randint
import dota


def get_response(user_input: str) -> str:
    """This is a dummy test function, will be removed soon."""
    lowered: str = user_input.lower()

    if lowered == "":
        return "Well, you're awfully silent..."
    elif "hello" in lowered:
        return "Hello there!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 6)}"
    else:
        return choice(["Hi Cora", "What are you doin", "Did this work"])


def get_heroes_message(dota_bot: dota.Dota):
    """This function gathers all hero data from a function.

    Takes in a dota.Dota object, returns the information
    from all of the dictionaries that are created when a dota_bot
    object is made. This includes every hero in dota with their attribute and id.

    """

    hero_data = dota_bot.get_heroes_data()

    return f"{hero_data}"


def get_winloss(dota_bot: dota.Dota, hero: str):
    """This function gets the win loss ratio of an indivdual hero
    for the user."""

    winloss_data = dota_bot.get_winloss_data(hero)

    return winloss_data
