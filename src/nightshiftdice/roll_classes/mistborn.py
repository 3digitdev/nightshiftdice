__all__ = ['Mistborn']
import collections

from random import randint

from .roll_class import RollClass


class Mistborn(RollClass):
    __roll_macro__ = '/mb'

    pool: int
    frequency: collections.Counter
    rolls: list[int]
    result: int
    nudges: int

    async def roll(self) -> None:
        extra = '\n'
        self.pool = int(self.dice_str)
        if self.pool > 10:
            self.nudges = self.pool - 10
            self.pool = 10
            extra = (
                f'**NOTE:** Dice pool above 10 -- Rolling 10 dice instead.  '
                f'**Granting {self.nudges} extra Nudges** (_reflected below_)'
            )
        else:
            self.nudges = 0
            if self.pool < 2:
                self.pool = 2
                extra = '**NOTE:** Dice pool below 2 -- Rolling 2 dice instead.  ' '**Outcome worsens by 1 level!**'
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)])
        self.frequency = collections.Counter(self.rolls)
        self.nudges += self.frequency[6]
        del self.frequency[6]
        try:
            self.result = max([k for k in self.frequency.keys() if self.frequency[k] > 1])
        except ValueError:
            self.result = 0
        await self._say(f"""{extra}
Rolling {self.pool} dice:
```Markdown
{self.rolls}
```
**Result:**  `{self.result}`
**Nudges:**  `{self.nudges}`
""")
