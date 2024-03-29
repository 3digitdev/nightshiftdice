__all__ = ['PolyDice']
import re

from random import randint
from typing import List

from .roll_class import RollClass

# A mapping of the supported operators for dice rolls,
# mapped to their respective modifiers to multiply the result by
# (so '-' maps to -1 so that N * -1 = -N, so that we can just sum results
OPS = {'+': 1, '-': -1, '': 1}


def parse_roll(roll_str: str, separate_dice: List[List[int]], results: List[int]) -> (List[int], List[int]):
    # This regex will pop all "dice" rolls like +XdY into a tuple of (op, # dice, faces)
    dice_reg = re.compile(r'([+-])?(\d)d(\d+)')
    all_dice = dice_reg.findall(roll_str)
    actual_dice = []
    dice_results = []
    for op, count, sides in all_dice:
        # We iterate through separately here so that we can show
        # the result of each individual dice in the roll
        for _ in range(int(count)):
            result = randint(1, int(sides))
            actual_dice.append(result)
            dice_results.append(result * OPS[op])
    # This regex will pop any remaining non-dice ('modifiers') into a tuple of (op, modifier)
    mod_reg = re.compile(r'([+-])(\d+)(?!d)')
    mod_result = [int(mod) * OPS[op] for op, mod in mod_reg.findall(roll_str)]
    separate_dice.append(actual_dice)
    results.append(sum(dice_results + mod_result))
    return separate_dice, results


class PolyDice(RollClass):
    __roll_macro__ = '/r(?:oll)?'

    async def roll(self) -> None:
        # Parses format of <number>x[<roll_string>]
        mult_reg = re.compile(r'(\d+)[x\*]\[((?:[+-]?\dd\d+)*(?:[+-]\d+(?!d))?)\]')
        mult_dice = mult_reg.findall(self.dice_str)
        separate_dice = []
        results = []
        if mult_dice:
            for _ in range(int(mult_dice[0][0])):
                separate_dice, results = parse_roll(mult_dice[0][1], separate_dice, results)
        else:
            dice_rolls = re.split(r',\w*', self.dice_str)
            for roll in dice_rolls:
                separate_dice, results = parse_roll(roll, separate_dice, results)
        await self._say(f"""Rolling `{self.dice_str.strip()}`:
```{separate_dice if len(separate_dice) > 1 else separate_dice[0]}```
**Result(s):  `{results if len(results) > 1 else results[0]}`**
""")
