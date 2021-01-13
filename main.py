import discord
import re
import os

from roll_classes.PolyDice import PolyDice
from roll_classes.Mistborn import MistbornRoll

HELP_MSG = """
**Use various '/' commands to roll dice!**
- `/roll <dice>`   To roll normal polyhedral dice.           Example:  `/roll 1d12+2d6+6`
- `/mb #`                   To roll dice for the Mistborn RPG.     Example:  `/mb 6` will roll 6 dice and calculate the results
"""

ROLL_CLASSES = [
    MistbornRoll,
    PolyDice,
]


def get_dice_class(message: str):
    for rc in ROLL_CLASSES:
        match = re.findall(f"{rc.__roll_macro__} (.*)", message)
        if match:
            return rc(match[0])


class DiceRollerClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if str(self.user.id) in message.content and "help" in message.content.lower():
            await message.channel.send(HELP_MSG)
            return
        dice_class = get_dice_class(message.content)
        if dice_class:
            await message.channel.send(dice_class.roll())


client = DiceRollerClient()
client.run(os.getenv("DISCORD_TOKEN"))
