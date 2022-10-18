# syntax=docker/dockerfile:1
FROM python:3.8-alpine

WORKDIR /app

ENV TOKEN=""
ENV DB_CONN_STR="mongodb://root:example@mongo/?retryWrites=true&w=majority"
ENV COLOUR="0x0c0f27"
ENV ADMIN_GUILD=""
ENV SPOTIFY_CLIENT_ID=""
ENV SPOTIFY_CLIENT_SECRET=""
ENV REDDIT_CLIENT_ID=""
ENV REDDIT_CLIENT_SECRET=""
ENV REDDIT_USER_AGENT="Discord bot v{}"
ENV SENTRY_URL=""
ENV TOPGG_API_KEY=""
ENV BOTSGG_API_KEY=""
ENV DISCORDBOTLIST_API_KEY=""
ENV DISCORDS_API_KEY=""

COPY . .
COPY lavalink.docker.json lavalink.json

RUN apk add --no-cache gcc g++ musl-dev libffi-dev && \
    pip install pipenv && \
    pipenv install

CMD ["pipenv", "run", "python3", "main.py"]