import discord
from discord.ext import commands
from datetime import date, datetime
from os.path import exists
import pickle

def load_pickle(default, filename):
   if exists(f'{filename}.pickle'):
       with open(f'{filename}.pickle', 'rb') as f:
           return pickle.load(f)
   else:
       with open(f'{filename}.pickle', 'wb') as f:
           pickle.dump(default, f)
           return default


def save_pickle(obj, filename):
    with open(f'./{filename}.pickle', 'wb') as f:
        pickle.dump(obj, f)

client = commands.Bot(intents=discord.Intents.all(), command_prefix='++')

@client.event
async def on_ready():
    print(f'Logado com sucesso como {client.user}')

@client.event
async def on_voice_state_update(member, state_before, state_after):
    channel = client.get_channel(1051004621264523358)

    if not state_before.channel and state_after.channel:
        await channel.send(str(member) + " entrou no canal de voz " + str(state_after.channel))
    elif state_before.channel and not state_after.channel:
        await channel.send(str(member) + " saiu do canal de voz " + str(state_before.channel))
    elif state_before.self_mute != state_after.self_mute:
       await channel.send(str(member) + " se mutou!") if state_after.self_mute else await channel.send(str(member) + " se desmutou!")
    elif state_before.self_video != state_after.self_video:
       await channel.send(str(member) + " abriu a câmera!") if state_after.self_video else await channel.send(str(member) + " fechou a câmera!")
    elif not state_before.self_stream and state_after.self_stream:
       await channel.send(str(member) + " iniciou um stream!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.author.bot:
        messages = load_pickle(0, "messages")
        messages += 1
        save_pickle(messages, "messages")
        messages_user = load_pickle({}, "messages_user")

        if message.author.id in messages_user:
            messages_user[message.author.id] += 1
        else:
            messages_user[message.author.id] = 1

        save_pickle(messages_user, "messages_user")

    await client.process_commands(message)


@client.command()
async def oi(context, *nome):
    if len(nome) == 0:
        await context.reply('Ei, cadê seu nome? Eu sei que você tem!! 👀')
    else:
        await context.channel.send(f'Oii {" ".join(nome)}!')

@client.command()
async def contador(context):
    d = load_pickle({}, 'd')
    if context.author.id in d:
        d[context.author.id] += 1
    else:
        d[context.author.id] = 0
    save_pickle(d, 'd')
    await context.channel.send("Usuario " + str(context.author) + ": " + str(d[context.author.id]))

@client.command()
async def date(context):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    await context.channel.send(dt_string)

@client.command()
async def rank(context):
    messages_user = load_pickle({}, "messages_user")
    i = 0
    messages_user = {k: v for k, v in sorted(messages_user.items(), key=lambda item: item[1],reverse=True)}
    mensagem_final = ""
    for user in messages_user:
        if i > 10: break
        mensagem_final += "<@" + str(user) + ">: " + str(messages_user[user]) + "\n"
        i += 1

    await context.channel.send(mensagem_final)

client.run('meu token')
