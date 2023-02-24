#!/usr/bin/env python3

import discord
import json
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

gifs = {}
with open("gifs.json") as file:
    gifs = json.load(file)

lines = {}
with open("lines.json") as file:
    lines = json.load(file)

HELP_MESSAGE = """
Commands:
```hug - Hugs target user  
kiss - Kisses target user 
cuddle - Cuddles with target user 
hold - Hold target user's hand 
pat - Gives the targeted user headpats 
wag - Makes the target user's tail wag  
fuck - Does some "stuff" to the target user 😳 
flush - Makes the target user blush 
lewd - Makes you say that it's too lewd 
boop - Boops target user
help - shows this list```
"""

# Commands


async def command_handler(message: discord.Message, command: list[str]):
    command_typed = command[0]

    target = message.author.name
    sender = message.author.name
    if len(message.mentions) > 0:
        target = message.mentions[0].name

    if command_typed == "help":
        await message.reply(HELP_MESSAGE)
        return

    if command_typed not in gifs:
        await message.reply(
            "im so sorry, i have no such thing to give you for now... come back later :3")
        return

    choosen_gif = random.choice(gifs[command_typed])
    choosen_line = random.choice(lines[command_typed])
    choosen_line = choosen_line.replace("$1", sender)
    choosen_line = choosen_line.replace("$2", target)
    await message.reply(f"{choosen_line}\n{choosen_gif}")

COMMANDS = [
    "hug",
    "kiss",
    "cuddle",
    "hold",
    "pat",
    "wag",
    "fuck",
    "blush",
    "help",
    "lewd",
    "boop",
]

# Discord events


@client.event
async def on_message(message: discord.Message):
    if message.author.bot == True:
        return

    # TODO: Do proper parsing of the message
    message_as_command = message.content.split(" ")

    command = message_as_command[0]
    if command in COMMANDS:
        await command_handler(message, message_as_command)


client.run(open("token").read())
