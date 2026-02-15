# A4 Shiny Apps

## Local Run (venv)

Use the project virtual environment and run Shiny Express via the CLI.

```powershell
.\.venv\Scripts\python.exe -m shiny run --reload a4_ex1\app.py
.\.venv\Scripts\python.exe -m shiny run --reload a4_ex2\app.py
```

If you see `ModuleNotFoundError`, confirm you are using the venv and install the missing package into it.

## Docker

Build the image:

```powershell
docker build -t a4-shiny .
```

Run exercise 1 (default):

```powershell
docker run --rm -p 8000:8000 a4-shiny
```

Run exercise 2:

```powershell
docker run --rm -p 8000:8000 -e APP_PATH=a4_ex2/app.py a4-shiny
```

The app will be available at `http://127.0.0.1:8000`.

## Docker Compose (two apps)

Start both apps:

```powershell
docker compose up -d --build
```

Stop them:

```powershell
docker compose down
```

Ports:

- Exercise 1: `http://127.0.0.1:8000`
- Exercise 2: `http://127.0.0.1:8001`
