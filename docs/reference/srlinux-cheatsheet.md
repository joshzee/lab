# Nokia SR Linux CLI Cheatsheet

Quick reference for SR Linux commands commonly used in network labs.

## Accessing SR Linux

```bash
# From host
docker exec -it clab-<lab>-<node> sr_cli

# Already in container
sr_cli
```

## CLI Modes

| Mode | Prompt | Purpose |
|------|--------|---------|
| Running | `--{ running }--` | View current state |
| Candidate | `--{ candidate }--` | Make changes |
| State | `--{ state }--` | Operational data |

### Switching Modes

```
# Enter candidate mode (to make changes)
A:node1# enter candidate

# Commit changes
A:node1# commit now

# Discard changes
A:node1# discard now

# Exit back to running
A:node1# exit
```

## Show Commands

### System Information

```bash
# Version and system info
show version

# System uptime and resources
show system information

# Hostname
show system name
```

### Interface Commands

```bash
# All interfaces summary
show interface brief

# Specific interface
show interface ethernet-1/1

# Interface statistics
show interface ethernet-1/1 statistics

# Interface with detail
show interface ethernet-1/1 detail
```

### Routing Commands

```bash
# Routing table
show network-instance default route-table ipv4-unicast summary

# All routes with detail
show network-instance default route-table ipv4-unicast route *

# Specific route
show network-instance default route-table ipv4-unicast route 10.0.0.0/24

# BGP summary (if configured)
show network-instance default protocols bgp summary
```

### ARP and Neighbors

```bash
# ARP table
show arpnd arp-entries

# All neighbors
show arpnd neighbor
```

## Configuration Commands

### Enter Configuration Mode

```bash
# Enter candidate mode
enter candidate

# Make your changes...

# Validate (check syntax)
validate

# Compare changes
diff

# Commit
commit now

# Or commit with comment
commit now comment "Added interface config"
```

### Interface Configuration

```bash
# Configure interface
set interface ethernet-1/1 admin-state enable
set interface ethernet-1/1 subinterface 0 ipv4 admin-state enable
set interface ethernet-1/1 subinterface 0 ipv4 address 10.0.0.1/24

# Verify
info interface ethernet-1/1
```

### Network Instance

```bash
# View network instances
show network-instance summary

# Configure default instance
set network-instance default interface ethernet-1/1.0
```

### Static Routes

```bash
# Add static route
set network-instance default static-routes route 192.168.1.0/24 next-hop-group nhg1
set network-instance default next-hop-groups group nhg1 nexthop 1 ip-address 10.0.0.2

# Verify
show network-instance default route-table ipv4-unicast route 192.168.1.0/24
```

## Operational Commands

### Connectivity Testing

```bash
# Ping
ping 10.0.0.2 network-instance default

# Traceroute
traceroute 10.0.0.2 network-instance default
```

### Save Configuration

```bash
# Save to file
save /tmp/config.json

# Load from file
load /tmp/config.json
```

## CLI Navigation

| Key | Action |
|-----|--------|
| Tab | Auto-complete |
| ? | Show options |
| Ctrl+C | Cancel command |
| Ctrl+Z | Exit to running mode |
| Up/Down | Command history |

### Output Modifiers

```bash
# Pipe to filter
show interface brief | grep ethernet

# JSON output
show interface brief | as json

# Table format
show interface brief | as table
```

## Common Troubleshooting

### Check Interface Status

```bash
# Is it up?
show interface brief

# Any errors?
show interface ethernet-1/1 statistics

# Physical link?
show interface ethernet-1/1 detail
```

### Check Routing

```bash
# Can we reach it?
ping 10.0.0.2 network-instance default

# What route would we use?
show network-instance default route-table ipv4-unicast route 10.0.0.0/24

# Is the route in the table?
show network-instance default route-table ipv4-unicast summary
```

### Check ARP

```bash
# Do we have ARP entry?
show arpnd arp-entries

# ARP for specific IP
show arpnd arp-entries ipv4-address 10.0.0.2
```

## Quick Reference: Common Tasks

### Enable an Interface

```bash
enter candidate
set interface ethernet-1/1 admin-state enable
commit now
```

### Assign IP Address

```bash
enter candidate
set interface ethernet-1/1 subinterface 0 ipv4 admin-state enable
set interface ethernet-1/1 subinterface 0 ipv4 address 10.0.0.1/24
set network-instance default interface ethernet-1/1.0
commit now
```

### Add Static Route

```bash
enter candidate
set network-instance default next-hop-groups group nhg1 nexthop 1 ip-address 10.0.0.2
set network-instance default static-routes route 192.168.0.0/24 next-hop-group nhg1
commit now
```

### View Full Running Config

```bash
info flat
# or
info
```

## Links

- [SR Linux Documentation](https://documentation.nokia.com/srlinux/)
- [SR Linux CLI Reference](https://documentation.nokia.com/srlinux/SR_Linux_HTML_R24-10/SRLinux-CLI-Ref/index.html)
- [Learn SR Linux](https://learn.srlinux.dev/)
