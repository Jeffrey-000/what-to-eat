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


#very inefficient sending
#takes around 40 secs just sending
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    for channel in bot.get_all_channels():
        if str(channel).upper() in scrapper.DINNING_HALLS:
            await channel.purge()
            await channel.send("--------------------------------------------------------**LUNCH**--------------------------------------------------------", silent=True)
            data  = food.filterParsedMenu(food.parseMenuWholeWeek(food.get_api(scrapper.DINNING_HALLS[str(channel).upper()], 'lunch')))[food.today.TODAY]
            for key, value in data.items():
                await channel.send("**" + str(key)  + "**" + "\n" + str(value) + "\n.", silent=True)

            await channel.send("--------------------------------------------------------**DINNER**--------------------------------------------------------", silent=True)

            data  = food.filterParsedMenu(food.parseMenuWholeWeek(food.get_api(scrapper.DINNING_HALLS[str(channel).upper()], 'dinner')))[food.today.TODAY]
            for key, value in data.items():
                await channel.send("**" + str(key)  + "**" + "\n" + str(value) + "\n.", silent=True)

    await bot.close()


@bot.event
async def on_message(message):
    if message.author == bot.user: #so bot cannot recursively respond to self
        return




bot.run(TOKEN)
