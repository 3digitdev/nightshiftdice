__all__ = ["Ryuutama"]
import re

from random import randint

from .roll_class import RollClass


class Ryuutama(RollClass):
    __roll_macro__ = "/ryu"

    rolls: list[int]

    async def roll(self) -> None:
        if self.dice_str == "help":
            await self._say("""**Ryuutama RPG Controls**
```
/ryu X Y    Roll two dice with X and Y sides respectively and calculate result
/ryu XY     Alias for ^^^  (Will fail if X or Y are not 4/6/8/10/12/20)
```""")
            return
        dice_reg = re.compile(r"^(4|6|8|10|12|20)\s*(4|6|8|10|12|20)$")
        all_dice = dice_reg.findall(self.dice_str)
        if not all_dice:
            await self._say(f"**ERROR:** unable to parse `{self.dice_str}`.  Dice must be 4/6/8/10/12/20.")
            return
        one, two = [int(x) for x in all_dice[0]]
        first = randint(1, one)
        second = randint(1, two)
        await self._say(f"""Rolling `1d{one} + 1d{two}`:
```{first} + {second}```
**Result:  `{first + second}`**""")
        if first == one and second == two:
            await self._say(":boom::game_die:**CRITICAL HIT!**:game_die::boom:")
        elif first == 1 and second == 1:
            await self._say(""":skull::game_die:**FUMBLE!**:game_die::skull:
:warning: Each party member gets 1 Fumble Point
:warning: Any bonus-granting equipment loses 1 durability""")
        return
