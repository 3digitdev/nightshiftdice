import discord
import re
import os

from roll_classes.PolyDice import PolyDice
from roll_classes.Mistborn import MistbornRoll
from roll_classes.Vaesen import VaesenRoll
from roll_classes.Coffee import CoffeeRoll

HELP_MSG = """
**Use various '/' commands to roll dice!**
- `/roll <dice>`   To roll normal polyhedral dice.           Example:  `/roll 1d12+2d6+6`
- `/mb #`                   To roll dice for the Mistborn RPG.     Example:  `/mb 6` will roll 6 dice and calculate the results
- `/v #`                     To roll dice for the Vaesen RPG.        Example:  `/v 5` will roll 5 dice and give you the successes
- `/cd`                       To draw a card for Coffee Detective
"""

ROLL_CLASSES = [
    MistbornRoll,
    PolyDice,
    VaesenRoll,
    CoffeeRoll,
]
ALLOWED_CHANNEL_IDS = [
    591462371323805748,  # game-room
]


cached = {}


def get_dice_class(message: str):
    for rc in ROLL_CLASSES:
        match = re.findall(f"^{rc.__roll_macro__}(.*)$", message)
        if match:
            if rc.__name__ in cached:
                c = cached[rc.__name__]
                c.dice_str = match[0]
            else:
                c = rc(match[0])
                cached[rc.__name__] = c
            return c


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
            if message.channel.id not in ALLOWED_CHANNEL_IDS:
                await message.channel.send(":eyes: _stares at channel name disapprovingly_")
            elif dice_class.__class__ == CoffeeRoll:
                await message.author.send(dice_class.roll())
            else:
                await message.channel.send(dice_class.roll())


token = os.getenv("DISCORD_TOKEN")
if not token:
    print("ERROR:  MISSING 'DISCORD_TOKEN' ENV VARIABLE")
    exit(1)
client = DiceRollerClient()
client.run(token)
