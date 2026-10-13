# Troubleshooting Guide

Common issues and solutions for containerlab and network labs.

## Containerlab Issues

### Lab Won't Deploy

**Symptom:** `containerlab deploy` fails immediately

**Check 1: Docker Running**
```bash
docker ps
# If "Cannot connect to Docker daemon"
sudo systemctl start docker
```

**Check 2: Topology Syntax**
```bash
# Validate YAML
containerlab deploy -t topology.clab.yml --debug
```

**Check 3: Image Available**
```bash
docker images | grep srlinux
# If not present
docker pull ghcr.io/nokia/srlinux:latest
```

**Check 4: Disk Space**
```bash
df -h
docker system df
# Clean up if needed
docker system prune
```

---

### Container Starts But Exits

**Symptom:** Container shows "Exited" status

**Check Logs:**
```bash
docker logs clab-<lab>-<node>
```

**Common Causes:**
- Insufficient memory for network OS
- Startup config syntax error
- Missing required files

**Solution:** Increase Docker resources or fix config.

---

### Can't Connect to Node

**Symptom:** `docker exec` fails or hangs

**Check Container State:**
```bash
docker ps -a | grep clab
```

**If Running But Unresponsive:**
```bash
# Try different shell
docker exec -it clab-<lab>-<node> /bin/bash
docker exec -it clab-<lab>-<node> /bin/sh

# For SR Linux specifically
docker exec -it clab-<lab>-<node> sr_cli
```

**If Container Is Restarting:**
```bash
# Check resource limits
docker stats clab-<lab>-<node>
```

---

### Nodes Can't Ping Each Other

**Symptom:** Ping between containerlab nodes fails

**Systematic Debugging:**

1. **Check interfaces exist:**
```bash
# Inside node
show interface brief  # SR Linux
ip addr show          # Linux
```

2. **Check IP addresses configured:**
```bash
show interface ethernet-1/1  # SR Linux
```

3. **Check interfaces in same subnet:**
```
Node1: 10.0.0.1/24
Node2: 10.0.0.2/24  ✓ Same subnet

Node1: 10.0.0.1/24
Node2: 10.0.1.2/24  ✗ Different subnets
```

4. **Check ARP:**
```bash
show arpnd arp-entries  # SR Linux
ip neigh show           # Linux
```

5. **Check routing:**
```bash
show network-instance default route-table ipv4-unicast summary  # SR Linux
ip route show  # Linux
```

---

### Graph Command Fails

**Symptom:** `containerlab graph` doesn't open browser

**Solution:** Save to file instead:
```bash
containerlab graph -t topology.clab.yml -o topology.png
```

Or use ASCII output:
```bash
containerlab inspect -t topology.clab.yml
```

---

## Network OS Issues

### SR Linux

**Can't Enter Configuration Mode**
```bash
# If "Error: candidate already exists"
discard now
enter candidate
```

**Config Changes Not Taking Effect**
```bash
# Did you commit?
commit now
```

**Interface Won't Come Up**
```bash
# Check admin-state
show interface ethernet-1/1 detail

# Enable it
enter candidate
set interface ethernet-1/1 admin-state enable
commit now
```

---

### FRRouting

**OSPF Neighbors Not Forming**
```bash
# Check interface is in OSPF
show ip ospf interface

# Check hello/dead timers match
show ip ospf neighbor
```

**BGP Not Establishing**
```bash
# Check BGP config
show running-config bgp

# Check BGP state
show bgp summary
```

---

## Test Failures

### pytest Can't Find Containers

**Check Lab Running:**
```bash
containerlab inspect -t topology.clab.yml
docker ps | grep clab
```

**Check Container Names:**
Test files may expect specific names. Verify topology name matches.

---

### Connection Timeout in Tests

**Increase Timeout:**
```python
# In test file
import time
time.sleep(30)  # Wait for nodes to fully boot
```

**Check Node Ready:**
```bash
# SR Linux readiness
docker exec clab-<lab>-node1 sr_cli -c "show version"
```

---

## Git/Fork Issues

### Can't Push to Fork

**Check Remote:**
```bash
git remote -v
# Should show YOUR username for 'origin'
```

**Fix:**
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/kubecraft.git
```

---

### Merge Conflicts

**Safe Resolution:**
```bash
# Stash your changes first
git stash

# Get upstream changes
git fetch upstream
git merge upstream/main

# Restore your changes
git stash pop

# Fix any conflicts manually
git add .
git commit -m "Resolve conflicts"
```

---

## Resource Issues

### Out of Memory

**Symptoms:**
- Containers crash
- System becomes slow
- "Cannot allocate memory" errors

**Solutions:**
```bash
# Check usage
free -h
docker stats

# Stop unused labs
containerlab destroy -t other-lab.clab.yml

# Clean Docker
docker system prune -a

# Reduce lab size
# Edit topology to use fewer nodes
```

---

### Out of Disk Space

**Check:**
```bash
df -h
docker system df
```

**Clean:**
```bash
# Remove unused Docker resources
docker system prune -a

# Remove old lab configs
rm -rf clab-*/

# Remove old images
docker image prune -a
```

---

## Quick Diagnostic Commands

### System Health
```bash
# Memory
free -h

# Disk
df -h

# Docker status
docker info
docker stats --no-stream
```

### Lab Health
```bash
# Running containers
docker ps | grep clab

# Container logs
docker logs clab-<lab>-<node>

# Lab details
containerlab inspect -t topology.clab.yml
```

### Network Health
```bash
# Inside container
ip addr show
ip route show
ping <other-node>
```

## Getting Help

1. **Check this guide first**
2. **Search existing GitHub issues** in containerlab repo
3. **Ask in Discord:** [Containerlab Discord](https://discord.gg/vAyddtaEV9)
4. **Open an issue** with:
   - Topology file
   - Error message
   - Output of `containerlab version`
   - Output of `docker version`
