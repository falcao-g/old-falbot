import discord
from discord.ext import commands
import json
from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter

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

c = CurrencyRates()
d = CurrencyCodes()
codes = ['BRL','USD', 'EUR', 'IDR', 'BGN', 'ILS', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON', 'MYR', 'SEK', 'SGD', 'HKD', 'AUD', 'CHF', 'KRW', 'CNY', 'TRY', 'HRK', 'NZD', 'THB', 'NOK']
names = ['Real Brasileiro', 'Dólar Americano', 'Euro', 'Rupia indonésia', 'Lev búlgaro', 'Novo shekel israelense', 'Libra esterlina', 'Coroa dinamarquesa', 'Dólar canadense', 'Iene', 'Florim húngaro', 'Leu romeno', 'Ringgit malaio', 'Coroa sueca', 'Dólar de Singapura', 'Dólar de Hong Kong', 'Dólar australiano', 'Franco suíço', 'Won sul-coreano', 'Remimbi', 'Lira turca', 'Kuna croata', 'Dólar neozelandês', 'Baht', 'Coroa norueguesa']
codes2 = ['RUB', 'INR', 'MXN', 'CZK', 'PLN', 'PHP', 'ZAR']
names2 = ['Rublo russo', 'Rupia indiana', 'Peso mexicano', 'Coroa checa', 'Zloty', 'Peso filipino', 'Rand sul-africano']


@commands.guild_only()
@client.command()
async def cambio(ctx, base_cur, dest_cur, amount):
    await ctx.send(f'O resultado da conversão é {d.get_symbol(dest_cur)}{c.convert(base_cur, dest_cur, float(amount))}')

@commands.guild_only()
@client.command()
async def moedas(ctx):
    embed = discord.Embed(
    title='**Moedas**',
    color=discord.Color.blue()
    )
    for f,i in enumerate(codes):
        embed.add_field(name=f'{codes[f]}', value=f'{names[f]}')

    embed2 = discord.Embed(
    color=discord.Color.blue()
    )
    for a,b in enumerate(codes2):
        embed2.add_field(name=f'{codes2[a]}', value=f'{names2[a]}')
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

client.run('NzQyMzMxODEzNTM5ODcyNzk4.XzEkYA.zxlzvzmaWBW8KMTs8Jrb6Zk-DfY')