__all__ = ['TrophyGold']

from random import randint

from .roll_class import RollClass


class TrophyGold(RollClass):
    __roll_macro__ = '/tg'

    rolls: list[int]

    async def roll(self) -> None:
        if self.dice_str == 'help':
            await self._say("""**Trophy Gold RPG Controls**
```
/tg [hunt|risk|combat|helping|contest]  --  The bot will describe how this type of roll works
/tg L D    Rolls <L> Light dice and <D> Dark Dice (if only rolling one of them use 0 for the other)
```""")
            return
        if self.dice_str == 'hunt':
            await self._say("""When you press ever deeper in pursuit of a specific and immediate goal (either the Set Goal, or a separate goal you define with the gm), say how you are exploring your environment, then gather dice:
---------------
- Take 1 **Light Dice** by default
- Take 1 **Light Dice** if you have a skill/equipment that helps you.  Only can be taken once.
- Roll the dice with `/tg <dice>`
- If highest **Light Dice** is:
  - 1:  You lose all Hunt Tokens; encounter something terrible.
  - 2-3:  You encounter something terrible.
  - 4-5:  You gain 1 Hunt Token; encounter something terrible.
  - 6:  You gain 1 Hunt Token""")
            return
        if self.dice_str == 'risk':
            await self._say("""When you attempt a risky task, say what you hope will happen, and ask the gm and the other players what could possibly go wrong. Then gather dice:
---------------
- Take 1 **Light Dice** if the task is something you're skilled at (Background/Occupation).  Only can be taken once.
- Take 1 **Light Dice** for accepting a Devil's Bargain with another player or GM.
- Take 1 **Dark Dice** if you risk body/mind on the task. (Rituals always take this)
- If highest dice is:
  - 1-3:  You fail, and things get worse
  - 4-5:  You succeed, but with a complication
  - 6:  You succeed with no issue.  Describe the success.
- **NOTE:** _If your highest dice is **Dark**, and it's higher than your **Ruin**, mark 1 **Ruin**
- If you are unhappy with the roll and your highest dice is **Light**, add 1 **Dark Dice** and reroll.  You can do this until your highest dice is **Dark**.
""")
            return
        if self.dice_str == 'combat':
            await self._say("""When you attempt to defeat a monster, you and fellow adventurers band together to fight it:
- Each adventurer rolls 1 **Light Dice**.  This value is that adventurer's **Weak Point**.  Make note of them.
- Gather 1 **Dark Dice** for each character involved in the attack
- State your weapon, then roll the **Dark Dice** you gathered
- If the 2 highest dice sum to greater or equal the monster's **Endurance**, you defeat the monster
- If any **Dark Dice** match a character's **Weak Point**, they mark 1 **Ruin** for EACH **Dark Dice** that matches
  - A player may mark 1 piece of armor to ignore all damage for a single roll.  That armor is unusable until you return to town.
- If a player retreats, another player must roll their **Weak Point** dice and apply it to themselves (must be different than first **Weak Point**)
- If the 2 highest dice sum to LESS than the monster's **Endurance**, add another **Dark Dice** and roll to attack again.
""")
            return
        if self.dice_str == 'helping':
            await self._say("""If another player is making a Risk Roll that includes at least one dark die, you may offer help before **or after** they roll.
- If they accept, roll 1 **Light Dice**
- Your dice is added to their result
- If your dice matches ANY of their **Dark Dice**, mark 1 **Ruin**
- If player rerolls, your roll does not help again (you must take this action again and risk more Ruin)""")
            return
        if self.dice_str == 'contest':
            await self._say("""If two treasure hunters act against each other, roll a Contest Roll.  Agree on what's at stake, then gather dice:
- Take 1 **Light Dice** if your Background/Occupation would make you skilled at this.  Only can be taken once.
- Take 1 **Light Dice** for each mark of **Ruin** you have
- Take 1 **Dark Dice** if the contest itself is inherently deadly/dangerous
- Take as many additional **Dark Dice** as you are willing to risk
- Count all the 6s you roll.  Whoever has the most wins. In case of tie, then count 5's, then 4's, etc.
- For each **Dark Dice** you rolled that's a 1, mark 1 **Ruin**""")
            return
        dice_txt = self.dice_str.split(' ')
        light, dark = [int(x) for x in dice_txt]
        light_rolls = [randint(1, 6) for _ in range(light)]
        dark_rolls = [randint(1, 6) for _ in range(dark)]
        await self._say(f"""Rolling `{light}` Light and `{dark}` Dark Dice:
```Light:  {list(reversed(sorted(light_rolls)))}
 Dark:  {list(reversed(sorted(dark_rolls)))}```""")
        return
