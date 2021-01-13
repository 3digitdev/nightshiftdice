FROM python:3.8.7-slim

RUN mkdir dicebot
WORKDIR dicebot
COPY main.py requirements.txt ./
COPY roll_classes/ ./roll_classes
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]