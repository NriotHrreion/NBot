import discord
import os
import requests
import json
from replit import db
from values import commands, channel_ids

client = discord.Client()

def get_hitokoto():
  response = requests.get("https://v1.hitokoto.cn")
  json_data = json.loads(response.text)
  hitokoto = "> "+ json_data["hitokoto"] +" --_"+ json_data["from"] +"_"
  return hitokoto

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(msg):

  if msg.author == client.user:
    return
  
  if msg.content.startswith("$"):
    print("User "+ msg.author.name +" did the command: "+ msg.content)
  
  if msg.channel.id == channel_ids["video-share"]:
    await client.get_channel(channel_ids["chat"]).send(msg.author.name +" shared a video in <#"+ str(channel_ids["video-share"]) +"> channel, would you like to have a look?")
  
  if msg.content.startswith("$about"):
    embedMsg = discord.Embed(title="About Me", description="I'm a discord bot!", color=discord.Color.blue())
    embedMsg.set_thumbnail(url="https://nin.red/static/icon.png")
    embedMsg.add_field(name="Author", value="By _NriotHrreion_", inline=False)
    embedMsg.add_field(name="Websites", value="My blog see -> https://nriothrreion.github.io\nMy website see -> https://nin.red", inline=False)
    await msg.channel.send(embed=embedMsg)

  if msg.content.startswith("$help"):
    embedMsg = discord.Embed(title="Command Help", description="Command list & help, you can see all my commands here.", color=discord.Color.blue())
    embedMsg.set_thumbnail(url="https://nin.red/static/icon.png")

    for command in commands:
      embedMsg.add_field(name=command.split("-")[0], value=command.split("-")[1], inline=True)
    
    await msg.channel.send(embed=embedMsg)

  if msg.content.startswith("$init"):
    db["afk."+ msg.author.name] = "false"
    await msg.channel.send("**Inited!**")

  if msg.content.startswith("$henlo"):
    await msg.channel.send("<@"+ str(msg.author.id) +">\nhenlo")
  
  if msg.content.startswith("$hitokoto"):
    hitokoto = get_hitokoto()

    print("Hitokoto "+ hitokoto.replace("_", "", 2))
    await msg.channel.send(hitokoto)
  
  if msg.content.startswith("$afk"):
    try:
      if db["afk."+ msg.author.name] != "true":
        db["afk."+ msg.author.name] = "true"
        await msg.channel.send("@everyone\n**"+ msg.author.name +"** is now afk"+ msg.content.replace("$afk", "") +".")
      else:
        db["afk."+ msg.author.name] = "false"
        await msg.channel.send("@everyone\n**"+ msg.author.name +"** no longer afk.")
    except:
      await msg.channel.send("Before using this feature, please do `$init`")
  
  if msg.content.startswith("$debug"):
    await msg.channel.send("debug")

client.run(os.getenv("TOKEN"))
