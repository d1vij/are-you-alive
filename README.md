# Are you alive ??

Simple cronjob script for termux which pings and notifies the health of servers.

## Installation and setup

1. Clone this repo
```bash
git clone https://github.com/d1vij/are-you-alive
cd are-you-alive
```

2. Setup venv and install dependencies
```bash
# Ensure that the name of venv is ".venv"
python3 -m venv .venv 

.venv/bin/python3 -m pip install -r requirements.txt
```

3. Define ServiceName, Host and Port in `config.yaml`

Config is defined as 

```yaml
service-name:
  host: <hotname of service>
  port: <port to which initiate the connection>
```

Example
```yaml
chatgpt:
  host: chatgpt.com
  port: 443 # Initiating a tcp connection on https port
google:
  host: google.com
  port: 443

# Proxied lan servers
vaultwarden:
  host: vaultwarden.divij.xyz
  port: 443 # Connection over https
couchdb:
  host: couchdb.divij.xyz
  port: 443

unreachable_local:
  host: 192.168.1.69
  port: 8000

localhost:
  host: localhost
  port: 7766

# [termux]:~/coding/are-you-alive $ nmap -sT localhost -p-
# Starting Nmap 7.98 ( https://nmap.org ) at 2025-11-05 17:20 +0530
# Nmap scan report for localhost (127.0.0.1)
# Host is up (0.00070s latency).
# Other addresses for localhost (not scanned): ::1
# Not shown: 65529 closed tcp ports (conn-refused)
# PORT      STATE SERVICE
# 8022/tcp  open  oa-system
# 10150/tcp open  unknown
# 10152/tcp open  unknown
# 20241/tcp open  unknown
# 33633/tcp open  unknown
# 46888/tcp open  unknown

non_http_port:
  host: 192.168.1.201
  port: 8022 # SSH ports also use TCP to intiate connections
valid_ip_but_random_port:
  host: 192.168.1.201
  port: 9000
```

4. Define the service in crontabs
```bash
# If crond is not installed
pkg install cronie
crontab -e
```
