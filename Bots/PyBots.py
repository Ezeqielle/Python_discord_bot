import discord
from discord.ext import commands
from discord.utils import find
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

#on ready
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Too powerfull BOT"))

#on join
@bot.event
async def on_guild_join(guild):
    general  = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('**Hello {}! Thanks to report to the >help command for list all commands and configure the bot.**'.format(guild.name))

#setup
@bot.command()
@commands.has_any_role('admin', 'Admin')
async def setup(ctx):
    print('> please enter the name of your guild between <>')
@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole): 
        await ctx.send('> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')

#roll
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    author = ctx.author.name
    await ctx.send('> '+author+' rolled a **'+result+'**')

#purge
@bot.command()
@commands.has_any_role('admin', 'Admin')
async def purge(ctx):
    old = ctx.channel
    pos_old = ctx.channel.position
    purged = await old.clone()
    await purged.edit(position = pos_old)
    await old.delete()
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole): 
        await ctx.send('> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')

#duplicate
@bot.command()
async def duplicate(ctx):
    dupl = ctx.channel
    pos = ctx.channel.position
    new = await dupl.clone()
    await new.edit(position = pos + 1)

#resetMS
@bot.command()
@commands.has_any_role('Admin', 'admin')
async def resetMS(ctx):
    ms = 'Mythic Score'
    for role in ctx.guild.roles:
        if ms in role.name:
            for member in role.members:
                await asyncio.sleep(1)
                await member.remove_roles(role)
@resetMS.error
async def resetRole_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole): 
        await ctx.send('> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')

#poll
@bot.command()
async def poll(ctx):
    poll = ctx.message.content
    poll = poll.split('<')
    question = poll[0].split(' ')
    del question[0]
    question = ' '.join(question)
    answers = poll[1].split('|')
    lenght = len(answers)
    if lenght > 7:
        await ctx.send('You can\'t make a poll for more than 7 things!!')
        return
    if lenght == 2 and answers[0] == ' yes ' and answers[1] == ' no':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']
    description = []
    for x, answer in enumerate(answers):
        description += '\n {} {}'.format(reactions[x], answer)
    embed = discord.Embed(title = question, description = ''.join(description))
    react_message = await ctx.send(embed = embed)
    for reaction in reactions[:len(answers)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text = 'Poll request by: {}'.format(ctx.message.author))
    await react_message.edit(embed = embed)
    await ctx.message.delete()

#help
@bot.command()
async def help(ctx):
    help_list = discord.Embed(colour = discord.Colour.red())
    help_list.set_author(name = "Command Helper")
    help_list.add_field(name = "__**REQUIREMENT**__", value = "You need to have a role named admin or Admin for use admin only commands!!", inline = False)
    #users commands
    help_list.add_field(name = "__**USERS commands : **__", value = "Commands for all members", inline = False)
    help_list.add_field(name = "**>help**", value = "Display all commands and how use them", inline = False)
    help_list.add_field(name = "**>roll NdN**", value = "Done N roll between 1 and N", inline = False)
    help_list.add_field(name = "**>duplicate**", value = "Duplicate the channel where command was sent", inline = False)
    help_list.add_field(name = "**>poll question < answer1 | ... | answer7**", value = "Done a poll request where command was sent", inline = False)
    #admin only commands
    help_list.add_field(name = "__**ADMIN only commands : **__", value = "Commands only for admin", inline = False)
    help_list.add_field(name = "**>setup**", value = "Start BOT setup for this guild (require admin role)", inline = False)
    help_list.add_field(name = "**>purge**", value = "Delete all messages in the channel where command was sent (require admin role)", inline = False)
    help_list.add_field(name = "**>resetMS**", value = "Reset Mythic Score for everyone (require admin role)", inline = False)
    
    await ctx.send(embed = help_list)

#last line
bot.run(token)