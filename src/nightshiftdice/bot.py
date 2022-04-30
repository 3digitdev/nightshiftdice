import discord
import os
import re

from typing import Optional

from .roll_classes import RollClass, CoffeeDetective

HELP_MSG = """
**Use various '/' commands to roll dice!**
`/roll help`  For rolling normal polyhedral dice.
**I also support multiple custom systems for dice rolling:**
- `/cd help`  for Coffee Detective
- `/cc help`  for Corvid Court
- `/mb help`  for Mistborn
- `/v help`    for Vaesen
"""

ROLL_CLASSES = RollClass.__subclasses__()
# Restrict which channels people are allowed to invoke the dicebot in
ALLOWED_CHANNEL_IDS = [
    591462371323805748,  # game-room
    798588526861484033,  # bot-pen
]
# This is to allow certain roll classes to persist between commands,
# in the case of tracking things like persistent state for initiative etc.
CACHED_ROLL_CLASSES = {}


def get_dice_class(message: discord.Message) -> Optional[RollClass]:
    """Retrieve the RollClass child that matches to the message, if any"""
    for rc in ROLL_CLASSES:
        match = re.findall(f"^{rc.__roll_macro__}\s+(.*)$", message.content)
        if match:
            if rc.__name__ in CACHED_ROLL_CLASSES:
                c = CACHED_ROLL_CLASSES[rc.__name__]
                c.dice_str = match[0]
                c.message = message
            else:
                c = rc(message, match[0])
                CACHED_ROLL_CLASSES[rc.__name__] = c
            return c
    return None


class DiceRollerClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if str(self.user.id) in message.content and "help" in message.content.lower():
            await message.channel.send(HELP_MSG)
            return
        dice_class = get_dice_class(message)
        if not dice_class:
            return
        if message.channel.id not in ALLOWED_CHANNEL_IDS:
            await message.channel.send(":eyes: _stares at channel name disapprovingly_")
        await dice_class.roll()


def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERROR:  MISSING 'DISCORD_TOKEN' ENV VARIABLE")
        exit(1)
    client = DiceRollerClient()
    client.run(token)
