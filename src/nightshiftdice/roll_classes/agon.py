__all__ = ['Agon']
import re

from random import randint

from .roll_class import RollClass


class Agon(RollClass):
    __roll_macro__ = '/ag(?:on)?'

    async def roll(self) -> None:
        if self.dice_str == 'help':
            await self._say("""**Agon RPG Controls**
```
/ag 1d8+1d10+1d6[ vs #]  Roll a dice pool (opt. against a TN)
/ag 8+10+6[ vs #]        Same as above, shorthand
/ag 8106[v#]             For lazy people.
```""")
            return
        # This regex will pop all "dice" rolls like +XdY into a tuple of (# dice, faces)
        dice_reg = re.compile(r'(\d*)d((?:4|6|8|10|12)+)')
        all_dice = dice_reg.findall(self.dice_str)
        try:
            vs_reg = re.compile(r'\s*vs?\s*(\d+)')
            tn = int(vs_reg.findall(self.dice_str)[0])
        except (IndexError, ValueError):
            tn = 0
        dice_results = []
        d4_results = []
        for count, sides in all_dice:
            # We iterate through separately here so that we can show
            # the result of each individual dice in the roll
            for _ in range(int((count or 1))):
                result = randint(1, int(sides))
                (d4_results if int(sides) == 4 else dice_results).append(result)
        if not dice_results:
            await self._say('🚨 Detected invalid roll')
            return
        best = sum(sorted(dice_results)[-2:])
        d4 = max(d4_results or [0])
        out = f"""Rolling `{self.dice_str.strip()}`:
```Dice Pool: {', '.join(str(d) for d in dice_results)}  (TOTAL: {best})
d4s: {', '.join(str(d) for d in d4_results) if d4_results else 'None'}  (BEST: {d4})
```
**Result(s):  `{best + d4}`**"""
        if tn:
            result = '🎉 Prevail 🎉' if (best + d4) >= tn else '⚡️ Suffer ⚡️'
            out += f'\nVersus **`{tn}`**:   **{result}**'
        await self._say(out)
