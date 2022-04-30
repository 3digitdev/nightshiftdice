import re

from random import randint

from .RollClass import RollClass


class PolyDice(RollClass):
    __roll_macro__ = "/r(?:oll)?"

    def roll(self) -> str:
        ops = {"+": 1, "-": -1, "": 1}
        dice_reg = re.compile(r"(?P<op>[+-])?(?P<count>\d)d(?P<sides>\d+)")
        mod_reg = re.compile(r"(?P<op>[+-])(?P<count>\d+)(?!d)")
        all_dice = dice_reg.findall(self.dice_str)
        actual_dice = []
        dice_results = []
        for op, count, sides in all_dice:
            for _ in range(int(count)):
                result = randint(1, int(sides))
                actual_dice.append(result)
                dice_results.append(result * ops[op])
        mod_result = [int(mod) * ops[op] for op, mod in mod_reg.findall(self.dice_str)]
        return f"""Rolling `{self.dice_str.strip()}`:
```{actual_dice}```
**Result:  `{sum(dice_results + mod_result)}`**
"""
