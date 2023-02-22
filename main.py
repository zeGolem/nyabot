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


async def hug_handler(message: discord.Message, command: list[str]):
    target = ""
    if len(command) <= 1:
        target = f"<@{message.author.id}>"
    else:
        target = command[1]

    if "hugs" not in gifs:
        await message.reply(
            "im so sorry, i have no hugs to give you for now... come back later :3")

    hug = random.choice(gifs["hugs"])
    await message.reply(f"here u go {target}\n{hug}")

COMMAND_HANDLERS = {
    "hug": hug_handler,
}

# Discord events


@client.event
async def on_message(message: discord.Message):
    if message.author.bot == True:
        return

    # TODO: Do proper parsing of the message
    message_as_command = message.content.split(" ")

    command = message_as_command[0]
    if command in COMMAND_HANDLERS:
        await COMMAND_HANDLERS[command](message, message_as_command)


client.run(open("token").read())
