import discord
from discord.ext import commands
import asyncio
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    
        prefixes[str(message.guild.id)] = '?'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        return prefixes[str(message.guild.id)]

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True, guild_messages=True)
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, help_command=None)

@commands.guild_only()
@client.command()
async def tetris(ctx):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://jstris.jezevec10.com/')

    ### creates room
    lobbyB = driver.find_element_by_id('lobby')
    lobbyB.click()

    createB = driver.find_element_by_id('createRoomButton')
    createB.click()

    privateC = driver.find_element_by_id('isPrivate')
    privateC.click()

    await asyncio.sleep(3)

    createBF = driver.find_element_by_id('create')
    createBF.click()

    await asyncio.sleep(5)

    joinLink = driver.find_element_by_class_name('joinLink')
    await ctx.send(joinLink.get_attribute('innerHTML'))

    await asyncio.sleep(30)

    driver.quit()

client.run('NzQyMzMxODEzNTM5ODcyNzk4.XzEkYA.zxlzvzmaWBW8KMTs8Jrb6Zk-DfY')