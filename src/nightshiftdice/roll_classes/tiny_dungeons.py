__all__ = ["TinyDungeons"]
import collections

from random import randint

from .roll_class import RollClass


class TinyDungeons(RollClass):
    __roll_macro__ = "/td"

    pool: int
    frequency: collections.Counter
    rolls: list[int]
    successes: int

    async def roll(self) -> None:
        if self.dice_str == "help":
            await self._say("""**Tiny Dungeons RPG Controls**
```
/td #     Roll 1-3 dice and calculate successes (5, 6)
/td #f    Roll 1-3 dice with focus and calculate successes (4, 5, 6)
```""")
            return
        self.focus = False
        if self.dice_str[-1] == "f":
            self.focus = True
            self.dice_str = self.dice_str.rstrip("f")
        self.pool = int(self.dice_str)
        if self.pool < 1 or self.pool > 3:
            await self._say("**ERROR**:  Can only have between 1-3 dice! Try again.")
            return
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)])
        self.frequency = collections.Counter(self.rolls)
        self.successes = self.frequency[6] + self.frequency[5] + (self.frequency[4] if self.focus else 0)
        await self._say(f"""**Rolling {self.pool} dice{' with focus' if self.focus else ''}:**
```Markdown
{self.rolls}
```
**Result:**  `{self.successes}`
""")
