FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

# Alembic 마이그레이션 스크립트 추가
COPY alembic.ini .
COPY alembic ./alembic

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]