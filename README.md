# AI News Pipeline

This project demonstrates a minimal implementation of an AI assisted news publishing pipeline.

## Requirements
- Docker

## Running Locally

```bash
docker compose up --build
```

Open `http://localhost:8000/` in your browser and submit a news article URL.

## Deployment

For instructions on deploying the stack to a VPS using Docker Compose, see [docs/VPS_SETUP.md](docs/VPS_SETUP.md).

If your server is managed by ISPConfig with Apache, you can clone the repository directly inside your web root, for example `/var/www/clients/client0/web1/`, and run Docker from there. See [docs/APACHE_SETUP.md](docs/APACHE_SETUP.md) for details.
