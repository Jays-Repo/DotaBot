"""Main functionality for the dota_bot.

Setup for the bot is provided. Functionality to 
send and receive messages, and slash commands are created.

"""

from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Message, app_commands
from discord.ext import commands
from responses import get_heroes_message, get_response, get_winloss
from dota import Dota

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
API_URL = "https://api.opendota.com/api/heroes"


# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
# client: Client = Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)

dota_bot = Dota(API_URL)


# Step 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    """Function to send messages back to the user.

    This is a test function to test the functionality of the dota_bot,
    it is not going to stay for the end product.

    """
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        (
            await message.author.send(response)
            if is_private
            else await message.channel.send(response)
        )

    except Exception as e:
        print(e)


# Step 3: HANDLING STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    """Handles the startup for our bot."""
    await client.tree.sync()
    print(f"{client.user} is now running!")

    # Debug: Print registered commands
    print("Registered Commands:", [cmd.name for cmd in client.tree.get_commands()])


# Step 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    """Handles incoming messages in the discord."""

    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

    await client.process_commands(message)


# slash-command to get the catalog of all heroes
@client.tree.command(
    name="getallheroes",
    description="Get a list of all Dota heroes categorized by attributes.",
)
async def get_all_heroes(interaction: discord.Interaction):
    """This function gets all the heroes from the dota bot dictionaries.

    We want to be able to show the discord users every single hero
    given their attribute. For example, Axe should fall under "strength
    heroes". This calls the get_heroes_message function from responses.py, which
    calls a function from the dota_bot class. A string is returned, and then sent
    to the user in the discord.

    """
    heroes_message = get_heroes_message(dota_bot)
    await interaction.response.send_message(heroes_message)


# slash-command to get individual winrates
@client.tree.command(name="getwinrate", description="Get a winrate for a given hero.")
@app_commands.describe(hero="Enter the hero name(e.g., Axe)")
async def get_win_rate(interaction: discord.Interaction, hero: str):
    """This function returns winrate information on a single hero to the user.

    The user provides a hero name, and then the get_winloss function is called from
    responses.py. This takes in the dota_bot object and the hero name, and backend
    functionality is performed to get the winrate information.

    """
    win_loss = get_winloss(dota_bot, hero)
    await interaction.response.send_message(win_loss)


@client.tree.command(name="sync", description="Sync")
async def sync(interaction: discord.Interaction):
    """Syncs our slash commands."""
    await client.tree.sync()
    await interaction.response.send_message("Slash commands synced!")


# STEP 5: MAIN ENTRY POINT
def main() -> None:
    """Main entry point to run the dota bot, token is provided."""
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
