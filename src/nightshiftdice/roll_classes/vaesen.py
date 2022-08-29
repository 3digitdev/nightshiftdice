__all__ = ["Vaesen"]
import json
import os
import re

from random import randint, shuffle
from typing import List, Dict

from .roll_class import RollClass

NO_COMBAT = "**`ERROR:  There is no active combat`**"


class Vaesen(RollClass):
    __roll_macro__ = "/v"

    pool: int
    result: int
    rolls: List[int]
    successes: int
    inits: Dict[str, int]

    def write_inits_to_file(self) -> None:
        with open("inits.json", "w") as i:
            json.dump(self.inits, i)

    def read_inits_from_file(self) -> bool:
        if not os.path.exists("inits.json"):
            return False
        with open("inits.json", "r") as i:
            self.inits = json.load(i)
        return True

    def show_inits(self) -> str:
        if not self.read_inits_from_file():
            return NO_COMBAT
        out_str = "\n".join([f"`{init}`:  **{name}**" for name, init in self.inits.items()])
        return f"**Combat Initiatives:**\n{out_str}"

    async def roll(self) -> None:
        if self.dice_str == "help":
            await self._say("""**Vaesen RPG Controls**
```/v start[ #]            Starts initiative -- opt. provide # enemies
/v show                 Show initiatives
/v end                  End initiative
/v swap [name], [name]  Swap two initiatives by name
/v #                    Roll # dice and calculate successes
/v 66                   Roll a d66 by Vaesen's logic```""")
            return
        if re.match(r"^start( \d+)?$", self.dice_str):
            # Start initiative
            parts = self.dice_str.strip(" ").split(" ")
            enemies = int(parts[1]) if len(parts) > 1 else 1
            names = ["Astrid", "Wilhelm", "Rina", "Torsten", *[f"Enemy Group {k+1}" for k in range(enemies)]]
            shuffle(names)
            numbers = list(range(1, 11))
            shuffle(numbers)
            self.inits = dict(sorted(
                {name: numbers[i] for i, name in enumerate(names)}.items(),
                key=lambda x: x[1]
            ))
            self.write_inits_to_file()
            await self._say(self.show_inits())
            return
        if self.dice_str == "show":
            await self._say(self.show_inits())
            return
        if self.dice_str == "end":
            if not os.path.exists("inits.json"):
                await self._say(NO_COMBAT)
                return
            os.remove("inits.json")
            await self._say(f"Combat **ended**!")
            return
        swap_match = re.match(r"^swap\s+(?P<one>[^,]*)\s*,\s*(?P<two>.*)\s*$", self.dice_str)
        if swap_match:
            if not self.read_inits_from_file():
                await self._say(NO_COMBAT)
                return
            one = swap_match.groupdict()["one"]
            two = swap_match.groupdict()["two"]
            if one not in self.inits:
                await self._say(f"**`ERROR:  {one} is not in the initiative`**")
                return
            if two not in self.inits:
                await self._say(f"**`ERROR:  {two} is not in the initiative`**")
                return
            tmp = self.inits[one]
            self.inits[one] = self.inits[two]
            self.inits[two] = tmp
            self.inits = dict(sorted(self.inits.items(), key=lambda x: x[1]))
            self.write_inits_to_file()
            await self._say(f"Swapped {one} and {two}!\n{self.show_inits()}")
            return
        self.pool = int(self.dice_str)
        if self.pool == 66:
            self.result = int(f"{randint(1, 6)}{randint(1, 6)}")
            await self._say(f"Rolling 1d66:  **`{self.result}`**")
            return
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)], reverse=True)
        self.successes = self.rolls.count(6)
        await self._say(f"Rolling {self.pool} Dice:  `{self.rolls}`\n**Successes: `{self.successes}`**")
