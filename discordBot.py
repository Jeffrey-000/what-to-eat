import scrapper



import discord
from dotenv import load_dotenv
import os
import random
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

food = scrapper.Bot()

EMOJILIST = []
EMOJILISTPATH = "/Users/moose/Documents/code/what-to-eat/emojiList.txt"
with open(EMOJILISTPATH, "r") as f:
    EMOJILIST = f.read().split("\n")


def pretty(foodsList): #custom formatting for food string
    s = ""
    for string in foodsList:
        s = s + string + " " + str(random.sample(EMOJILIST, 1)[0]) + " "

    return s    

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
            #with open("./test.txt","w") as f:
               # f.write(str(data))
            for key, value in data.items():
                await channel.send("**" + str(key)  + "**" + "\n" + pretty(value) + "\n.", silent=True)

            await channel.send("--------------------------------------------------------**DINNER**--------------------------------------------------------", silent=True)

            data  = food.filterParsedMenu(food.parseMenuWholeWeek(food.get_api(scrapper.DINNING_HALLS[str(channel).upper()], 'dinner')))[food.today.TODAY]
            for key, value in data.items():
                await channel.send("**" + str(key)  + "**" + "\n" + pretty(value) + "\n.", silent=True)

    await bot.close() #does print some unclosed connection warning but its a dont care situation for now
    exit()

@bot.event
async def on_message(message):
    if message.author == bot.user: #so bot cannot recursively respond to self
        return




bot.run(TOKEN)
