import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import asyncio
import json
import random
from aternosapi import AternosAPI
from funcoes import *
import time

headers_cookie = "ATERNOS_SEC_o393mvvlhqa00000=hobt7nyuf0k00000; __cfduid=d59d8b32263dbb9cabf79ef3d31abeb971600109203; _ga=GA1.2.405738038.1600109207; _gid=GA1.2.65661332.1600109207; ATERNOS_SESSION=vwLUDu3aeQYaQyS3FcJ7GHUGKT3nmgDoHFmHKtwlumK1ExzgqDpws1xyWcQYsnObOAOdVUOU2q8yn5DUkOER5DrIJQhX3KLDbTxF; __gads=ID=3da6e8ad584b8867:T=1600110888:S=ALNI_MZG_60N0rgeQMcbVSU3yDVuEgNaWw; SKpbjs-unifiedid=%7B%22TDID%22%3A%22b393d141-1a89-4358-a8e0-2a21dc2ccf77%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222020-09-14T19%3A12%3A15%22%7D; SKpbjs-unifiedid_last=Mon%2C%2014%20Sep%202020%2019%3A12%3A15%20GMT; SKpbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMOWTG3aMOoikJ8kOLovSVwJlmczM7o2dymoGhePg%22%2C%22ID5ID_CREATED_AT%22%3A%222020-09-14T19%3A12%3A15.882Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Afalse%2C%223PIDS%22%3A%5B%5D%7D; SKpbjs-id5id_last=Mon%2C%2014%20Sep%202020%2019%3A12%3A16%20GMT; cto_bundle=FKtmm18wSTdhcjZ2VDMlMkZaTVdHbHd3cW1nVlZyUWpVNW1nc0YzOSUyRldBd1doalBJWUc4M0pCa2NCaXNGS2hERXRaRnJLall3NFVSUkV1Y3ZkbU55enVRTHUlMkZCeUtvMm50N3V6ODZaZUF2MHZtTkJTQ3JXN2s5cllrZ1JPdXJqdWJ0aTVhbG8zR0gxVm91djVyYTdBbU9jWGJpa3clM0QlM0Q; cnx_userId=3b52d7fb5beb44e9bf9058e792abba71; ATERNOS_SERVER=kOOyQDQSLLj2Xni7; _gat=1"
cookie = "IiH8ERcQwdhqj3ZMGaVKCkxa38vc8fOrBUGHFeCfLMFOTXjAg4T2YV7XiHx8acoFyddKDCfqnVbV69eR4RfVDMbREMj8CU0p8Q9h"
ASEC = "o393mvvlhqa00000:hobt7nyuf0k00000"
epromo = 1
elootbox = 1
eaposta = 1

server = AternosAPI(headers_cookie, cookie, ASEC)

def get_prefix(client, message):
    with open('prefixos.json', 'r') as f:
        prefixos = json.load(f)
    
    return prefixos[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

@client.event
async def on_ready():
    cancela_evento.start()
    evento.start()
    activity = discord.Activity(name='?comandos', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    print('Bot online')

@client.event
async def on_guild_join(guild):
    if discord.utils.get(guild.roles, name="Falcão") == None:
        await guild.create_role(name="Falcão", colour=discord.Colour(0x4C4CFF))
    if discord.utils.get(guild.roles, name="Tucano") == None:
        await guild.create_role(name="Tucano", colour=discord.Colour(0xFFA500))
    if discord.utils.get(guild.roles, name="Pardal") == None:
        await guild.create_role(name="Pardal", colour=discord.Colour(0x842121))
    if discord.utils.get(guild.roles, name="Audacioso") == None:
        await guild.create_role(name="Audacioso", colour=discord.Colour(0xA64CA6))
    if discord.utils.get(guild.roles, name="Pomba") == None:
        await guild.create_role(name="Pomba", colour=discord.Colour(0xD2D4DC))

    with open('prefixos.json', 'r') as f:
        prefixos = json.load(f)
    
    prefixos[str(guild.id)] = '?'

    with open('prefixos.json', 'w') as f:
        json.dump(prefixos, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixos.json', 'r') as f:
        prefixos = json.load(f)

    prefixos.pop(str(guild.id))

@tasks.loop(minutes=30)
async def cancela_evento():
    global elootbox
    global eaposta
    global epromo
    if elootbox == 2 or eaposta == 2 or epromo == 2:
        elootbox = 1
        eaposta = 1
        epromo = 1
        print('Eventos acabaram')
        activity = discord.Activity(name='?comandos', type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
        print(time.localtime())

@tasks.loop(hours=2)
async def evento():
    global elootbox
    global eaposta
    global epromo
    evento = random.randint(1,100)
    if evento <= 20:
        escolha = random.randint(1,3)
        if escolha == 1:
            activity = discord.Activity(name='Evento ativado! Apostas rendem 2x', type=discord.ActivityType.watching)
            await client.change_presence(activity=activity)
            eaposta = 2
            print('Eventos iniciados')
            print(time.localtime())
        elif escolha == 2:
            activity = discord.Activity(name='Evento ativado! Lootboxs rendem 2x', type=discord.ActivityType.watching)
            await client.change_presence(activity=activity)
            elootbox = 2
            print('Eventos iniciados')
            print(time.localtime())
        else:
            activity = discord.Activity(name='Evento ativado! Cargos custam metade', type=discord.ActivityType.watching)
            await client.change_presence(activity=activity)
            epromo = 2
            print('Eventos iniciados')
            print(time.localtime())

@commands.guild_only()
@client.command()
async def eu(ctx):
    cria_banco(str(ctx.message.author.id))
    with open('falbot2.json', 'r') as f:
        banco = json.load(f)
    embed = discord.Embed(
        title=ctx.message.author.name,
        color=discord.Color(000000)
    )
    for key,item in banco[str(ctx.message.author.id)].items():
        if key != 'Agiota' and key != 'Cargo' and key != 'Audacias':
            embed.add_field(name=key, value=format(item), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def apostar(ctx, arg, *args):
    global eaposta
    cria_banco(str(ctx.message.author.id))
    arg = arg_especial(arg, str(ctx.message.author.id))
    try:
        if checa_arquivo(str(ctx.message.author.id), 'Falcoins') >= int(arg) and int(arg) > 0:
            role = discord.utils.get(ctx.guild.roles, name="Pomba")
            role1 = discord.utils.get(ctx.guild.roles, name="Pardal")
            role2 = discord.utils.get(ctx.guild.roles, name="Tucano")
            role3 = discord.utils.get(ctx.guild.roles, name="Falcão")
            if role not in ctx.message.author.roles and role1 not in ctx.message.author.roles and role2 not in ctx.message.author.roles and role3 not in ctx.message.author.roles and checa_cargo(str(ctx.message.author.id)) == 0:
                await ctx.message.author.add_roles(role)
            elif checa_cargo(str(ctx.message.author.id)) == 1:
                await ctx.message.author.add_roles(role1)
            elif checa_cargo(str(ctx.message.author.id)) == 2:
                await ctx.message.author.add_roles(role2)
            elif checa_cargo(str(ctx.message.author.id)) == 3:
                await ctx.message.author.add_roles(role3)
            sorte = random.randint(0,100)
            if sorte >= 95:
                muda_saldo(str(ctx.message.author.id), -int(arg))
                await ctx.send (f'{ctx.message.author.mention} você perdeu tudo que apostou :pensive: :fist: *Saldo atual*: {format(checa_arquivo(str(ctx.message.author.id), "Falcoins"))}') 
            elif sorte <= 55:
                porcentagem = random.randint(10,100)
                total = int((porcentagem * int(arg)) / 100) * eaposta
                comissao = int(total/10)
                if checa_arquivo(str(ctx.message.author.id), 'Divida') > 0:
                    total -= comissao
                if total == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), total)
                await ctx.send (f'{ctx.message.author.mention} Parabéns! Você lucrou {format(total)} falcoins :sunglasses: *Saldo atual*: {format(checa_arquivo(str(ctx.message.author.id), "Falcoins"))}')
                if checa_arquivo(str(ctx.message.author.id), 'Divida') > 0:
                    if comissao == 0:
                        comissao = 1
                    if comissao >= checa_arquivo(str(ctx.message.author.id), 'Divida'):
                        muda_saldo(checa_arquivo(str(ctx.message.author.id),'Agiota'), checa_arquivo(str(ctx.message.author.id), 'Divida'))
                        user = client.get_user(int(checa_arquivo(str(ctx.message.author.id), 'Agiota')))
                        await ctx.send(f'{ctx.message.author.name} pagou {format(checa_arquivo(str(ctx.message.author.id), "Divida"))} falcoins de comissão. Restando 0 de débito com {user.name}')
                        muda_divida(str(ctx.message.author.id), -int(checa_arquivo(str(ctx.message.author.id), 'Divida')))
                        zera_divida(str(ctx.message.author.id))
                    else:    
                        muda_saldo(str(checa_arquivo(str(ctx.message.author.id), 'Agiota')), comissao)
                        user = client.get_user(int(checa_arquivo(str(ctx.message.author.id), 'Agiota')))
                        muda_divida(str(ctx.message.author.id), -comissao)
                        if checa_arquivo(str(ctx.message.author.id), 'Divida') == 0:
                            zera_divida(str(ctx.message.author.id))
                        await ctx.send(f'{ctx.message.author.name} pagou {format(comissao)} falcoins de comissão. Restando {format(checa_arquivo(str(ctx.message.author.id), "Divida"))} de débito com {user.name}')
            else:
                porcentagem = random.randint(10,90)
                total = int((porcentagem * int(arg)) / 100)
                if total == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), -total)
                await ctx.send (f'{ctx.message.author.mention} você perdeu {format(total)} falcoins :slight_frown: *Saldo atual*: {format(checa_arquivo(str(ctx.message.author.id), "Falcoins"))}')
        elif int(arg) <= 0:
            await ctx.send(f'{ctx.message.author.mention} {arg} não é um valor válido... :rage:')
        else:
            await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para esta aposta! :rage:')
    except ValueError:
        await ctx.send(f'{ctx.message.author.mention} {arg}{args} não é um valor válido... :rage:')

@commands.guild_only()
@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def lootbox(ctx):
        global elootbox
        cria_banco(str(ctx.message.author.id))
        lb = random.randint(200, 600) * elootbox
        muda_saldo(str(ctx.message.author.id), lb)
        await ctx.send(f' Parabéns {ctx.message.author.mention}! Você ganhou **{lb}** falcoins :heart_eyes:')
        @client.event
        async def on_command_error(ctx,error):
            if "You are on cooldown." in str(error):
                await ctx.send(f'{ctx.message.author.mention} faltam **{tempo_formatado(error)}** para você resgatar a lootbox grátis!')
            else:
                print(error)

@commands.guild_only()
@client.command()
async def doar(ctx, arg, arg2):
    cria_banco(str(ctx.message.author.id))
    cria_banco(arg[3:-1])
    arg2 = arg_especial(arg2, str(ctx.message.author.id))
    if checa_arquivo(str(ctx.message.author.id), 'Falcoins')>= int(arg2):
        muda_saldo(str(ctx.message.author.id), -int(arg2))
        muda_saldo(arg[3:-1], int(arg2))
        await ctx.send(f'{ctx.message.author.mention} transferiu {format(arg2)} falcoins para {arg}')
    else:
        await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para esta doação! :rage:')

@commands.guild_only()
@client.command()
async def sobre(ctx, arg):
    cria_banco(str(ctx.message.author.id))
    cria_banco(arg[3:-1])
    user = client.get_user(int(arg[3:-1]))
    embed = discord.Embed(
        title=user.name,
        color=discord.Color(000000)
    )
    for key,item in checa_arquivo(arg[3:-1]).items():
        if key != "Agiota" and key != "Cargo" and key != 'Audacias':
            embed.add_field(name=key, value=format(item), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def falcoins(ctx):
    cria_banco(str(ctx.message.author.id))
    embed = discord.Embed(
        color=discord.Color(000000)
    )
    embed.add_field(name="Falcoins", value=format(checa_arquivo(str(ctx.message.author.id),'Falcoins')), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(ctx.message.author.mention)
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def rank_global(ctx):
    with open('falbot2.json', 'r') as f:
        banco = json.load(f)
    chaves = []
    for chave in banco:
        chaves.append([banco[chave]['Falcoins'], chave])
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
        for c in range(10):
            embed.add_field(name=f"{c+1}° - {users[c].name} falcoins:", value=f'`{format(banco[rank[c]]["Falcoins"])}`', inline=False)
    else:
        for c,i in enumerate(rank):
            embed.add_field(name=f"{c+1}° - {users[c].name} falcoins:", value=f'`{format(banco[rank[c]]["Falcoins"])}`', inline=False)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def duelo(ctx, arg, arg2):
    arg = arg[3:-1]
    if str(ctx.message.author.id) != arg:
        gifs = ['4.gif', '2.gif', '3.gif', '4.gif']
        user = client.get_user(int(arg))
        cria_banco(str(ctx.message.author.id))
        cria_banco(str(arg))
        arg2 = arg_especial(arg2,str(ctx.message.author.id))
        if checa_arquivo(str(ctx.message.author.id),'Falcoins') >= int(arg2) and checa_arquivo(arg, 'Falcoins') >= int(arg2):
            message = await ctx.send(f'{ctx.message.author.mention} chamou {user.mention} para um duelo da sorte apostando {format(arg2)} reais :smiling_imp:')
            await message.add_reaction('✅')
            await message.add_reaction('🚫')

            def check(reaction, useri):
                return useri == user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🚫')

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f'Duelo cancelado. {user.mention} demorou muito para aceitar! :confounded:')
            else:
                if str(reaction.emoji) == '✅':
                    await ctx.send(f'Duelo aceito. {user.mention} aceitou entrar em duelo com {ctx.message.author.mention} :open_mouth:')
                    await ctx.send(file=discord.File(random.choice(gifs)))
                    ganhou = random.randint(1,2)

                    if int(arg2) >= checa_arquivo(str(ctx.message.author.id),'Falcoins') / 20:
                        muda_audacias(str(ctx.message.author.id))
                        if checa_arquivo(str(ctx.message.author.id), 'Audacias') >= 20:
                            role1 = discord.utils.get(ctx.guild.roles, name="Audacioso")
                            if role1 not in ctx.message.author.roles:
                                 await ctx.message.author.add_roles(role1)
                                 await ctx.send(f'Parabéns {ctx.message.author.mention}! Você ganhou o cargo de Audacioso :star_struck:')

                    if int(arg2) >= checa_arquivo(arg, 'Falcoins') / 20:
                        muda_audacias(arg)
                        if checa_arquivo(arg, 'Audacias') >= 20:
                            role1 = discord.utils.get(ctx.guild.roles, name="Audacioso")
                            if role1 not in user.roles:
                                 await user.add_roles(role1)
                                 await ctx.send(f'Parabéns {user.mention}! Você ganhou o cargo de Audacioso :star_struck:')    

                    if ganhou == 1:
                        muda_saldo(str(ctx.message.author.id), int(arg2))
                        muda_saldo(arg, -int(arg2))
                        muda_vitoria(str(ctx.message.author.id))
                        await asyncio.sleep(2)
                        await ctx.send(f'{ctx.message.author.mention} ganhou os {format(arg2)} reais do duelo! :stuck_out_tongue:')
                    else:
                        muda_saldo(str(ctx.message.author.id), -int(arg2))
                        muda_saldo(arg, int(arg2))
                        muda_vitoria(arg)
                        await asyncio.sleep(2)
                        await ctx.send(f'{user.mention} ganhou os {format(arg2)} reais do duelo! :stuck_out_tongue:')
                else:
                    await ctx.send(f'Duelo cancelado. {user.mention} recusou o duelo! :confounded:')
        else:
            await ctx.send(f'Saldo insuficiente em uma das contas! :grimacing:')
    else:
        await ctx.send(f'{ctx.message.author.mention} Você não pode duelar com você mesmo, espertinho :rage:')

@commands.guild_only()
@client.command()
async def rank(ctx):
    with open('falbot2.json', 'r') as f:
        banco = json.load(f)
    x = [str(c.id) for c in ctx.guild.members]
    chaves = []
    for chave in banco:
        if chave in x:
            chaves.append([banco[chave]['Falcoins'], chave])
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
        for c in range(10):
            embed.add_field(name=f"{c+1}° - {users[c].name} falcoins:", value=f'`{format(banco[rank[c]]["Falcoins"])}`', inline=False)
    else:
        for c,i in enumerate(rank):
            embed.add_field(name=f"{c+1}° - {users[c].name} falcoins:", value=f'`{format(banco[rank[c]]["Falcoins"])}`', inline=False)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def investir(ctx, arg, arg2):
    arg = arg[3:-1]
    if str(ctx.message.author.id) != arg:
        user = client.get_user(int(arg))
        cria_banco(str(ctx.message.author.id))
        cria_banco(arg)
        arg2 = arg_especial(arg2, str(ctx.message.author.id))
        if checa_arquivo(str(ctx.message.author.id), 'Falcoins') >= int(arg2):
            if checa_arquivo(arg, 'Divida') == 0:
                message = await ctx.send(f'{ctx.message.author.mention} quer investir {format(arg2)} falcoins em {user.mention}. Aceitas? :smiling_imp:')
                await message.add_reaction('✅')
                await message.add_reaction('🚫')

                def check(reaction, useri):
                    return useri == user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🚫')

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
                except:
                    await ctx.send(f'Investimento cancelado. {user.mention} demorou muito para aceitar! :confounded:')
                else:
                    if str(reaction.emoji) == '✅':
                        role = discord.utils.get(ctx.guild.roles, name="Pardal")
                        role1 = discord.utils.get(ctx.guild.roles, name="Tucano")
                        role2 = discord.utils.get(ctx.guild.roles, name="Falcão")
                        if role not in ctx.message.author.roles and role1 not in ctx.message.author.roles and role2 not in ctx.message.author.roles:
                            divida = int(int(arg2) + int(arg2) / 4)
                        elif role in ctx.message.author.roles:
                            divida = int(int(arg2) + int(arg2) / 2)
                        elif role1 in ctx.message.author.roles:
                            divida = int(int(arg2) + (int(arg2) / 4 * 3))
                        elif role2 in ctx.message.author.roles:
                            divida = int(int(arg2) + int(arg2))
                        await ctx.send(f'Investimento aceito! {ctx.message.author.mention} depositou {format(arg2)} falcoins na conta de {user.mention}, {ctx.message.author.name} ganhará 10% de tudo que {user.name} ganhar, até cobrir a divida de {format(divida)} zulcoins :open_mouth: :smiling_imp:')
                        muda_saldo(str(ctx.message.author.id), -int(arg2))
                        muda_saldo(arg, int(arg2))
                        muda_divida(arg, divida)
                        muda_agiota(arg, str(ctx.message.author.id))
                    else:
                        await ctx.send(f'Investimento cancelado. {user.mention} recusou o investimento de {format(arg2)} por {ctx.message.author.mention} :slight_frown:')
            else:
                await ctx.send(f'{ctx.message.author.mention}, {user.name} já está em uma dívida... :neutral_face:')
        else:
            await ctx.send(f'{ctx.message.author.mention} O investimento não pode ser feito, pois você não tem os falcoins suficientes! :rage:')

@commands.guild_only()
@client.command()
async def loja(ctx):
    cria_banco(str(ctx.message.author.id))
    embed = discord.Embed(
    title='**Loja**',
    color=discord.Color.green()
    )
    embed.add_field(name=f'Item número 1: Pardal', value='Pelo custo de 500.000 falcoins você adquire um cargo de pardal no servidor, aumentando em 25% os ganhos de investimentos! (necessário ter feito alguma aposta)', inline=False)
    embed.add_field(name=f'Item número 2: Tucano',value=f'Pelo custo de 100.000.000 falcoins você adquire um cargo de tucano no servidor, aumentando em 50% os ganhos de investimentos! (necessário ser um pardal)', inline=False)
    embed.add_field(name=f'Item número 3: Falcão', value='Pelo custo de 1.000.000.000 falcoins você adquire um cargo da melhor ave do mundo no servidor, aumentando em 75% os ganhos de investimentos! (necessário ser um tucano)', inline=False)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def comprar(ctx, arg):
    global epromo
    if arg == "1":
        role = discord.utils.get(ctx.guild.roles, name="Pardal")
        role2 = discord.utils.get(ctx.guild.roles, name="Tucano")
        role3 = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles or role2 in ctx.message.author.roles or role3 in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if checa_arquivo(str(ctx.message.author.id), 'Falcoins') >= 500000 / epromo:
                role1 = discord.utils.get(ctx.guild.roles, name="Pomba")
                if role1 in ctx.message.author.roles:
                    custo = int(-500000 / epromo)
                    muda_saldo(str(ctx.message.author.id), custo)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    muda_cargo(str(ctx.message.author.id), 'Pardal')
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Pardal :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa fazer alguma aposta antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:')
    elif arg == "2":
        role = discord.utils.get(ctx.guild.roles, name="Tucano")
        role2 = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles or role2 in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if checa_arquivo(str(ctx.message.author.id), 'Falcoins') >= 100000000 / epromo:
                role1 = discord.utils.get(ctx.guild.roles, name="Pardal")
                if role1 in ctx.message.author.roles:
                    custo = int(-100000000 / epromo)
                    muda_saldo(str(ctx.message.author.id), custo)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    muda_cargo(str(ctx.message.author.id), 'Tucano')
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Tucano :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa ter o cargo de Pardal antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:')
    elif arg == "3":
        role = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if checa_arquivo(str(ctx.message.author.id), 'Falcoins')>= 1000000000 / epromo:
                role1 = discord.utils.get(ctx.guild.roles, name="Tucano")
                if role1 in ctx.message.author.roles:
                    custo = int(-1000000000 / epromo)
                    muda_saldo(str(ctx.message.author.id), custo)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    muda_cargo(str(ctx.message.author.id),'Falcão')
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Falcão :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa ter o cargo de Tucano antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:') 

@commands.guild_only()
@client.command()
async def pixelmon(ctx, arg):
    if arg == "start":
        await ctx.send('Iniciando servidor')
        server.StartServer()
        await ctx.send(f'{ctx.message.author.mention} Servidor iniciado')
    elif arg == "stop":
        await ctx.send(server.StopServer())
    elif arg == "status":
        await ctx.send(server.GetStatus())
    elif arg == "info":
        await ctx.send(server.GetServerInfo())

@commands.guild_only()
@client.command()
async def sugestao(ctx, *args):
    with open('sugestões.txt', 'a') as arquivo:
        sugestao = ''
        for c in args:
            sugestao += ' '
            sugestao += c
            sugestao += ' '
        arquivo.write(f'\n{sugestao}')
        arquivo.close()
    await ctx.send(f'{ctx.message.author.mention} sua sugestão foi salva com suscesso, obrigado! :smiling_face_with_3_hearts:')

@commands.guild_only()
@client.command()
@has_permissions(administrator = True)
async def prefixo(ctx, arg):
    with open('prefixos.json', 'r') as f:
        prefixos = json.load(f)
    
    prefixos[str(ctx.guild.id)] = arg

    with open('prefixos.json', 'w') as f:
        json.dump(prefixos, f, indent=4)
    
    await ctx.send(f'{ctx.message.author.mention} o prefixo do servidor foi mudado para "{arg}"  :smile:')

@commands.guild_only()
@client.command()
async def comandos(ctx):
    embed = discord.Embed(
        title='Comandos para sala de jogos',
        color=discord.Color.green()
    )
    embed.add_field(name=f"?eu", value=f'Mostra os seus dados', inline=False)
    embed.add_field(name=f"?lootbox", value=f'Resgata sua lootbox grátis(disponível a cada 30 minutos)', inline=False)
    embed.add_field(name="?falcoins", value='Mostra o seu saldo atual', inline=False)
    embed.add_field(name=f"?sobre [@pessoa]", value=f'Mostra os dados sobre a pessoa marcada', inline=False)
    embed.add_field(name="?doar [@pessoa] [valor]", value='Doa o valor inserido para a pessoa marcada', inline=False)
    embed.add_field(name=f"?apostar [valor]", value=f'Aposta o valor ou porcentagem indicado, com ganhos até 100%!', inline=False)
    embed.add_field(name=f"?duelo [@pessoa] [valor]", value=f'Duela com a pessoa marcada. apostando o valor indicado', inline=False)
    embed.add_field(name=f"?rank", value=f'Retorna a tabela de ranking do servidor atual por falcoins', inline=False)
    embed.add_field(name=f"?rank_global", value=f'Retorna a tabela de ranking global por falcoins', inline=False)
    embed.add_field(name=f"?loja", value=f"Retorna a tabela de compras e seus valores", inline=False)
    embed.add_field(name=f"?comprar [Número do item]", value=f"Compra o item citado no parametro se você tem os requisitos")
    embed.add_field(name=f"?investir [@pessoa] [Quantidade]", value=f"Tranfere a quantidade inserida para a pessoa, e ela pagará uma dívida com parte dos ganhos das apostas", inline=False)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)
    embed1 = discord.Embed(
        title='Outros comandos',
        color=discord.Color.red()
    )
    embed1.add_field(name=f"?prefixo [Prefixo desejado]", value=f'Muda o prefixo do bot no servidor, OBS: só administradores podem usar', inline=False)
    embed1.add_field(name=f"?sugestao [...]", value=f'Anota sua sugestão para o bot!', inline=False)
    embed1.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed1)

client.run('SECRET-TOKEN')
