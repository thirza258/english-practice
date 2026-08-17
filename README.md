# English Practice Diagnostic

A Django template app for a hidden-topic English grammar diagnostic.

The question generator uses the OpenAI Python SDK pointed at OpenRouter.
If `OPENROUTER_API_KEY` is not set or the request fails, the app falls back to the local question bank so the UI still works.

## Run locally

```bash
python3 -m pip install -r requirements.txt
export OPENROUTER_API_KEY="your_openrouter_api_key"
export OPENROUTER_MODEL="openai/gpt-4o-mini"
python manage.py migrate
python manage.py runserver 0.0.0.0:5170
```

Open `http://localhost:5170/`.

The landing page is at `/`, and the diagnostic itself lives at `/test/`.

## Run in Docker

```bash
docker build -t english-practice .
docker run --rm -p 5170:5170 \
  -e DJANGO_SECRET_KEY=change-me \
  -e DJANGO_ALLOWED_HOSTS='*' \
  -e OPENROUTER_API_KEY=your_openrouter_api_key \
  -e OPENROUTER_MODEL=openai/gpt-4o-mini \
  english-practice
```

Or use Docker Compose:

```bash
docker compose up --build
```

The app listens on port `5170` in both local and containerized runs.

The SQLite question bank is stored in `data/db.sqlite3` so Docker runs can persist generated questions across restarts when the `data/` volume is mounted.

The active test session is stored in the same SQLite database through a Django model, so the current test can be restored after restarts as long as `data/db.sqlite3` remains in place.
