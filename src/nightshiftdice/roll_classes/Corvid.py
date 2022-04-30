from random import randint
from typing import List

from .RollClass import RollClass


COUNTDOWN = [12, 10, 8, 6, 4]


class CorvidRoll(RollClass):
    __roll_macro__ = "/c"

    pool: int
    rolls: List[int]
    best: int
    h_countdown: int
    c_countdown: int

    def __init__(self, dice_str: str):
        self.h_countdown = 0
        self.c_countdown = 2
        super().__init__(dice_str)


    def roll(self) -> str:
        """
        /c #                Rolls # dice pool and calculates best result
        /c show             Shows countdown dice
        """
        if self.dice_str == " help":
            return """**Corvid Ct RPG Controls**
```/c #     Roll # dice and calculate best result
/c show  Show the countdown dice currently```"""
        if self.dice_str == " show":
            return f"**Countdown Dice:**\nHumans:  `d{COUNTDOWN[self.h_countdown]}`\nCorvids:  `d{COUNTDOWN[self.c_countdown]}`"
        self.pool = int(self.dice_str)
        extra = ""
        if self.pool > 3:
            self.pool = 3
            extra = "(_Cannot roll more than 3 dice!  Dropping to 3._)\n"
        self.rolls = sorted([randint(1, 6) for _ in range(self.pool)], reverse=True)
        self.best = max(self.rolls)
        if self.best < 3:
            result = f":fire: The humans to fight back!"
            hc_result = randint(1, COUNTDOWN[self.h_countdown])
            result += f"\nThe humans roll a `{hc_result}` on their countdown dice!"
            if hc_result < 4:
                self.h_countdown += 1
                result += f"\n    (The human countdown moves forward 1 step to a d{COUNTDOWN[self.h_countdown]}!)"
            if self.h_countdown > 4:
                result += "\n:bangbang: **The humans have finished their countdown!** :bangbang:"
        elif self.best < 5:
            result = ":warning: You succeed but are left in a precarious situation!"
            hc_result = randint(1, COUNTDOWN[self.h_countdown])
            result += f"\nThe humans roll a `{hc_result}` on their countdown dice!"
            if hc_result < 4:
                self.h_countdown += 1
                result += f"\n    (The human countdown moves forward 1 step to a d{COUNTDOWN[self.h_countdown]}!)"
            if self.h_countdown > 4:
                result += "\n:bangbang: **The humans have finished their countdown!** :bangbang:"
            cc_result = randint(1, COUNTDOWN[self.c_countdown])
            result += f"\nThe corvids roll a `{cc_result}` on their countdown dice!"
            if cc_result < 4:
                self.c_countdown += 1
                result += f"\n   (The corvid countdown moves forward 1 step to a d{COUNTDOWN[self.c_countdown]}!)"
            if self.c_countdown > 4:
                result += "\n:bangbang: **The corvids have finished their countdown!** :bangbang:"
        else:
            result = ":tada: You succeed and put the humans on their heels!"
            cc_result = randint(1, COUNTDOWN[self.c_countdown])
            result += f"\nThe corvids roll a `{cc_result}` on their countdown dice!"
            if cc_result < 4:
                self.c_countdown += 1
                result += f"\n   (The corvid countdown moves forward 1 step to a d{COUNTDOWN[self.c_countdown]}!)"
            if self.c_countdown > 4:
                result += "\n:bangbang: **The corvids have finished their countdown!** :bangbang:"
        return f"{extra}Rolling {self.pool} Dice:  `{self.rolls}`\n**Best Result: `{self.best}`**\n{result}"
