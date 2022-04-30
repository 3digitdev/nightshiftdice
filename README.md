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

## Running the Bot

Running the bot requires that you have a Discord API Token to provide.

This token must be supplied via env variable `DISCORD_TOKEN` (the bot will throw an error without it)

### Locally

The bot runs using `poetry`:

```bash
# install poetry
python3 -m pip install poetry
# Install dependencies
poetry install
# Run the bot
poetry run bot
```

### Docker

There is a `Dockerfile` ready to go for the bot already!

If you have the `DISCORD_TOKEN` env variable already set locally, you can easily achieve this with:
```bash
# Build the docker image
docker build -t nightshiftdice .
# Run the docker image, providing the token
docker run -e DISCORD_TOKEN=$DISCORD_TOKEN nightshiftdice

# ALTERNATE: Provide the token manually
docker run -e DISCORD_TOKEN=<your_discord_token> nightshiftdice
```
