# NightShiftDice Dicebot

Made for a personal Discord where I play Tabletop RPGS.

## Supporting a New System

- All new systems should be contained within a single class that extends `RollClass`.
  - Add that class in a new file inside `roll_classes/`
- The new class must override `roll()` 
- The new class needs to define a regex using `__roll_macro__` for matching messages
  - This regex must be unique to the roll class!
- The contents of the message from the user (after stripping what was in the macro) will be available in `self.dice_str`
- **Optional, but recommended:**  Create an option for `help` for your dice class too!

Once you've created your class and done the above, it should get picked up automatically by the dicebot!

## Usage in Discord

Ping the bot + "help" for info
