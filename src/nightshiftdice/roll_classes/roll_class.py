__all__ = ["RollClass"]
from discord import Message


class RollClass:
    # This is needed in each class, defining how to parse the message
    __roll_macro__ = None
    message: Message

    def __init__(self, message: Message, dice_str: str) -> None:
        self.message = message
        self.dice_str = dice_str
        if not self.__roll_macro__:
            raise NotImplementedError("Every subclass must define a `__roll_macro__`")

    async def _say(self, msg: str) -> None:
        """Send the given message to the channel the both received a command from"""
        await self.message.channel.send(msg)

    async def _dm(self, msg: str) -> None:
        """Send the given message to the person who sent the command"""
        await self.message.author.send(msg)

    async def roll(self) -> None:
        """
        Takes the basic roll string and parses it for the specific roll class
        It's up to the child class to call either
        `await self._say(msg)`
        or
        `await self._dm(msg)`
        in order to send messages to Discord.
        """
        pass
