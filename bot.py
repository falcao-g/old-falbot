import discord
from discord.ext import commands
import shelve
import random
import time
from operator import attrgetter,itemgetter

def cria_banco(pessoa):
    if not pessoa in banco:
        banco[pessoa] = {'Dinheiro': 0, 'Vitorias': 0}

def muda_saldo(pessoa, dinheiro):
    temp = banco[pessoa]
    temp['Dinheiro'] += dinheiro
    banco[pessoa] = temp
    temp = ''

def muda_vitoria(pessoa, vitoria):
    temp = banco[pessoa]
    temp['Vitorias'] += vitoria
    banco[pessoa] = temp
    temp = ''

def tratamento(mencao):
    cu = ''
    for c in mencao:
        if c not in '@<>!':
            cu += c
    return cu

banco = shelve.open('twnt', 'c')

client = commands.Bot(command_prefix='?')

@client.command()
async def eu(ctx):
    cria_banco(str(ctx.message.author.id))
    embed = discord.Embed(
        title=ctx.message.author.name,
        color=discord.Color.blue()
    )
    embed.add_field(name="Dinheiro", value=banco[str(ctx.message.author.id)]['Dinheiro'], inline=True)
    embed.add_field(name="Vitorias", value=banco[str(ctx.message.author.id)]['Vitorias'], inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@client.command()
async def apostar(ctx, arg):
    cria_banco(str(ctx.message.author.id))
    try:
        if banco[str(ctx.message.author.id)]['Dinheiro'] >= int(arg) and int(arg) > 0:
            sorte = random.randint(0,100)
            if sorte >= 95:
                muda_saldo(str(ctx.message.author.id), -arg)
                await ctx.send ('você perdeu tudo que apostou :pensive: :fist:') 
            elif sorte <= 50:
                porcentagem = random.randint(10,90)
                total = (porcentagem * int(arg)) / 100
                if int(total) == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), int(total))
                await ctx.send (f'{ctx.message.author.mention} Parabéns! Você lucrou {int(total)} reais :sunglasses: *Saldo atual*: {banco[str(ctx.message.author.id)]["Dinheiro"]}')
            else:
                porcentagem = random.randint(10,90)
                total = (porcentagem * int(arg)) / 100
                if int(total) == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), int(-total))
                await ctx.send (f'{ctx.message.author.mention} você perdeu {int(total)} reais :slight_frown: *Saldo atual*: {banco[str(ctx.message.author.id)]["Dinheiro"]}')
        elif int(arg) <= 0:
            await ctx.send(f'{ctx.message.author.mention} o número precisa ser maior do que zero! :rage:')
        else:
            await ctx.send(f'{ctx.message.author.mention} você não tem dinheiro suficiente para esta aposta! :rage:')
    except ValueError:
        await ctx.send(f'{ctx.message.author.mention} não é um número válido :rage:')


@client.command()
async def lootbox(ctx):
        cria_banco(str(ctx.message.author.id))
        lb = random.randint(200, 600)
        muda_saldo(str(ctx.message.author.id), lb)
        await ctx.send(f'{ctx.message.author.mention} Parabéns! Você ganhou **{lb}** reais :heart_eyes:')

@client.command()
async def doar(ctx, arg, arg2):
    cu = tratamento(arg)
    cria_banco(str(ctx.message.author.id))
    cria_banco(cu)
    doacao = int(arg2)
    if banco[str(ctx.message.author.id)]['Dinheiro'] >= doacao:
        muda_saldo(str(ctx.message.author.id),-doacao)
        muda_saldo(cu,doacao)
        await ctx.send(f'{ctx.message.author.mention} transferiu {doacao} reais para <@{int(cu)}>')

@client.command()
async def sobre(ctx, arg):
    cu = tratamento(arg)
    cria_banco(str(ctx.message.author.id))
    cria_banco(cu)
    user = client.get_user(int(cu))
    embed = discord.Embed(
        title=user.name,
        color=discord.Color.blue()
    )
    embed.add_field(name="Dinheiro", value=banco[cu]['Dinheiro'], inline=True)
    embed.add_field(name="Vitorias", value=banco[cu]['Vitorias'], inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@client.command()
async def dinheiro(ctx):
    embed = discord.Embed(
        color=discord.Color.blue()
    )
    embed.add_field(name="Dinheiro", value=banco[str(ctx.message.author.id)]['Dinheiro'], inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(ctx.message.author.mention)
    await ctx.send(embed=embed)

@client.command()
async def rank(ctx):
    chaves = []
    for chave in banco:
        chaves.append([banco[chave]['Dinheiro'], chave])
    for num in range(len(chaves)-1,0,-1):
        for i in range(num):
                if not chaves[i][0]>chaves[i+1][0]:
                    temp = chaves[i]
                    chaves[i] = chaves[i+1]
                    chaves[i+1] = temp
    rank = [user[1] for user in chaves]
    users = [client.get_user(int(user)) for user in rank]
    embed = discord.Embed(
        color=discord.Color.blue()
    )
    if len(rank) >= 10:
        embed.add_field(name=f"1° - {users[0].name} reais:", value=f'`{banco[rank[0]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"2° - {users[1].name} reais:", value=f'`{banco[rank[1]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"3° - {users[2].name} reais:", value=f'`{banco[rank[2]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"4° - {users[3].name} reais:", value=f'`{banco[rank[3]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"5° - {users[4].name} reais:", value=f'`{banco[rank[4]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"6° - {users[5].name} reais:", value=f'`{banco[rank[5]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"7° - {users[6].name} reais:", value=f'`{banco[rank[6]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"8° - {users[7].name} reais:", value=f'`{banco[rank[7]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"9° - {users[8].name} reais:", value=f'`{banco[rank[8]]["Dinheiro"]}`', inline=False)
        embed.add_field(name=f"10° - {users[9].name} reais:", value=f'`{banco[rank[9]]["Dinheiro"]}`', inline=False)
    else:
        for c,i in enumerate(rank):
            embed.add_field(name=f"{c+1}° - {users[c].name} reais:", value=f'`{banco[rank[c]]["Dinheiro"]}`', inline=False)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@client.command()
async def duelo(ctx, arg, arg2):
    grana = int(arg2)
    cu = tratamento(arg)
    user = client.get_user(int(cu))
    cria_banco(str(ctx.message.author.id))
    cria_banco(cu)
    if banco[str(ctx.message.author.id)]['Dinheiro'] >= grana and banco[cu]["Dinheiro"] >= grana:
        message = await ctx.send(f'{ctx.message.author.mention} chamou {arg} para um duelo da sorte apostando {arg2} reais :smiling_imp:')
        await message.add_reaction('✅')
        await message.add_reaction('🚫')
        @client.event
        async def on_reaction_add(reaction, useri):
                if reaction.emoji == '✅' and useri == user:
                    await ctx.send(f'Duelo aceito. {arg} aceitou entrar em duelo com {ctx.message.author.mention} :open_mouth:')
                    ganhou = random.randint(1,2)
                    if ganhou == 1:
                        muda_saldo(str(ctx.message.author.id), grana)
                        muda_saldo(cu, -grana)
                        time.sleep(2)
                        await ctx.send(f'{ctx.message.author.mention} ganhou')
                    else:
                        muda_saldo(str(ctx.message.author.id), -grana)
                        muda_saldo(cu, grana)
                        time.sleep(2)
                        await ctx.send(f'{arg} ganhou')
    else:
        await ctx.send(f'{ctx.message.author.mention} saldo insuficiente em uma das contas :slight_frown:')

    

client.run('SECRET-TOKEN')
