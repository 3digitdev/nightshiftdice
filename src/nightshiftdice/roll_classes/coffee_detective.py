__all__ = ['CoffeeDetective']
from random import shuffle

from .roll_class import RollClass


explain = {
    'RED-HANDED': "Keep this card.  During any other player's scene to which you weren't invited, you may choose to make a dramatic entrance and catch someone in the act",
    'CONFIDANTE': "Show this card to the DETECTIVE and tell them they've been chasing the wrong lead.  Together decide on a new PRIME SUSPECT -- anyone except you!",
    'DOPPELGANGER': 'Pick another character from the table.  You canonically resemble this character enough -- either in face, voice, or silhouette -- to get away with impersonating them in a scene.',
    'THE BIG SLEEP': 'Keep this card.  At a moment of your choosing, you can play it to fall into a coma, to be ended at any sutiably dramatic point.  You may still take turns, but may not re-enter a coma once you awaken.',
    'ALIBI': 'Keep this card.  You have an ironclad alibi for the murder -- you are innocent and cannot be convicted in the final accusation (though you could be an accomplice, or guilty of other crimes)!',
    "DON'T I KNOW YOU?": "Choose another player to 'recognize' from somewhere they ought not to have been.  This can be a recent encounter or a chance meeting in your sordid paths",
    'FATALE': 'If you have a romantic partner, you may play this card at any time to make them take the fall for a crime you committed.',
    "J'ACCUSE": 'This is it!  Inform the DETECTIVE that you have solved the case and state your accusation!',
}


class CoffeeDetective(RollClass):
    __roll_macro__ = '/cd'

    deck: list[str]

    def __init__(self, dice_str: str) -> None:
        super().__init__(dice_str)
        self.build_deck()

    def build_deck(self) -> None:
        self.deck = [
            'RED-HANDED',
            'CONFIDANTE',
            'DOPPELGANGER',
            'THE BIG SLEEP',
            'ALIBI',
            "DON'T I KNOW YOU?",
            'FATALE',
        ]
        shuffle(self.deck)
        self.deck.append("J'ACCUSE")

    async def roll(self) -> None:
        if self.dice_str == 'help':
            await self._say("""**Coffee Detective RPG Controls**
```
/cd         Draw the next card in the deck.  If the deck is empty, it will reshuffle and draw fresh
/cd reset   Reset the game to a full deck
```
""")
            return
        if self.dice_str == 'reset':
            self.build_deck()
            await self._say('Received command -- starting over!')
            return
        if not self.deck:
            self.build_deck()
        card = self.deck.pop(0)
        await self._dm(f"""You have drawn **{card}**:\n_{explain[card]}_""")
