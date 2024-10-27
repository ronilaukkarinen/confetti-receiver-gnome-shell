
# Confetti Trigger Service for GNOME with Cloudflare Tunnel

This project allows you to trigger a confetti animation in the GNOME Shell environment by sending a POST request to a public URL, thanks to Cloudflare Tunnel and a Python HTTP server.

## Requirements

- [confetti-gnome-shell-extension](https://github.com/ronilaukkarinen/confetti-gnome-shell-extension/)
- **Python 3**
- **dbus-x11** package (for D-Bus session access)
- **Cloudflare account** (for managing DNS and tunnel)
- **cloudflared** (Cloudflare Tunnel client)

## Installation and setup

### Install dependencies

Install `dbus-x11` and `cloudflared` if they are not already installed.

```bash
sudo apt install dbus-x11
sudo apt install cloudflared
```

### Authenticate Cloudflared

Log in to Cloudflare using `cloudflared` to authenticate and create a credentials file.

```bash
cloudflared tunnel login
```

This will open a browser window for you to log in to your Cloudflare account.

### Create the Cloudflare tunnel

Create a tunnel named `confetti`.

```bash
cloudflared tunnel create confetti
```

Note the **tunnel ID** provided after creating the tunnel. This will be used to configure the Cloudflare tunnel.

### Configure the tunnel

Create or edit the Cloudflare Tunnel configuration file at `~/.cloudflared/config.yml`:

Replace `<tunnel-id>` with the tunnel ID from Step 3 and `/home/yourusername/.cloudflared/<tunnel-id>.json` with the path to the credentials file generated earlier.

```yaml
tunnel: confetti
credentials-file: /home/yourusername/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: confetti.yourdomain.com
    service: http://localhost:4769
  - service: http_status:404
```

### Add a CNAME Record in Cloudflare DNS

In your Cloudflare dashboard:

1. Go to **DNS** settings for `yourdomain.com`.
2. Add a **CNAME** record:
   - **Name**: `confetti`
   - **Target**: `<tunnel-id>.cfargotunnel.com`
   - **Proxy Status**: Set to **Proxied** (orange cloud icon).

### Create a systemd service

Save the following as `/etc/systemd/system/confetti-trigger.service` to create a systemd service that runs the Python server script:

```ini
[Unit]
Description=Confetti Trigger Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/trigger_confetti.py
Restart=always
User=yourusername
Environment=DISPLAY=:0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/trigger_confetti.py` with the path to the Python script and `yourusername` with your actual username. Ensure the `DISPLAY` and `DBUS_SESSION_BUS_ADDRESS` values are correct for your environment.

### Start and enable the service

Reload systemd to recognize the new service, then start and enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable confetti-trigger.service --now
```

### Start the Cloudflare tunnel

Run the Cloudflare Tunnel:

```bash
cloudflared tunnel run confetti
```

You can add a systemd for the tunnel as well:

```bash
sudo nano /etc/systemd/system/cloudflared.service
```

Tunnel id can be `confetti` or whatever you named your tunnel.

```ini
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/cloudflared tunnel run <tunnel-id>
Restart=always
User=yourusername
Environment=LOGLEVEL=info

[Install]
WantedBy=multi-user.target
```

### Test the Setup

Send a POST request to trigger the confetti:

```bash
curl -X POST https://confetti.example.com
```

You should see the confetti effect activate in your GNOME environment. If you encounter any issues, check the logs with:

```bash
journalctl -u confetti-trigger.service
```

## License

This project is licensed under the MIT License.
