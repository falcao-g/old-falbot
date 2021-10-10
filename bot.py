import discord
from discord.ext import commands
import asyncio
import shelve
import random

banco = shelve.open('santander', 'c')

client = commands.Bot(command_prefix='?', case_insensitive=True)

def cria_banco(pessoa):
    if not pessoa in banco:
        banco[pessoa] = {'Falcoins': 0, 'Vitorias': 0, 'Dívida': 0, 'Agiota': ''}

def muda_saldo(pessoa, dinheiro):
    temp = banco[pessoa]
    temp['Falcoins'] += dinheiro
    banco[pessoa] = temp
    temp = ''

def muda_divida(pessoa, dinheiro):
    temp = banco[pessoa]
    temp['Dívida'] += dinheiro
    if temp['Dívida'] <= 0:
        temp['Agiota'] = ''
    banco[pessoa] = temp
    temp = ''

def muda_agiota(pessoa, agiota):
    temp = banco[pessoa]
    temp['Agiota'] += agiota
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

def tempo_formatado(erro):
    minuto = 0
    segundo = 0
    formata = ''
    errinho = str(erro)
    for c in errinho:
        if c in '0123456789':
            formata += c
    segundo += int(formata[0:-2])
    minuto += segundo//60
    segundo -= minuto*60
    if len(str(minuto)) == 1 and len(str(segundo)) == 1: 
        formata = f'00:0{minuto}:0{segundo}'
    elif len(str(minuto)) == 1 and len(str(segundo)) == 2:
        formata = f'00:0{minuto}:{segundo}'
    elif len(str(minuto)) == 2 and len(str(segundo)) == 1:
        formata = f'00:{minuto}:0{segundo}'
    else:
        formata = f'00:{minuto}:{segundo}'
    return formata

def arg_especial(arg,pessoa):
    if arg == 'tudo':
        arg = banco[pessoa]['Falcoins']
    elif arg == 'metade':
        arg = int(banco[pessoa]['Falcoins'] / 2)
    else:
        for c in arg:
            if c == '%':
                arg = int(int(arg[:-1]) * int(banco[str(pessoa)]['Falcoins']) / 100)
    return arg

def format(falcoins):
    pop = str(falcoins)
    pop_2 = ''
    for c,i in enumerate(pop[::-1]):
        if c/3 == int(c/3) and c/3 != 0:
            pop_2 += '.'
            pop_2 += i
        else:
            pop_2 += i

    return pop_2[::-1]

@client.event
async def on_ready():
    activity = discord.Activity(name='?comandos', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

@commands.guild_only()
@client.command()
async def eu(ctx):
    cria_banco(str(ctx.message.author.id))
    embed = discord.Embed(
        title=ctx.message.author.name,
        color=discord.Color(000000)
    )
    for key,item in banco[str(ctx.message.author.id)].items():
        if key != 'Agiota':
            embed.add_field(name=key, value=format(item), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def apostar(ctx, arg, *args):
    cria_banco(str(ctx.message.author.id))
    arg = arg_especial(arg, str(ctx.message.author.id))
    try:
        if banco[str(ctx.message.author.id)]['Falcoins'] >= int(arg) and int(arg) > 0:
            guild = ctx.guild
            if discord.utils.get(ctx.guild.roles, name="Pomba") == None:
                await guild.create_role(name="Pomba", colour=discord.Colour(0xD2D4DC))
            role = discord.utils.get(ctx.guild.roles, name="Pomba")
            role1 = discord.utils.get(ctx.guild.roles, name="Pardal")
            role2 = discord.utils.get(ctx.guild.roles, name="Tucano")
            role3 = discord.utils.get(ctx.guild.roles, name="Falcão")
            if role not in ctx.message.author.roles and role1 not in ctx.message.author.roles and role2 not in ctx.message.author.roles and role3 not in ctx.message.author.roles:
                await ctx.message.author.add_roles(role)
            sorte = random.randint(0,100)
            if sorte >= 95:
                muda_saldo(str(ctx.message.author.id), -int(arg))
                await ctx.send (f'{ctx.message.author.mention} você perdeu tudo que apostou :pensive: :fist: *Saldo atual*: {format(banco[str(ctx.message.author.id)]["Falcoins"])}') 
            elif sorte <= 55:
                porcentagem = random.randint(10,100)
                total = int((porcentagem * int(arg)) / 100)
                comissao = int(total/10)
                if banco[str(ctx.message.author.id)]['Dívida'] > 0:
                    total -= comissao
                if total == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), total)
                await ctx.send (f'{ctx.message.author.mention} Parabéns! Você lucrou {format(total)} falcoins :sunglasses: *Saldo atual*: {format(banco[str(ctx.message.author.id)]["Falcoins"])}')
                if banco[str(ctx.message.author.id)]['Dívida'] > 0:
                    if comissao == 0:
                        comissao = 1
                    if comissao > banco[str(ctx.message.author.id)]['Dívida']:
                        muda_saldo(str(banco[str(ctx.message.author.id)]['Agiota']), banco[str(ctx.message.author.id)]['Dívida'])
                        user = client.get_user(int(banco[str(ctx.message.author.id)]['Agiota']))
                        await ctx.send(f'{ctx.message.author.name} pagou {format(banco[str(ctx.message.author.id)]["Dívida"])} falcoins de comissão. Restando 0 de débito com {user.name}')
                        muda_divida(str(ctx.message.author.id), -int(banco[str(ctx.message.author.id)]['Dívida']))
                    else:    
                        muda_saldo(str(banco[str(ctx.message.author.id)]['Agiota']), comissao)
                        user = client.get_user(int(banco[str(ctx.message.author.id)]['Agiota']))
                        muda_divida(str(ctx.message.author.id), -comissao)
                        await ctx.send(f'{ctx.message.author.name} pagou {format(comissao)} falcoins de comissão. Restando {format(banco[str(ctx.message.author.id)]["Dívida"])} de débito com {user.name}')
            else:
                porcentagem = random.randint(10,90)
                total = int((porcentagem * int(arg)) / 100)
                if total == 0:
                    total = 1
                muda_saldo(str(ctx.message.author.id), -total)
                await ctx.send (f'{ctx.message.author.mention} você perdeu {format(total)} falcoins :slight_frown: *Saldo atual*: {format(banco[str(ctx.message.author.id)]["Falcoins"])}')
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
        cria_banco(str(ctx.message.author.id))
        lb = random.randint(200, 600)
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
    cu = tratamento(arg)
    cria_banco(str(ctx.message.author.id))
    cria_banco(cu)
    arg2 = arg_especial(arg2, str(ctx.message.author.id))
    if banco[str(ctx.message.author.id)]['Falcoins'] >= int(arg2):
        muda_saldo(str(ctx.message.author.id), -int(arg2))
        muda_saldo(cu, int(arg2))
        await ctx.send(f'{ctx.message.author.mention} transferiu {format(arg2)} falcoins para {arg}')
    else:
        await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para esta doação! :rage:')

@commands.guild_only()
@client.command()
async def sobre(ctx, arg):
    cu = tratamento(arg)
    cria_banco(str(ctx.message.author.id))
    cria_banco(cu)
    user = client.get_user(int(cu))
    embed = discord.Embed(
        title=user.name,
        color=discord.Color(000000)
    )
    for key,item in banco[str(cu)].items():
        if key != "Agiota":
            embed.add_field(name=key, value=format(item), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def falcoins(ctx):
    embed = discord.Embed(
        color=discord.Color(000000)
    )
    embed.add_field(name="Falcoins", value=format(banco[str(ctx.message.author.id)]['Falcoins']), inline=True)
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(ctx.message.author.mention)
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command()
async def rank_global(ctx):
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
    if str(ctx.message.author.id) != tratamento(arg):
        gifs = ['4.gif', '2.gif', '3.gif', '4.gif']
        cu = tratamento(arg)
        user = client.get_user(int(cu))
        cria_banco(str(ctx.message.author.id))
        cria_banco(cu)
        arg2 = arg_especial(arg2,str(ctx.message.author.id))
        if banco[str(ctx.message.author.id)]['Falcoins'] >= int(arg2) and banco[cu]["Falcoins"] >= int(arg2):
            message = await ctx.send(f'{ctx.message.author.mention} chamou {arg} para um duelo da sorte apostando {format(arg2)} reais :smiling_imp:')
            await message.add_reaction('✅')
            await message.add_reaction('🚫')

            def check(reaction, useri):
                return useri == user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🚫')

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f'Duelo cancelado. {arg} demorou muito para aceitar! :confounded:')
            else:
                if str(reaction.emoji) == '✅':
                    await ctx.send(f'Duelo aceito. {arg} aceitou entrar em duelo com {ctx.message.author.mention} :open_mouth:')
                    await ctx.send(file=discord.File(random.choice(gifs)))
                    ganhou = random.randint(1,2)
                    if ganhou == 1:
                        muda_saldo(str(ctx.message.author.id), int(arg2))
                        muda_saldo(cu, -int(arg2))
                        muda_vitoria(str(ctx.message.author.id), 1)
                        await asyncio.sleep(2)
                        await ctx.send(f'{ctx.message.author.mention} ganhou os {format(arg2)} reais do duelo! :stuck_out_tongue:')
                    else:
                        muda_saldo(str(ctx.message.author.id), -int(arg2))
                        muda_saldo(cu, int(arg2))
                        muda_vitoria(tratamento(arg), 1)
                        await asyncio.sleep(2)
                        await ctx.send(f'{arg} ganhou os {format(arg2)} reais do duelo! :stuck_out_tongue:')
                else:
                    await ctx.send(f'Duelo cancelado. {arg} recusou o duelo! :confounded:')
        else:
            await ctx.send(f'Saldo insuficiente em uma das contas! :grimacing:')
    else:
        await ctx.send(f'{ctx.message.author.mention} Você não pode duelar com você mesmo, espertinho :rage:')

@commands.guild_only()
@client.command()
async def rank(ctx):
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
    if str(ctx.message.author.id) != tratamento(arg):
        cu = tratamento(arg)
        user = client.get_user(int(cu))
        cria_banco(str(ctx.message.author.id))
        cria_banco(cu)
        arg2 = arg_especial(arg2, str(ctx.message.author.id))
        if banco[str(ctx.message.author.id)]['Falcoins'] >= int(arg2):
            if banco[cu]['Dívida'] == 0:
                message = await ctx.send(f'{ctx.message.author.mention} quer investir {format(arg2)} falcoins em {arg}. Aceitas? :smiling_imp:')
                await message.add_reaction('✅')
                await message.add_reaction('🚫')

                def check(reaction, useri):
                    return useri == user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🚫')

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
                except:
                    await ctx.send(f'Investimento cancelado. {arg} demorou muito para aceitar! :confounded:')
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
                        await ctx.send(f'Investimento aceito! {ctx.message.author.mention} depositou {format(arg2)} falcoins na conta de {arg}, {ctx.message.author.name} ganhará 10% de tudo que {user.name} ganhar, até cobrir a divida de {format(divida)} zulcoins :open_mouth: :smiling_imp:')
                        muda_saldo(str(ctx.message.author.id), -int(arg2))
                        muda_saldo(cu, int(arg2))
                        muda_divida(cu, divida)
                        muda_agiota(cu, str(ctx.message.author.id))
                    else:
                        await ctx.send(f'Investimento cancelado. {arg} recusou o investimento de {format(arg2)} por {ctx.message.author.mention} :slight_frown:')
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
    if arg == "1":
        guild = ctx.guild
        if discord.utils.get(ctx.guild.roles, name="Pardal") == None:
            await guild.create_role(name="Pardal", colour=discord.Colour(0x842121))
        role = discord.utils.get(ctx.guild.roles, name="Pardal")
        role2 = discord.utils.get(ctx.guild.roles, name="Tucano")
        role3 = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles or role2 in ctx.message.author.roles or role3 in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if banco[str(ctx.message.author.id)]['Falcoins'] >= 500000:
                role1 = discord.utils.get(ctx.guild.roles, name="Pomba")
                if role1 in ctx.message.author.roles:
                    muda_saldo(str(ctx.message.author.id), -500000)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Pardal :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa fazer alguma aposta antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:')
    elif arg == "2":
        guild = ctx.guild
        if discord.utils.get(ctx.guild.roles, name="Tucano") == None:
            await guild.create_role(name="Tucano", colour=discord.Colour(0xFFA500))
        role = discord.utils.get(ctx.guild.roles, name="Tucano")
        role2 = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles or role2 in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if banco[str(ctx.message.author.id)]['Falcoins'] >= 100000000:
                role1 = discord.utils.get(ctx.guild.roles, name="Pardal")
                if role1 in ctx.message.author.roles:
                    muda_saldo(str(ctx.message.author.id), -100000000)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Tucano :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa ter o cargo de Pardal antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:')
    elif arg == "3":
        guild = ctx.guild
        if discord.utils.get(ctx.guild.roles, name="Falcão") == None:
            await guild.create_role(name="Falcão", colour=discord.Colour(0x4C4CFF))
        role = discord.utils.get(ctx.guild.roles, name="Falcão")
        if role in ctx.message.author.roles:
            await ctx.send(f'{ctx.message.author.mention} você já possui esse cargo! :rage:')
        else:
            if banco[str(ctx.message.author.id)]['Falcoins'] >= 1000000000:
                role1 = discord.utils.get(ctx.guild.roles, name="Tucano")
                if role1 in ctx.message.author.roles:
                    muda_saldo(str(ctx.message.author.id), -1000000000)
                    await ctx.message.author.remove_roles(role1)
                    await ctx.message.author.add_roles(role)
                    await ctx.send(f'Parabéns {ctx.message.author.mention}! Você comprou o cargo de Falcão :star_struck:')
                else:
                    await ctx.send(f'{ctx.message.author.mention} você precisa ter o cargo de Tucano antes de comprar esse cargo! :rage:')
            else:
                await ctx.send(f'{ctx.message.author.mention} você não tem falcoins suficiente para comprar esse cargo! :rage:') 

@client.command()
async def comandos(ctx):
    embed = discord.Embed(
        title='Comandos para sala de jogos',
        color=discord.Color.green()
    )
    embed.add_field(name=f"?sobre [@pessoa]", value=f'Mostra os dados sobre a pessoa marcada', inline=False)
    embed.add_field(name=f"?eu", value=f'Mostra os seus dados', inline=False)
    embed.add_field(name=f"?lootbox", value=f'Resgata sua lootbox grátis(disponível a cada 30 minutos)', inline=False)
    embed.add_field(name="?falcoins", value='Mostra o seu saldo atual', inline=False)
    embed.add_field(name="?doar [@pessoa] [valor]", value='Doa o valor inserido para a pessoa marcada', inline=False)
    embed.add_field(name=f"?apostar [valor]", value=f'Aposta o valor ou porcentagem indicado, com ganhos até 100%!', inline=False)
    embed.add_field(name=f"?duelo [@pessoa] [valor]", value=f'Duela com a pessoa marcada. apostando o valor indicado', inline=False)
    embed.add_field(name=f"?rank", value=f'Retorna a tabela de ranking do servidor atual por falcoins', inline=False)
    embed.add_field(name=f"?rank_global", value=f'Retorna a tabela de ranking global por falcoins', inline=False)
    embed.add_field(name=f"?loja", value=f"Retorna a tabela de compras e seus valores", inline=False)
    embed.add_field(name=f"?comprar [Número do item]", value=f"Compra o item citado no parametro se você tem os requisitos")
    embed.set_footer(text='by Falcão ❤️')
    await ctx.send(embed=embed)

client.run('SECRET-TOKEN')
