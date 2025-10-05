__all__ = ['Wildsea']
import re

from random import randint

from .roll_class import RollClass


class Wildsea(RollClass):
    __roll_macro__ = '/ws?'

    async def roll(self) -> None:
        emoji = ['zero', 'one', 'two', 'three', 'four', 'five', 'six']
        if self.dice_str == 'help':
            await self._say("""**Wildsea RPG Controls**
```
/ws #          Roll # dice and display result + doubles
/ws X c[ut] Y  Roll X dice and cut the highest Y before tallying
/ws XcY        Same as above, shortcutted
```""")
        else:
            reg = re.compile(r'(\d+)(?: ?(?:c(?:ut)?)? ?(\d+))?')
            try:
                match = reg.findall(self.dice_str)[0]
                dice = int(match[0])
                cut = int(match[1] or 0)
                rolls = sorted([randint(1, 6) for _ in range(dice)])
                final_rolls, cut_rolls = rolls[: len(rolls) - cut], rolls[len(rolls) - cut :]
                highest_double = max([n for n in final_rolls if final_rolls.count(n) > 1] or [0])
                await self._say(f"""Rolling {dice} dice{f', cutting {cut}' if cut > 0 else ''}:

**Rolls:** {', '.join(str(r) for r in final_rolls)}{f' :scissors: ~~{', '.join(str(r) for r in cut_rolls)}~~' if cut_rolls else ''}
**Results: :{emoji[max(final_rolls)]}: {f'plus double :{emoji[highest_double]}:s' if highest_double > 0 else '(_no doubles_)'}**
""")
            except ValueError:
                await self._say(f'{self.dice_str} is not a valid roll, try again human.')
