__all__ = ['HelperClass']
from discord import Message


class HelperClass:
    # This is needed in each class, defining how to parse the message
    __cmd_macro__ = None
    message: Message

    def __init__(self, message: Message, cmd_str: str) -> None:
        self.message = message
        self.cmd_str = cmd_str
        if not self.__cmd_macro__:
            raise NotImplementedError('Every subclass must define a `__cmd_macro__`')

    async def _say(self, msg: str) -> None:
        """Send the given message to the channel the both received a command from"""
        await self.message.reply(msg)

    async def _dm(self, msg: str) -> None:
        """Send the given message to the person who sent the command"""
        await self.message.author.send(msg)

    async def cmd(self) -> None:
        """
        Takes the basic cmd string and parses it for the specific helper class
        It's up to the child class to call either
        `await self._say(msg)`
        or
        `await self._dm(msg)`
        in order to send messages to Discord.
        """
        pass
