FROM python:3.10.7
RUN pip install pipenv
WORKDIR /app/
COPY Pipfile \
    Pipfile.lock \
    /app/
RUN pipenv sync
ADD /stepbot stepbot/
COPY bot.py \
    credentials.json \
    /app/
CMD pipenv run python3 bot.py