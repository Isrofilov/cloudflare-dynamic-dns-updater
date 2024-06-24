# Cloudflare Dynamic DNS Updater

This Python script updates the A record of a specified subdomain in Cloudflare with your server's current external IP address. Designed to run in a Docker container, it periodically checks for IP changes every 5 minutes.

 ### How It Works

1. **Get External IP**: The script retrieves the current external IP using the `https://api.ipify.org` service.
2. **Check DNS Record**: It verifies the current A record for the specified subdomain in Cloudflare.
3. **Update if Necessary**: If the external IP has changed, the script updates the A record in Cloudflare.
4. **Repeat**: This process repeats every 5 minutes.

### Prerequisites

- Docker
- Docker Compose
- Cloudflare API Token with DNS Edit permissions

### Configuration

To set up the Cloudflare Dynamic DNS Updater service, create a `docker-compose.yml` file using the template below. Replace the placeholder values with your actual configuration details.

```yml
version: '3.8'
services:
  updater:
    image: isrofilov/cloudflare-dynamic-dns-updater:latest
    environment:
        - API_TOKEN=your_cloudflare_api_token_here
        - ZONE=your_domain_here
        - SUBDOMAIN=your_subdomain_here
        - PROXIED=true_or_false_here
```

Here's what you need to replace:

- `your_cloudflare_api_token_here`: Your actual Cloudflare API Token with DNS Edit permissions.
- `your_domain_here`: Your domain (e.g., example.com).
- `your_subdomain_here`: Your subdomain (e.g., subdomain). If not specified, the main domain (example.com) will be updated; if specified, it updates SUBDOMAIN.example.com.
- `true_or_false_here`: Set to `true` if you want Cloudflare to proxy the traffic, or `false` if not.

### Getting Started

To start the Cloudflare Dynamic DNS Updater, navigate to the directory containing your `docker-compose.yml` and run:

```bash
docker-compose up -d
```

### Support

For support, feature requests, or bug reporting, please open an issue on the GitHub repository.