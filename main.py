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
async def on_message(message):
    if message.author == client.user:
        return
    
    # await message.channel.send("%contador")

    await client.process_commands(message)


@client.command()
async def oi(context, *nome):
    if len(nome) == 0:
        await context.reply('Ei, cadê seu nome? Eu sei que você tem!! 👀')
    else:
        await context.channel.send(f'Oii {" ".join(nome)}!')

@client.command()
async def contador(context):
    usuario = context.author
    counter = load_pickle(0, 'counter-{}'.format(usuario))
    counter += 1
    save_pickle(counter, 'counter-{}'.format(usuario))
    await context.channel.send("Usuario " + str(usuario) + ": " + str(counter))

@client.command()
async def date(context):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    await context.channel.send(dt_string)

client.run('MTA1MjI2NDg5ODA1MjIzNTI5NQ.GtGrps.XLoAnGD1ZOOcbnDZyiQr4MpvG_2X7kKtqJBLgQ')
