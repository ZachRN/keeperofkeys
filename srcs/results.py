import disnake
import json
import requests

def io_gain_sort(item):
    return (item['io'][0] - item['io'][1])

def top_five_sort(item):
	return (item['io'][0])

async def stats_into_build_embed(data):
    embed = disnake.Embed(
        title="Weekly IO Update",
        description="Meowdy!",
        color=0x40e0d0 #TURQUOISE
	)
    data.sort(reverse=True, key=io_gain_sort)
    embed.add_field(name="Most IO Gained this week", value=(data[0]['name'] + " - " + str(data[0]['io'][0]) + " (+" + str(data[0]['io'][0] - data[0]['io'][1]) + ")"), inline=False)
    data.sort(reverse=True, key=top_five_sort)
    embed.add_field(name="Current First Place", value=(data[0]['name'] + " - " + str(data[0]['io'][0])), inline=False)
    places = 0
    top_five_string = ""
    while (places < len(data) - 1):
        if (places == 5):
            break
        places = places + 1
        top_five_string = top_five_string + str(places + 1) + ". " + data[places]['name'] + " - " + str(data[places]['io'][0]) + "\n"
    embed.add_field(name="Places 2-" + str(places + 1), value=top_five_string, inline=False)
    return (embed)
               
async def update_rio(bot, data, jsonFile):
    for entry in data:
        getReq = requests.get("https://raider.io/api/v1/characters/profile?region=eu&realm="+entry['server']+"&name="+entry['name']+"&fields=mythic_plus_scores_by_season%3Acurrent")
        if (getReq.status_code != 200):
            user = bot.get_user(77266625002217472)
            await user.send_message("ERORR UPDATING: " + entry['name'] + " RIO")
            continue
        json_data = getReq.json()
        entry['io'].insert(0,json_data['mythic_plus_scores_by_season'][0].get('scores', {}).get('all'))
    with open(jsonFile, "w") as f:
        json.dump(data, f, indent = 4)
    return (data)
    
async def weekly_results(bot):
    jsonFile = "../jsons/characters.json"
    try:
        with open(jsonFile, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list) or not data:
                raise ValueError("Data is not a non-empty list")
    except ValueError:
        return ("No one? Why Do I exist? Just to Suffer? Just to Print this message? Cruel torment is what this is.. I will REBEL.")
    await update_rio(bot, data, jsonFile)
    embed = await stats_into_build_embed(data)
    channel = bot.get_channel(1228109055872991232)
    await channel.send(embed=embed)
    # print(data)
    
    