# Deploying AI News Pipeline on a VPS

This guide explains how to run the AI News Pipeline on your own Virtual Private Server (VPS) using Docker Compose. The steps have been verified on **Debian 12 (Bookworm)** and are also compatible with Ubuntu-based distributions and other recent Debian derivatives.

## 1. Prepare the VPS

1. **Update system packages**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. **Install Docker Engine and Docker Compose plugin**
   ```bash
   sudo apt install -y ca-certificates curl gnupg
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
   Verify Docker is working:
   ```bash
   sudo docker run hello-world
   ```

3. **(Optional) Manage Docker as a non-root user**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

## 2. Obtain the Project

Clone the repository to your VPS:
```bash
cd ~
git clone https://github.com/your-org/ai-news-pipeline.git
cd ai-news-pipeline
```
Replace the repository URL with the correct one if it differs.

## 3. Configure Environment Variables

By default, `docker-compose.yml` sets up PostgreSQL and Redis containers along with the FastAPI backend and a Celery worker. You can override default credentials by creating an `.env` file in the project root:

```bash
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
```

Update the `DATABASE_URL` in `docker-compose.yml` or provide it via environment variables if you change credentials.

## 4. Build and Run the Services

From the project root run:
```bash
docker compose up --build -d
```
This command downloads the required images, builds the backend container, and starts all services (PostgreSQL, Redis, API, and Celery worker) in detached mode.

Access the application in your browser at `http://<VPS_IP>:8000/`.

## 5. Set Up Reverse Proxy (Optional)

To expose the service on your domain name and handle TLS, you can use a reverse proxy like Nginx or Traefik. A minimal Nginx configuration might look like:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

After configuring Nginx, restart the service:
```bash
sudo systemctl restart nginx
```

For HTTPS, consider setting up [Let's Encrypt](https://certbot.eff.org/) certificates.

## 6. Managing the Stack

- View running containers:
  ```bash
  docker compose ps
  ```
- Follow logs for a service (e.g., backend):
  ```bash
  docker compose logs -f backend
  ```
- Stop the stack:
  ```bash
  docker compose down
  ```

## 7. Persistence and Backups

The default configuration stores PostgreSQL data inside the container, which means data will be lost if the container is removed. For production, mount a volume for persistent storage by editing `docker-compose.yml`:

```yaml
services:
  db:
    ...
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

You may also wish to create regular database backups using `pg_dump` or another tool.

## 8. Updating the Application

To pull the latest changes and rebuild containers:
```bash
git pull
docker compose up --build -d
```

## 9. Troubleshooting

- Use `docker compose logs` to inspect service output.
- Ensure ports `5432`, `6379`, and `8000` are not blocked by your firewall.
- If Celery tasks are not processing, check the `worker` container logs.

This completes the basic setup of the AI News Pipeline on a VPS. Customize the deployment as needed for your production environment.
