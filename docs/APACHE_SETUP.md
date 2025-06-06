# Running with Apache and ISPConfig

This guide explains how to start the AI News Pipeline when your server is managed by ISPConfig and Apache serves the site from `/var/www/clients/client0/web1/` (adjust the path if your ISPConfig setup uses a different client or web number).

## 1. Clone the Repository

```
cd /var/www/clients/client0/web1/
git clone https://github.com/your-org/ai-news-pipeline.git
cd ai-news-pipeline
```

The project files now reside within the web root managed by ISPConfig.

## 2. Build and Start the Containers

Run the stack from the project directory:

```
docker compose up --build -d
```

The command downloads images (if necessary) and starts the services in detached mode.

## 3. Permissions

Depending on your ISPConfig configuration, the files in `/var/www/clients/client0/web1/ai-news-pipeline` should typically be owned by `web1:client0`.
If you encounter permission errors, adjust ownership and allow the web user to run Docker:

```
sudo chown -R web1:client0 /var/www/clients/client0/web1/ai-news-pipeline
sudo usermod -aG docker web1   # log out and back in for this to take effect
```

Alternatively, run `sudo docker compose` as `root`.
