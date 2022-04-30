import json
import os
import re

from random import randint, shuffle
from typing import List, Dict

from .RollClass import RollClass

NO_COMBAT = "**`ERROR:  There is no active combat`**"


class VaesenRoll(RollClass):
    __roll_macro__ = "/v"

    pool: int
    result: int
    rolls: List[int]
    successes: int
    inits: Dict[str, int]

    def write_inits_to_file(self):
        with open("inits.json", "w") as i:
            json.dump(self.inits, i)

    def read_inits_from_file(self):
        if not os.path.exists("inits.json"):
            return False
        with open("inits.json", "r") as i:
            self.inits = json.load(i)
        return True

    def show_inits(self):
        if not self.read_inits_from_file():
            return NO_COMBAT
        out_str = "\n".join([f"`{init}`:  **{name}**" for name, init in self.inits.items()])
        return f"**Combat Initiatives:**\n{out_str}"

    def roll(self) -> str:
        """
        /v start [#]        Starts initiative - if num is provided, sets # enemy groups, otherwise 1
        /v show             Shows the current initiative counts
        /v end              Ends the current initiative
        /v swap [name,name] Swaps the initiatives of the two provided names
        /v #                Rolls # dice pool and calculates results
        /v 66               Rolls a "d66" according to Vaesen logic
        """
        if self.dice_str == " help":
            return """**Vaesen RPG Controls**
```/v start[ #]            Starts initiative -- opt. provide # enemies
/v show                 Show initiatives
/v end                  End initiative
/v swap [name], [name]  Swap two initiatives by name
/v #                    Roll # dice and calculate successes
/v 66                   Roll a d66 by Vaesen's logic```"""
        if re.match(r"^ start( \d+)?$", self.dice_str):
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
            return self.show_inits()
        if self.dice_str == " show":
            return self.show_inits()
        if self.dice_str == " end":
            if not os.path.exists("inits.json"):
                return NO_COMBAT
            os.remove("inits.json")
            return f"Combat **ended**!"
        swap_match = re.match(r"^ swap\s+(?P<one>[^,]*)\s*,\s*(?P<two>.*)\s*$", self.dice_str)
        if swap_match:
            if not self.read_inits_from_file():
                return NO_COMBAT
            one = swap_match.groupdict()["one"]
            two = swap_match.groupdict()["two"]
            if one not in self.inits:
                return f"**`ERROR:  {one} is not in the initiative`**"
            if two not in self.inits:
                return f"**`ERROR:  {two} is not in the initiative`**"
            tmp = self.inits[one]
            self.inits[one] = self.inits[two]
            self.inits[two] = tmp
            self.inits = dict(sorted(self.inits.items(), key=lambda x: x[1]))
            self.write_inits_to_file()
            return f"Swapped {one} and {two}!\n{self.show_inits()}"
        self.pool = int(self.dice_str)
        if self.pool == 66:
            self.result = f"{randint(1, 6)}{randint(1, 6)}"
            return f"Rolling 1d66:  **`{self.result}`**"
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)], reverse=True)
        self.successes = self.rolls.count(6)
        return f"Rolling {self.pool} Dice:  `{self.rolls}`\n**Successes: `{self.successes}`**"
