FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry==1.4.2

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "main"]

