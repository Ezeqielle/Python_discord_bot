import discord
from discord.ext import commands
import random
import time
import asyncio

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

bot = commands.Bot(command_prefix = '>')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def purge(ctx):
    async for msg in ctx.channel.history(limit = None):
        await msg.delete()

@bot.command()
async def help(ctx):
    help_list = discord.Embed(colour = discord.Colour.red())
    help_list.set_author(name = "Command Helper")
    help_list.add_field(name = "__**>help**__", value = "All commands and how use them", inline = False)
    help_list.add_field(name = "__**>roll**__", value = ">roll NdN | done N roll between 1 and N", inline = False)
    help_list.add_field(name = "__**>purge**__", value = "Delete all messages in the channel where the command was send (require admin role)", inline = False)
    help_list.add_field(name = "__**>othercommand**__", value = "other explaination", inline = False)
    
    await ctx.send(embed = help_list)

#last line
bot.run(token)