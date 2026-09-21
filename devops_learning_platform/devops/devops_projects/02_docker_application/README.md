# Docker Application

A minimal containerized Python HTTP service.

## Run

```powershell
docker build -t devops-python-app .
docker run --rm -p 8000:8000 devops-python-app
```

Or use Docker Compose:

```powershell
docker compose up --build
```

Open `http://localhost:8000` after the container starts.
