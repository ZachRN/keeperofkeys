import disnake
from disnake.ext import commands
import json
import requests
from main import json_mutex


async def register(ID, raiderio):
    linkParse = raiderio.split("/")
    if (len(linkParse) != 7):
        return ("This isn't a valid Raider IO Link! Or a Valid link to scam my parsing!")
    name = linkParse[6]
    server = linkParse[5].capitalize()
    apiCallStore = requests.get("https://raider.io/api/v1/characters/profile?region=eu&realm="+server+"&name="+name)
    if (apiCallStore.status_code != 200):
         return ("Information provided did not yield a character.")
    apiInfo = apiCallStore.json()
    jsonFile = "../jsons/characters.json"
    new_entry = {'id': ID, 'name': name, 'server': server, 'io': [0, 0], 'class': apiInfo['class'], 'spec': apiInfo['active_spec_name'], 'ksm': False}
    async with json_mutex:
        try:
            with open(jsonFile, 'r') as file:
                data = json.load(file)
                if not isinstance(data, list) or not data:
                    raise ValueError("Data is not a non-empty list")
        except ValueError:
            data = []
        for entry in data:
            if entry['id'] == ID:
                return ("Error! You already have a registered Character. Please ping Zach as he is too lazy to have functionality for you to manually fix it yourself.")
        data.append(new_entry)
        with open(jsonFile, 'w') as file:
            json.dump(data, file, indent = 4)
    return (name + " Of " + server + " has joined the ranks!")
class RegisterCommand(commands.Cog):
    #This is the Register command

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Enter your character name and server to register on the bot.")
    async def register(self, inter: disnake.ApplicationCommandInteraction, raiderio:str):
        #This 
        await inter.response.send_message(await register(inter.author.id, raiderio))

def setup(bot: commands.Bot):
    bot.add_cog(RegisterCommand(bot))