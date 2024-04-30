import disnake
import json
import requests

async def send_embed(bot, data):
	channel = bot.get_channel(1228109055872991232)
	embed = disnake.Embed(
		title="Keystone Master Alert!",
		description="Meowdy!",
		color=0xD8D8D8 #LIGHT SILVER
	)
	embed.add_field(name="**Congratulations!**", value=f"{data['name']} of {data['server']} has acquired Keystone Master!")
	await channel.send(embed=embed)

async def ksm_announce(bot):
	jsonFile = "../jsons/characters.json"
	try:
		with open(jsonFile, 'r') as file:
			data = json.load(file)
			if not isinstance(data, list) or not data:
				raise ValueError("Data is not a non-empty list")
	except ValueError:
		return ("No one? Why Do I exist? Just to Suffer? Just to Print this message? Cruel torment is what this is.. I will REBEL.")
	for entry in data:
		if (entry['ksm'] == False):
			getReq = requests.get("https://raider.io/api/v1/characters/profile?region=eu&realm="+entry['server']+"&name="+entry['name']+"&fields=mythic_plus_scores_by_season%3Acurrent")
			if (getReq.status_code != 200):
				user = bot.get_user(77266625002217472)
				await user.send_message("ERORR KSM: " + entry['name'] + "ZACH PUT OUT THE FIRE QUICK")
				continue
			json_data = getReq.json()
			if ((json_data['mythic_plus_scores_by_season'][0].get('scores', {}).get('all')) >= 2000):
				entry['ksm'] = True
				await send_embed(bot, entry)
	with open(jsonFile, "w") as f:
		json.dump(data, f, indent = 4)
	# print(data)