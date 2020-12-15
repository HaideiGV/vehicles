FROM python:3.7-alpine

WORKDIR /app
COPY . .

RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add --no-cache  \
    bash build-base gcc && \
    pip install --no-cache-dir pip-tools==5.2.1 && \
    pip install --no-cache-dir -r requirements.txt


EXPOSE 8000
CMD ["uvicorn", "run:app", "--host", "127.0.0.1", "--port", "8000"]
