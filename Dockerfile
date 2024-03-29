FROM python:3.12-slim

RUN pip install poetry~=1.4.0
RUN mkdir dicebot
WORKDIR dicebot
COPY src/ ./src
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

ENTRYPOINT ["poetry", "run", "bot"]
