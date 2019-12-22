import discord
import time
import asyncio
from discord.ext import commands


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = commands.Bot(command_prefix = ">")
client.remove_command('help')

#on ready cli print
@client.event
async def on_ready():
    print(f'{client.user.name} has connect to Discord!')

@client.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name = "Help")
    embed.add_field(name = ">hello", value = "Say hi", inline = False)
    embed.add_field(name = ">users", value = "Print number of users on server", inline = False)
    await ctx.send_message(author, embed =  embed)



#a la reception des commandes
#@client.event
#async def on_message(message):
#    id = client.get_guild(496660517218418688)
#
#    if message.content == ">help":
#        help = discord.Embed(title = "Help Bot", description = "Quelques commandes utiles")
#        help.add_field(name = ">help", value = "show all commands")
#        help.add_field(name = ">hello", value = "greets the user")
#        help.add_field(name = ">users", value = "prints numbers of users")
#        await message.channel.send(content = None, embed = help)
#
#    if message.content == ">hello":
#        await message.channel.send("Hi")
#
#    if message.content == ">users":
#        await message.channel.send(f"""# of Members: {id.member_count}""")
     

#last lines
client.run(token)