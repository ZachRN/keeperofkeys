import os
from typing import Union
import disnake
from disnake.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
from results import weekly_results
from ksm import ksm_announce
# import fun_slash

# bot = commands.Bot(command_prefix=commands.when_mentioned)
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

#assigning a mutex to prevent data overwrites
#not the most elegant solution here however with such a small scope this is fine
json_mutex = asyncio.Lock()

# intents = disnake.Intents.default()
# intents.members = True
# intents.message_content = True

# bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
bot = commands.Bot(
	command_prefix='!',
	test_guilds=[578254452356546588, 1116806351893577834], # Optional
	command_sync_flags=command_sync_flags,
)
# bot = commands.Bot()
async def weekly_rio_check():
	first_task = False
	while True:
		# Get the current date and time
		now = datetime.now()

		# Define the day and time you want the function to run (Monday at 8:00 AM in this example)
		target_day = 2  # Monday (0-indexed, where Monday is 0)
		target_time = "05:30:01"  # 8:00 AM
		target_datetime = datetime.strptime(target_time, "%H:%M:%S")

		# Calculate the next occurrence of the target day and time
		next_occurrence = now + timedelta(days=(target_day - now.weekday()) % 7)
		if first_task:
			next_occurrence += timedelta(days=7)
		next_occurrence = datetime(
			year=next_occurrence.year,
			month=next_occurrence.month,
			day=next_occurrence.day,
			hour=target_datetime.hour, # SET BACK TO TARGET_OCCURENCE LATER
			minute=target_datetime.minute,
			second=target_datetime.second
		)
		print(next_occurrence.year,next_occurrence.month,next_occurrence.day)
		# Calculate the time until the next occurrence
		time_until_next_occurrence = (next_occurrence - now).total_seconds()
		print(time_until_next_occurrence)
		# Wait until the next occurrence
		await asyncio.sleep(time_until_next_occurrence)
		# Execute your function
		async with json_mutex:
			await (weekly_results(bot))
		first_task = True

async def ksm_check():
	first_task = False
	while True:
		# Get the current date and time
		now = datetime.now()

		# Define the day and time you want the function to run (Monday at 8:00 AM in this example)
		target_day = 2  # Monday (0-indexed, where Monday is 0)
		target_time = "05:30:01"  # 5:30:01 AM
		target_datetime = datetime.strptime(target_time, "%H:%M:%S")

		# Calculate the next occurrence of the target day and time
		next_occurrence = now + timedelta(hours=(target_day - now.weekday()) % 7)
		if first_task:
			next_occurrence += timedelta(hours=1)
		next_occurrence = datetime(
			year=next_occurrence.year,
			month=next_occurrence.month,
			day=next_occurrence.day,
			hour=next_occurrence.hour,
			minute=target_datetime.minute,
			second=target_datetime.second
		)
		print(next_occurrence.year,next_occurrence.month,next_occurrence.day, next_occurrence.hour)
		# Calculate the time until the next occurrence
		time_until_next_occurrence = (next_occurrence - now).total_seconds()
		print(time_until_next_occurrence)
		# Wait until the next occurrence
		await asyncio.sleep(time_until_next_occurrence)
		# Execute your function
		async with json_mutex:	
			await (ksm_announce(bot))
		first_task = True

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")
	bot.loop.create_task(weekly_rio_check())
	bot.loop.create_task(ksm_check())
	# await weekly_results(bot)

def load_extensions():
	bot.load_extension("slash_commands.register")
	bot.load_extension("slash_commands.embed")


if __name__ == "__main__":
	with open("../tokens/discord.txt", "r") as f:
		token = f.readline()
	load_extensions()
	bot.run(token)

	#Send messages, Add Reactions, Use Slash commands 2147485760