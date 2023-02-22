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

# Commands
# Gif commands


async def gif_handler(message: discord.Message, command: list[str]):
    gif_kind = command[0]

    target = message.author.name
    if len(message.mentions) > 0:
        target = message.mentions[0].name

    if gif_kind not in gifs:
        await message.reply(
            "im so sorry, i have no such thing to give you for now... come back later :3")
        return

    choosen_gif = random.choice(gifs[gif_kind])
    await message.reply(f"here u go {target}\n{choosen_gif}")

GIF_COMMANDS = [
    "hug",
    "kiss",
    "cuddle",
    "hold",
    "pat",
]

# Discord events


@client.event
async def on_message(message: discord.Message):
    if message.author.bot == True:
        return

    # TODO: Do proper parsing of the message
    message_as_command = message.content.split(" ")

    command = message_as_command[0]
    if command in GIF_COMMANDS:
        await gif_handler(message, message_as_command)


client.run(open("token").read())
