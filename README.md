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

Running the bot requires several environment variables:

- `DISCORD_TOKEN`:  The Discord Bot Token for your bot
- `GPT_ORG`:  The organization ID for your OpenAI API Account
- `GPT_KEY`:  The API Key for your OpenAI API Account

The bot will throw an error if any of these have not been supplied.

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

If you have the env variables already set locally, you can easily achieve this with:
```bash
# Build the docker image
docker build -t nightshiftdice .
# Run the docker image, providing the required variables
docker run -e DISCORD_TOKEN=$DISCORD_TOKEN -e GPT_ORG=$GPT_ORG -e GPT_KEY=$GPT_KEY nightshiftdice

# ALTERNATE: Provide the variables manually
docker run -e DISCORD_TOKEN=<your_discord_token> -e GPT_ORG=<org> -e GPT_KEY=<key> nightshiftdice
```
