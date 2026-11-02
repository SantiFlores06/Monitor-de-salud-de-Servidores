# Server Health Monitor

**Agentless health monitoring for Linux servers over SSH, driven by a YAML config.**

![status](https://img.shields.io/badge/status-in%20progress-yellow)

## What it does

- Reads the list of servers and alert thresholds from `config.yaml`
- Connects to each server over SSH (Paramiko) — nothing to install on the monitored hosts
- Collects CPU, RAM and disk usage and compares them against the configured thresholds

## Design

Monitors are created through a **Factory** behind a common interface (`IServidorMonitor`), so adding a new
kind of host (for example Windows over WMI) means adding one class, without touching the main loop
(open/closed principle).

```
config.yaml ──► main.py ──► MonitorFactory ──► MonitorSSHLinux ──► SSH ──► server
                                    │
                                    └──► (future) MonitorWindowsWMI
```

## Configuration

```yaml
servers:
  - name: "web-server"
    type: "linux_ssh"
    ip: "127.0.0.1"
    user: "monitor"
    port: 22

thresholds:
  cpu_percent: 85
  ram_percent: 90
  disk_percent: 80
```

## Run

```bash
pip install -r requirements.txt
python src/main.py
```

## Roadmap

- [ ] Load `config.yaml` in `main.py`
- [ ] Collect real metrics over SSH instead of simulated values
- [ ] Alerts when a threshold is exceeded (`alert_system.py`)
- [ ] Secure SSH: verify host keys against `known_hosts` and use key-based authentication
- [ ] Unit tests with pytest
