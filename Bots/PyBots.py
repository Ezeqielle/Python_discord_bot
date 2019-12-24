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
    author = ctx.author.name
    await ctx.send(author+' rolled a **'+result+'**')

@bot.command()
@commands.has_any_role('admin', 'Admin')
async def purge(ctx):
    old = ctx.channel
    pos_old = ctx.channel.position
    purged = await old.clone()
    await purged.edit(position = pos_old + 1)
    await old.delete()
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole): 
        await ctx.send('> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')

@bot.command()
async def duplicate(ctx):
    dupl = ctx.channel
    pos = ctx.channel.position
    new = await dupl.clone()
    await new.edit(position = pos + 1)

@bot.command()
@commands.has_any_role('Admin', 'admin')
async def resetRole():
    ""
@resetRole.error
async def resetRole_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole): 
        await ctx.send('> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')

@bot.command()
async def help(ctx):
    help_list = discord.Embed(colour = discord.Colour.red())
    help_list.set_author(name = "Command Helper")
    help_list.add_field(name = "__**>help**__", value = "Display all commands and how use them", inline = False)
    help_list.add_field(name = "__**>roll NdN**__", value = "Done N roll between 1 and N", inline = False)
    help_list.add_field(name = "__**>purge**__", value = "Delete all messages in the channel where command was sent (require admin role)", inline = False)
    help_list.add_field(name = "__**>duplicate**__", value = "Duplicate the channel where command was sent", inline = False)
    help_list.add_field(name = "__**>resetRole**__", value = "Reset specific role for everyone on this guild", inline = False)
    
    await ctx.send(embed = help_list)

#last line
bot.run(token)