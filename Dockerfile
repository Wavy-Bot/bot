# syntax=docker/dockerfile:1
FROM golang:alpine

WORKDIR /app
COPY . .
RUN go mod download

# TODO(Robert): Update env vars
ENV DEBUG=false
ENV TOKEN=""
ENV ADMIN_GUILD=""

ENV EMB_COLOUR=13774433
ENV EMB_ERR_COLOUR=16399360

ENV SUPPORT_SERVER_URL="https://discord.wavybot.com"

RUN go get -d -v . && \
    go build -o wavy cmd/wavy/main.go

CMD ["/app/wavy"]