FROM python:3.13-slim

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ENV PYTHONPATH=/src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd -m user && \
    mkdir -p /src && \
    chown -R user:user /src

COPY --chown=user:user . .

USER user


CMD ["sh", "-c", "alembic upgrade head && python app/main.py"]