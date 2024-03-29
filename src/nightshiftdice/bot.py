import discord
import os
import re
import logging

from typing import Optional

from .roll_classes import RollClass

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s :: %(message)s')
log = logging.getLogger()
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.ERROR)

HELP_MSG = """
**Use various '/' commands to roll dice**
`/roll help`  For rolling normal polyhedral dice.
**I also support multiple custom systems for dice rolling:**
- `/cd help`   for Coffee Detective
- `/cc help`   for Corvid Court
- `/mb help`   for Mistborn
- `/v help`     for Vaesen
- `/td help`   for Tiny Dungeons
- `/ryu help` for Ryuutama
- `/h help`     for Hunter: The Vigil
- `/tg help`   for Trophy Gold
- `/ag help`   for Agon
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
        match = re.findall(f'^{rc.__roll_macro__}\s+(.*)$', message.content)
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


class ChatClient(discord.Client):
    async def on_ready(self):
        log.info(f'{self.user} has connected to Discord')

    async def _handle_ping_commands(self, message: discord.Message) -> None:
        if 'help' == ' '.join(message.content.split(' ')[1:]).lower():
            log.info('Prayer to the Machine Spirit detected, lending aid')
            await message.channel.send(HELP_MSG)
            return

    async def _handle_roll_commands(self, message: discord.Message) -> None:
        log.info('Parsing as dice roll')
        dice_class = get_dice_class(message)
        if not dice_class:
            log.warn('No dice handler found')
            return
        log.info(f'Found handler: {dice_class.__class__.__name__}')
        if message.channel.id not in ALLOWED_CHANNEL_IDS:
            await message.channel.send(':eyes: _stares at channel name disapprovingly_')
        await dice_class.roll()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        log.info(f'Message seen: {message.content}\n  From: {message.author}')
        if str(self.user.id) in message.content:
            await self._handle_ping_commands(message)
        else:
            await self._handle_roll_commands(message)


def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        log.fatal('ERROR:  MISSING DISCORD_TOKEN')
        exit(1)
    client = ChatClient()
    client.run(token)
