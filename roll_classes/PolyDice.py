from dataclasses import dataclass
from random import randint
from typing import List

from roll_classes.RollClass import RollClass


@dataclass
class Dice:
    count: int
    sides: int

    def roll(self):
        return sum([randint(1, self.sides) for _ in range(self.count)])


class PolyDice(RollClass):
    __roll_macro__ = "/roll"
    pool: List[Dice]
    results: List[int]

    def _is_mod(self, mod: str) -> bool:
        try:
            int(mod)
            return True
        except ValueError:
            return False

    def roll(self) -> str:
        # Doesn't support anything but "+" in dice strings
        parts = self.dice_str.split("+")
        dice = [p.lower() for p in parts if "d" in p.lower()]
        mods = [int(p) for p in parts if self._is_mod(p)]
        # each part should either be "XdY" or an integer
        try:
            self.pool = [Dice(count=int(d[0]), sides=int(d[1])) for d in [die.split("d") for die in dice]]
        except ValueError:
            return
        else:
            self.results = [d.roll() for d in self.pool]
            return f"""
Rolling `{self.dice_str}`:
```{self.results}{(' + ' + str(sum(mods))) if mods else ''}```
**Result:  `{sum(self.results) + sum(mods)}`**
"""
