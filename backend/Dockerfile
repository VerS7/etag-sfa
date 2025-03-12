FROM python:3.11.11-alpine AS builder

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN python -m venv /app/.venv

RUN apk update && apk add tzdata

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

FROM python:3.11.11-alpine

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

ENV TZ="Europe/Moscow"

COPY . .
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/share/zoneinfo/Europe/Moscow /usr/share/zoneinfo/Europe/Moscow

RUN apk update --no-cache && apk add --no-cache ca-certificates

EXPOSE 3000

ENTRYPOINT [ "python", "src/main.py" ]


