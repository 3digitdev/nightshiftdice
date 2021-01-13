class RollClass:
    # This is needed in each class, defining how to parse the message
    __roll_macro__ = None

    def __init__(self, dice_str: str):
        self.dice_str = dice_str

    def roll(self) -> str:
        """
        Takes the basic roll string and parses it for the specific roll class
        Returns a string of the message to be returned to the channel
        """
        pass