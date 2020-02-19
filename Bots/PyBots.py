# python 3

import discord
from discord.ext import commands
from discord.utils import find
import random
import asyncio
import re


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
bot = commands.Bot(command_prefix='>')
bot.remove_command('help')


# on ready
@bot.event
async def on_ready():
    print('Logged in as')
    print('Name : ' + bot.user.name)
    print('ID   : ' + str(bot.user.id))
    print('-------------------------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("for help write >help"))


# on join
@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(
            '**Hello {}! Thanks to report to the >help command for list all commands and configure the bot.**'.format(
                guild.name))


# setup
@bot.command()
@commands.has_any_role('admin', 'Admin')
async def setup(ctx):
    print('> please enter the name of your guild between <>')


@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(
            '> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')


# roll
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    author = ctx.author.name
    await ctx.send('> ' + author + ' rolled a **' + result + '**')


# purge
@bot.command()
@commands.has_any_role('admin', 'Admin')
async def purge(ctx):
    old = ctx.channel
    pos_old = ctx.channel.position
    purged = await old.clone()
    await purged.edit(position=pos_old)
    await old.delete()


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(
            '> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')


# duplicate
@bot.command()
async def duplicate(ctx):
    dupl = ctx.channel
    pos = ctx.channel.position
    new = await dupl.clone()
    await new.edit(position=pos + 1)


# resetMS
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
async def resetMS_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(
            '> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')


# reset role
@bot.command()
@commands.has_any_role('Admin', 'admin')
async def reset(ctx):
    re = ctx.message.content
    re = re.split(' ')
    del re[0]
    re = ' '.join(re)
    for role in ctx.guild.roles:
        if re in role.name:
            for member in role.members:
                await asyncio.sleep(1)
                await member.remove_roles(role)


@reset.error
async def reset_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(
            '> **Can\'t do that! You don\'t have admin role. Please ask an admin to send command or give you admin role.**')


# poll
@bot.command()
async def poll(ctx):
    poll = ctx.message.content
    poll = poll.split('<')
    question = poll[0].split(' ')
    del question[0]
    question = ' '.join(question)
    answers = poll[1].split('|')
    length = len(answers)
    if length > 7:
        await ctx.send('You can\'t make a poll for more than 7 things!!')
        return
    if length == 2 and answers[0] == ' yes ' and answers[1] == ' no':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']
    description = []
    for x, answer in enumerate(answers):
        description += '\n {} {}'.format(reactions[x], answer)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for reaction in reactions[:len(answers)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text='Poll request by: {}'.format(ctx.message.author))
    await react_message.edit(embed=embed)
    await ctx.message.delete()


# set role by reaction
@bot.command()
@commands.has_any_role('Admin', 'admin')
async def role(ctx, user, reaction):
    getRole = ctx.message.content
    getRole = getRole.split(';')
    message = getRole[0].split(' ')
    del message[0]
    message = ' '.join(message)
    reactions = []
    description = []
    choices = getRole[1].split("|")
    try:
        for emoji in re.findall('<:(.+?)>', ctx.message.content):
            reactions.append(f'<:{emoji}>')
    except:
        print('no custom emojis')
    for choice in choices:
        description += '\n {}'.format(choice)
    embed = discord.Embed(title=message, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for react in reactions:
        await react_message.add_reaction(react)
    embed.set_footer(text='Request by: {}'.format(ctx.message.author))
    await react_message.edit(embed=embed)
    await ctx.message.delete()
    tmp = getRole[1].split(' ')
    print(tmp)
    roleList = []
    removeList = ['', '<', '|']
    for element in tmp:
        if element not in removeList:
            if element.isalpha():
                roleList.append(element)
    print('roleList: ', roleList)
    await ctx.add_reaction(emoji=reactions)
    for x, moji in enumerate(reactions):
        if reaction.emoji == moji:
            role = discord.utils.get(user.server.roles, name=roleList[x].name)
            await bot.add_roles(user, role)


'''
@bot.event
async def on_ready():
    Channel = client.get_channel('YOUR_CHANNEL_ID')
    Text= "YOUR_MESSAGE_HERE"
    Moji = await client.send_message(Channel, Text)
    await client.add_reaction(Moji, emoji='🏃')
@bot.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel('YOUR_CHANNEL_ID')
    if reaction.message.channel.id != Channel
    return
    if reaction.emoji == "🏃":
      Role = discord.utils.get(user.server.roles, name="YOUR_ROLE_NAME_HERE")
      await client.add_roles(user, Role)
'''


@bot.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(color=discord.Color.dark_blue())
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


# help
@bot.command()
async def help(ctx):
    help_list = discord.Embed(colour=discord.Colour.red())
    help_list.set_author(name="Command Helper")
    help_list.add_field(name="__**REQUIREMENT**__",
                        value="You need to have a role named admin or Admin for use admin only commands!!",
                        inline=False)
    # users commands
    help_list.add_field(name="__**USERS commands : **__",
                        value="Commands for all members",
                        inline=False)
    help_list.add_field(name="**>help**",
                        value="Display all commands and how use them",
                        inline=False)
    help_list.add_field(name="**>roll NdN**",
                        value="Done N roll between 1 and N",
                        inline=False)
    help_list.add_field(name="**>duplicate**",
                        value="Duplicate the channel where command was sent",
                        inline=False)
    help_list.add_field(name="**>avatar @mention**",
                        value="Show the mentioned avatar in an embed",
                        inline=False)
    # admin only commands
    help_list.add_field(name="__**ADMIN only commands : **__",
                        value="Commands only for admin",
                        inline=False)
    # help_list.add_field(name="**>setup**", value="Start BOT setup for this guild (require admin role)", inline=False)
    help_list.add_field(name="**>purge**",
                        value="Delete all messages in the channel where command was sent (require admin role)",
                        inline=False)
    help_list.add_field(name="**>role message; :emoji: choice | :emoji: choice | ... | :emoji: choice**",
                        value="Give role by react at an embed you need to write the role name like in your role manager (work only with custom emoji and require admin role)",
                        inline=False)
    help_list.add_field(name="**>resetMS**",
                        value="Reset Mythic Score for everyone (require admin role)",
                        inline=False)
    help_list.add_field(name="**>reset role**",
                        value="Reset role for everyone (require admin role and the bot need to have the highest role on guild for good work)",
                        inline=False)

    help_list.set_footer(text='https://github.com/Ezeqielle/Python_discord_bot')
    await ctx.send(embed=help_list)


# last line
bot.run(token)
