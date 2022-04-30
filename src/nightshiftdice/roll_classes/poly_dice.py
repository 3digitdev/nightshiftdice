__all__ = ["PolyDice"]
import re

from random import randint

from .roll_class import RollClass

# A mapping of the supported operators for dice rolls,
# mapped to their respective modifiers to multiply the result by
# (so '-' maps to -1 so that N * -1 = -N, so that we can just sum results
OPS = {"+": 1, "-": -1, "": 1}


class PolyDice(RollClass):
    __roll_macro__ = "/r(?:oll)?"

    async def roll(self) -> None:
        # This regex will pop all "dice" rolls like +XdY into a tuple of (op, # dice, faces)
        dice_reg = re.compile(r"([+-])?(\d)d(\d+)")
        all_dice = dice_reg.findall(self.dice_str)
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
        mod_reg = re.compile(r"([+-])(\d+)(?!d)")
        mod_result = [int(mod) * OPS[op] for op, mod in mod_reg.findall(self.dice_str)]
        await self._say(f"""Rolling `{self.dice_str.strip()}`:
```{actual_dice}```
**Result:  `{sum(dice_results + mod_result)}`**
""")
