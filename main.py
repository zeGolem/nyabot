#!/usr/bin/env python3

import discord
import json
import random

import data_manager
import interaction_views

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

gifs = {}
with open("gifs.json") as file:
    gifs = json.load(file)

lines = {}
with open("lines.json") as file:
    lines = json.load(file)

HELP_MESSAGE = """
Gif commands:
```
hug - Hugs target user
kiss - Kisses target user 
cuddle - Cuddles with target user 
hold - Hold target user's hand 
pat - Gives the targeted user headpats 
wag - Makes the target user's tail wag  
fuck - Does some "stuff" to the target user 😳 
flush - Makes the target user blush 
lewd - Makes you say that it's too lewd 
boop - Boops target user
```

Slash commands:
```
/help - Shows this message
/marry - Marries someone
```
"""


def __find_mariage_for_member_id(member_id: int) -> list[int]:
    data = data_manager.get_data()
    if "marriages" not in data:
        data["marriages"] = []
        with data_manager.DataWriter() as writer:
            writer.set_data(data)
        return []

    for marriage in data["marriages"]:
        if member_id in marriage:
            return marriage

    return []


# Slash commands


@bot.slash_command()
@discord.guild_only()
@discord.option(
    "target", type=discord.Member,
    description="Which user to marry",
    required=False,
)
async def marry(
        context: discord.ApplicationContext, member_to_marry: discord.Member
):
    # Check if the person asked in mariage is interested
    marriage_asker = context.author
    if marriage_asker is None:
        await context.respond("ow :/ something went wonky wonky, try again!")
        return

    askers_marriage = __find_mariage_for_member_id(marriage_asker.id)
    askees_marriage = __find_mariage_for_member_id(member_to_marry.id)

    if member_to_marry.id in askers_marriage:  # Already married
        await context.respond(f"u are already married to {member_to_marry.mention}, silly!")
        return

    marriage_confirmation = interaction_views.MariageConfirmationView(
        member_to_marry
    )
    await context.respond(
        f"{member_to_marry.mention}, would you like to marry"
        + f" {marriage_asker.mention}?", view=marriage_confirmation)

    await marriage_confirmation.wait()
    if marriage_confirmation.user_accepted is None:
        await context.respond("silly little bug going on :3 try again l8er :3")
        return

    if marriage_confirmation.user_accepted == False:
        await context.respond(
            "no consent == no marriage! consent is key to a happy life :3"
        )

    # Marriage was accepted, yay :3!
    # Now check for polycules
    if len(askers_marriage) == 0 and len(askees_marriage) == 0:
        # No polycules, just update the records to marry the two :3
        data = data_manager.get_data()
        data["marriages"].append([marriage_asker.id, member_to_marry.id])
        with data_manager.DataWriter() as writer:
            writer.set_data(data)

        await context.respond(
            f"{marriage_asker.mention} married {member_to_marry.mention}"
        )

        return

    await context.respond(
        "ooh looks like you're trying to do a ploly marriage..." +
        " unfortunately, that's still a work in progress," +
        " come back later to register it :3"
    )


@bot.slash_command()
async def help(ctx: discord.ApplicationContext):
    await ctx.respond(HELP_MESSAGE)

# Commands


async def gif_command_handler(message: discord.Message, command: list[str]):
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

GIF_COMMANDS = [
    "hug",
    "kiss",
    "cuddle",
    "hold",
    "pat",
    "wag",
    "fuck",
    "blush",
    "lewd",
    "boop",
]

# Discord events


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot == True:
        return

    # TODO: Do proper parsing of the message
    message_as_command = message.content.split(" ")

    command = message_as_command[0]
    if command in GIF_COMMANDS:
        await gif_command_handler(message, message_as_command)


bot.run(open("token").read())
