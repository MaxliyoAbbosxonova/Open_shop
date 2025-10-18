FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY ./ /app

COPY . .

# kutubxonalarni o‘rnatish
RUN uv sync --frozen --no-cache
CMD ["uv", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]

