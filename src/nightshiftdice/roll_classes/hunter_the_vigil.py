__all__ = ["HunterVigil"]
from random import randint

from .roll_class import RollClass


class HunterVigil(RollClass):
    __roll_macro__ = "/h"

    pool: list[int]
    explode: list[int] = [10]

    def print_result(self, rolls) -> str:
        result = ''
        longest = max([len(x) for x in rolls])
        for idx in range(longest):
            for roll_list in rolls:
                space = ' ' if max(roll_list) < 10 else '  '
                try:
                    roll = roll_list[idx]
                    result += f"{roll}{space if roll < 10 else ' '}"
                except IndexError:
                    result += f" {space}"
            result += '\n'
        return result

    async def roll(self) -> None:
        if self.dice_str == "help":
            await self._say("""**Hunter: The Vigil RPG Controls**
```
/h #     Roll # dice and calculate total successes (10's explode)
/h #!    Same as above, but 9's also explode
/h #!!   Same as above, but 8's and 9's also explode
```""")
            return
        bang_count = self.dice_str.count('!')
        if bang_count > 0:
            self.explode.append(9)
        if bang_count > 1:
            self.explode.append(8)
        final_rolls: list[list[int]] = []
        total_dice = int(self.dice_str.replace('!', ''))
        self.pool = [randint(1, 10) for _ in range(total_dice)]
        for roll in self.pool:
            if roll not in self.explode:
                final_rolls.append([roll])
                continue
            x = [roll]
            while roll in self.explode:
                roll = randint(1, 10)
                x.append(roll)
            final_rolls.append(x)
        results = self.print_result(final_rolls)
        successes = len([a for sub in final_rolls for a in sub if a >= 8])
        extra = ''
        if successes == 0:
            extra = ':skull: **Failure** :skull:'
        if successes >= 5:
            extra = ':tada: **Exceptional Success** :tada:'
        await self._say(f"""Results: (vertical = exploding, {self.explode}):
```{results}```
**Total Successes:  {successes}**
{extra}
""")
