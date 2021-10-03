from random import randint
from typing import List

from roll_classes.RollClass import RollClass


class VaesenRoll(RollClass):
    __roll_macro__ = "/v"

    pool: int
    result: int
    rolls: List[int]
    successes: int

    def roll(self) -> str:
        self.pool = int(self.dice_str)
        if self.pool == 66:
            self.result = randint(1, 66)
            return f"Rolling 1d66:  **`{self.result}`**"
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)], reverse=True)
        self.successes = self.rolls.count(6)
        return f"Rolling {self.pool} Dice:  `{self.rolls}`\n**Successes: `{self.successes}`**"
