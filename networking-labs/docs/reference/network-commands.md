# Network Commands Reference

Essential network diagnostic commands for DevOps engineers.

## Linux Host Commands

### Interface Information

```bash
# Show all interfaces
ip addr show
ip a  # shorthand

# Show specific interface
ip addr show eth0

# Show interface statistics
ip -s link show eth0

# Show only IPv4 addresses
ip -4 addr show
```

### Routing

```bash
# Show routing table
ip route show
ip r  # shorthand

# Show route to specific destination
ip route get 8.8.8.8

# Add static route
ip route add 192.168.1.0/24 via 10.0.0.1

# Delete route
ip route del 192.168.1.0/24
```

### Connectivity Testing

```bash
# Basic ping
ping 10.0.0.1

# Ping with count
ping -c 4 10.0.0.1

# Ping with specific interface
ping -I eth0 10.0.0.1

# Traceroute
traceroute 8.8.8.8

# TCP traceroute (useful when ICMP is blocked)
traceroute -T 8.8.8.8
```

### DNS

```bash
# DNS lookup
dig google.com

# Specific record type
dig google.com MX

# Short output
dig +short google.com

# Query specific DNS server
dig @8.8.8.8 google.com

# Reverse lookup
dig -x 8.8.8.8

# Alternative: nslookup
nslookup google.com
```

### ARP and Neighbors

```bash
# Show ARP table
ip neigh show
arp -a  # legacy

# Clear ARP cache
ip neigh flush all
```

### Network Statistics

```bash
# Show listening ports
ss -tlnp  # TCP
ss -ulnp  # UDP
ss -tunlp # Both

# Legacy netstat equivalent
netstat -tlnp

# Show connections by state
ss -t state established

# Show socket statistics
ss -s
```

### Packet Capture

```bash
# Capture on interface
tcpdump -i eth0

# Capture specific host
tcpdump -i eth0 host 10.0.0.1

# Capture specific port
tcpdump -i eth0 port 80

# Write to file
tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Verbose output
tcpdump -i eth0 -v

# Show packet contents
tcpdump -i eth0 -X
```

### HTTP/API Testing

```bash
# Simple GET
curl http://example.com

# With headers
curl -v http://example.com

# POST with data
curl -X POST -d '{"key":"value"}' http://example.com

# Test connectivity only
curl -I http://example.com

# Timeout
curl --connect-timeout 5 http://example.com
```

## Container-Specific Commands

### Docker Networking

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create network
docker network create mynet

# Connect container to network
docker network connect mynet container1

# View container network settings
docker inspect container1 --format='{{json .NetworkSettings}}'
```

### Inside Container

```bash
# Check if networking tools exist
which ip ping traceroute

# Install if needed (Alpine)
apk add --no-cache iproute2 iputils

# Install if needed (Debian/Ubuntu)
apt-get update && apt-get install -y iproute2 iputils-ping
```

## Troubleshooting Workflow

### 1. Check Local Interface

```bash
# Is the interface up?
ip link show eth0

# Does it have an IP?
ip addr show eth0
```

### 2. Check Local Routing

```bash
# What's the route to the destination?
ip route get 10.0.0.1

# Is there a default route?
ip route show default
```

### 3. Test Connectivity

```bash
# Can we reach the gateway?
ping -c 2 $(ip route show default | awk '{print $3}')

# Can we reach the destination?
ping -c 2 10.0.0.1
```

### 4. Check ARP

```bash
# Do we have the MAC address?
ip neigh show 10.0.0.1
```

### 5. Check Higher Layers

```bash
# Is the port open?
nc -zv 10.0.0.1 22

# Is DNS working?
dig +short google.com

# Is the service responding?
curl -v http://10.0.0.1
```

## MTU and Fragmentation

```bash
# Check MTU
ip link show eth0 | grep mtu

# Ping with specific size (check for fragmentation)
ping -M do -s 1472 10.0.0.1  # 1472 + 28 header = 1500
```

## VLAN Operations

```bash
# Show VLAN info (if 8021q module loaded)
cat /proc/net/vlan/config

# Add VLAN interface
ip link add link eth0 name eth0.100 type vlan id 100
ip link set eth0.100 up
ip addr add 10.0.100.1/24 dev eth0.100
```

## Performance Testing

```bash
# iperf3 server
iperf3 -s

# iperf3 client
iperf3 -c 10.0.0.1

# With bandwidth limit
iperf3 -c 10.0.0.1 -b 100M
```

## Quick Diagnostic Script

```bash
#!/bin/bash
# network-check.sh

echo "=== Interfaces ==="
ip -br addr show

echo -e "\n=== Routes ==="
ip route show

echo -e "\n=== DNS ==="
cat /etc/resolv.conf

echo -e "\n=== Gateway Ping ==="
ping -c 2 $(ip route show default | awk '{print $3}') 2>/dev/null || echo "No default gateway"

echo -e "\n=== Listening Ports ==="
ss -tlnp
```

## Common Issues

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| "Network unreachable" | No route | `ip route show` |
| "Host unreachable" | ARP failure | `ip neigh show` |
| "Connection refused" | Port not listening | `ss -tlnp` |
| "Connection timed out" | Firewall/filter | `iptables -L -n` |
| "Name resolution failed" | DNS issue | `dig google.com` |

## Links

- [iproute2 documentation](https://wiki.linuxfoundation.org/networking/iproute2)
- [tcpdump manual](https://www.tcpdump.org/manpages/tcpdump.1.html)
- [curl manual](https://curl.se/docs/manual.html)
