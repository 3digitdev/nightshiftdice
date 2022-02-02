import collections
from random import randint, shuffle
from typing import List

from roll_classes.RollClass import RollClass


explain = {
    "RED-HANDED": "Keep this card.  During any other play'ers scene to which you weren't invited, you may choose to make a dramatic entrance and catch someone in the act",
    "CONFIDANTE": "Show this card to the DETECTIVE and tell them they've been chasing the wrong lead.  Together decide on a new PRIME SUSPECT -- anyone except you!",
    "DOPPLEGANGER": "Pick another character from the table.  You canonically resemble this character enough -- either in face, voice, or silhouette -- to get away with impersonating them in a scene.",
    "THE BIG SLEEP": "Keep this card.  At a moment of your choosing, you can play it to fall into a coma, to be ended at any sutiably dramatic point.  You may still take turns, but may not re-enter a coma once you awaken.",
    "ALIBI": "Keep this card.  You have an ironclad alibi for the murder -- you are innocent and cannot be convicted in the final accusation (though you could be an accomplice, or guilty of other crimes)!",
    "DON'T I KNOW YOU?": "Choose another player to \"recognize\" from somewhere they ought not to have been.  This can be a recent encounter or a chance meeting in your sordid paths",
    "FATALE": "If you have a romantic partner, you may play this card at any time to make them take the fall for a crime you committed.",
    "J'ACCUSE": "This is it!  Inform the DETECTIVE that you have solved the case and state your accusation!"
}


class CoffeeRoll(RollClass):
    __roll_macro__ = "/cd"

    def __init__(self, dice_str: str):
        super().__init__(dice_str)
        self.build_deck()

    def build_deck(self):
        self.deck = [
            "RED-HANDED",
            "CONFIDANTE",
            "DOPPLEGANGER",
            "THE BIG SLEEP",
            "ALIBI",
            "DON'T I KNOW YOU?",
            "FATALE"
        ]
        shuffle(self.deck)
        self.deck.append("J'ACCUSE")

    def roll(self) -> str:
        print(self.dice_str)
        if self.dice_str == " reset":
            self.build_deck()
            return f"Received command -- starting over!"
        if not self.deck:
            print("Starting over")
            self.build_deck()
        card = self.deck.pop(0)
        return f"""You have drawn **{card}**:\n_{explain[card]}_"""
