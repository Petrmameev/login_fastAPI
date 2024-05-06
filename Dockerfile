FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# COPY pyproject.toml poetry.lock* /app/
COPY requirements.txt /app/
# RUN pip install poetry && poetry install --no-root
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]