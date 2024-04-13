import scrapper

import discord
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

food = scrapper.Bot()

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    for channel in bot.get_all_channels():
        if str(channel).upper() in scrapper.DINNING_HALLS:
            await channel.purge()
            for key, value in food.lazyGet(scrapper.DINNING_HALLS[str(channel).upper()]).items():
                await channel.send("**" + str(key)  + "**" + "\n" +str(value) + "\n.")


@bot.event
async def on_message(message):
    if message.author == bot.user: #so bot cannot recursively respond to self
        return




bot.run(TOKEN)