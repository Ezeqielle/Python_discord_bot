import discord
import time
import asyncio

messages = joined = 0

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = discord.Client()

#quand un user rejoint le serveur
@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "welcome":
            ""
            #await client.send_message(f"""welcome to the server {member.mention}""")

#a la reception des commandes
@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(496660517218418688)
    channels = ["testbot"]

    if message.content == ">help":
        help = discord.Embed(title = "Help Bot", description = "Quelques commandes utiles")
        help.add_field(name = ">hello", value = "greets the user")
        help.add_field(name = ">users", value = "prints numbers of users")
        await message.channel.send(content = None, embed = help)

    if str(message.channel) in channels:
        if message.content.find(">hello") != -1:
            await message.channel.send("Hi")
        elif message.content == ">users":
            await message.channel.send(f"""# of Members: {id.member_count}""")
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")


#last lines
client.loop.create_task(update_stats())
client.run(token)