__all__ = ["CorvidCourt"]
from random import randint

from .roll_class import RollClass


COUNTDOWN = [12, 10, 8, 6, 4]


class CorvidCourt(RollClass):
    __roll_macro__ = "/cc"

    pool: int
    rolls: list[int]
    best: int
    h_countdown: int
    c_countdown: int

    def __init__(self, dice_str: str) -> None:
        self.h_countdown = 0
        self.c_countdown = 2
        super().__init__(dice_str)

    async def roll(self) -> None:
        """
        /c #                Rolls # dice pool and calculates best result
        /c show             Shows countdown dice
        """
        if self.dice_str == "help":
            await self._say("""**Corvid Court RPG Controls**
```
/cc #     Roll # dice and calculate best result
/cc show  Show the countdown dice currently
```""")
            return
        if self.dice_str == "show":
            await self._say(f"**Countdown Dice:**\nHumans:  `d{COUNTDOWN[self.h_countdown]}`\nCorvids:  `d{COUNTDOWN[self.c_countdown]}`")
            return
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
        await self._say(f"{extra}Rolling {self.pool} Dice:  `{self.rolls}`\n**Best Result: `{self.best}`**\n{result}")
