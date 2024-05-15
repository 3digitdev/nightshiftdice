__all__ = ['FabulaUltima']
import re

from random import randint
from typing import List

from .roll_class import RollClass

# A mapping of the supported operators for dice rolls,
# mapped to their respective modifiers to multiply the result by
# (so '-' maps to -1 so that N * -1 = -N, so that we can just sum results
OPS = {'+': 1, '-': -1, '': 1}


def parse_roll(roll_str: str) -> (List[int], int):
    # This regex will parse 2 dice rolls like "dX+dY" into a tuple of (X, Y)
    dice_reg = re.compile(r'd(\d+)\+d(\d+)')
    all_dice = dice_reg.findall(roll_str)
    actual_dice = []
    for first, second in all_dice:
        # We iterate through separately here so that we can show
        # the result of each individual dice in the roll
        actual_dice.append(randint(1, int(first)))
        actual_dice.append(randint(1, int(second)))
    # This regex will pop any remaining non-dice ('modifiers') into a tuple of (op, modifier)
    mod_reg = re.compile(r'([+-])(\d+)(?!d)')
    mod_result = [int(mod) * OPS[op] for op, mod in mod_reg.findall(roll_str)]
    return actual_dice, sum(actual_dice + mod_result)


class FabulaUltima(RollClass):
    __roll_macro__ = '/fu'

    async def roll(self) -> None:
        if self.dice_str == 'help':
            await self._say("""**Fabula Ultima RPG Controls**
```
/fu dX+dY[+Z]   Roll 2 attribute dice [+ modifier]
```""")
            return
        try:
            separate_dice, result = parse_roll(self.dice_str)
            highest = max(separate_dice)
            gather = set(separate_dice)
            msg = f"""Rolling `{self.dice_str.strip()}`:
```{separate_dice}```
**Result:  `{result}`**
**HR: `{highest}`**"""
            if len(gather) == 1 and gather.pop() >= 6:
                msg += '\n**💥Crit!💥**'
            await self._say(msg)
        except ValueError:
            await self._say(f'{self.dice_str} is not a valid roll, try again human.')
