# Apache Reverse Proxy Setup

This guide explains how to forward traffic from Apache to the FastAPI backend running on port 8000. The instructions target Debian 12 servers and assume the project lives under a directory typically created by ISPConfig such as `/var/www/clients/client0/web1/`.

## Prerequisites

- Debian 12 with Apache 2 installed
- Docker Engine and Docker Compose

Install Docker if it is not already present:
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
```

Enable the required Apache modules:
```bash
sudo a2enmod proxy proxy_http
```

## Example VirtualHost

Create a site configuration, e.g. `/etc/apache2/sites-available/ainews.conf`:
```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/clients/client0/web1/web

    ProxyPreserveHost On
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
</VirtualHost>
```
This assumes the project files and `docker-compose.yml` are located in `/var/www/clients/client0/web1/`.

## Enable the Site

```bash
sudo a2ensite ainews.conf
sudo systemctl reload apache2
```
After reloading Apache, requests to `example.com` will be forwarded to the FastAPI service.

## Running from ISPConfig Web Root

If your server is managed by ISPConfig with Apache, you can clone the repository directly inside your web root and run Docker from there:

```bash
cd /var/www/clients/client0/web1/
git clone https://github.com/your-org/ai-news-pipeline.git
cd ai-news-pipeline
docker compose up --build -d
```

The command downloads images (if necessary) and starts the services in detached mode.

### Permissions

Depending on your ISPConfig configuration, the files in `/var/www/clients/client0/web1/ai-news-pipeline` should typically be owned by `web1:client0`. If you encounter permission errors, adjust ownership and allow the web user to run Docker:

```bash
sudo chown -R web1:client0 /var/www/clients/client0/web1/ai-news-pipeline
sudo usermod -aG docker web1   # log out and back in for this to take effect
```

Alternatively, run `sudo docker compose` as `root`.
