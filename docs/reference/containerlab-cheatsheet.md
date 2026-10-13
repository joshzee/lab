# Containerlab Cheatsheet

Quick reference for common containerlab commands and concepts.

## Core Commands

### Lab Lifecycle

```bash
# Deploy a lab
containerlab deploy -t topology.clab.yml

# Deploy with custom name
containerlab deploy -t topology.clab.yml --name mylab

# Destroy a lab
containerlab destroy -t topology.clab.yml

# Destroy with cleanup (remove configs)
containerlab destroy -t topology.clab.yml --cleanup

# Destroy all labs
containerlab destroy --all
```

### Inspection

```bash
# List running labs
containerlab inspect --all

# Inspect specific lab
containerlab inspect -t topology.clab.yml

# Show detailed node info
containerlab inspect -t topology.clab.yml --format json
```

### Visualization

```bash
# Generate topology graph (opens browser)
containerlab graph -t topology.clab.yml

# Save graph to file
containerlab graph -t topology.clab.yml -o topology.png
```

## Topology File Structure

```yaml
name: my-lab

topology:
  nodes:
    # Node definition
    node1:
      kind: srl          # Node type
      image: ghcr.io/nokia/srlinux:latest

    node2:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest

  links:
    # Link definition
    - endpoints: ["node1:e1-1", "node2:e1-1"]
```

## Node Kinds

| Kind | Description | Example Image |
|------|-------------|---------------|
| `srl` | Nokia SR Linux | `ghcr.io/nokia/srlinux` |
| `ceos` | Arista cEOS | `ceos:latest` (local) |
| `linux` | Generic Linux | `alpine:latest` |
| `vr-sros` | Nokia SR OS (VM) | Requires license |
| `sonic-vs` | SONiC | `docker-sonic-vs` |
| `crpd` | Juniper cRPD | Requires download |

## Common Patterns

### Adding Management Network

```yaml
topology:
  nodes:
    node1:
      kind: srl
      mgmt-ipv4: 172.20.20.10
```

### Binding Startup Configs

```yaml
topology:
  nodes:
    node1:
      kind: srl
      startup-config: configs/node1.cfg
```

### Setting Environment Variables

```yaml
topology:
  nodes:
    node1:
      kind: linux
      env:
        MY_VAR: value
```

### Port Publishing

```yaml
topology:
  nodes:
    node1:
      kind: linux
      ports:
        - 8080:80
```

### Custom Commands

```yaml
topology:
  nodes:
    node1:
      kind: linux
      exec:
        - ip addr show
```

## Connecting to Nodes

```bash
# Docker exec (generic)
docker exec -it clab-mylab-node1 bash

# SR Linux CLI
docker exec -it clab-mylab-node1 sr_cli

# SSH (if configured)
ssh admin@clab-mylab-node1
```

## Interface Naming

### SR Linux
- `e1-1` = ethernet-1/1
- `e1-2` = ethernet-1/2
- Management: `mgmt0`

### Linux Containers
- `eth1`, `eth2`, etc.

### Link Format
```yaml
endpoints: ["node1:e1-1", "node2:e1-1"]
#           ^source       ^destination
```

## Working with Configs

### Save Running Configs

```bash
# Configs saved to clab-<name>/ directory by default
containerlab save -t topology.clab.yml
```

### Config Directory Structure

```
clab-mylab/
├── node1/
│   └── config/
├── node2/
│   └── config/
└── topology-data.json
```

## Useful Environment Variables

```bash
# Set default topology file
export CLAB_TOPOLOGY=./lab.clab.yml

# Disable telemetry
export CLAB_TELEMETRY=false
```

## Networking

### View Lab Networks

```bash
# Docker networks created by containerlab
docker network ls | grep clab

# Inspect network
docker network inspect clab-mylab
```

### Management Network

By default, containerlab creates a management bridge:
- Network: `172.20.20.0/24`
- Nodes get sequential IPs

## Troubleshooting Commands

```bash
# Check container status
docker ps -a | grep clab

# View container logs
docker logs clab-mylab-node1

# Check interface assignment
docker exec clab-mylab-node1 ip link show

# Verify connectivity between nodes
docker exec clab-mylab-node1 ping <other-node-ip>
```

## Example Topologies

### Two Nodes Connected

```yaml
name: two-nodes

topology:
  nodes:
    srl1:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest
    srl2:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest

  links:
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
```

### Linear Topology (3 Nodes)

```yaml
name: linear

topology:
  nodes:
    srl1:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest
    srl2:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest
    srl3:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest

  links:
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
    - endpoints: ["srl2:e1-2", "srl3:e1-1"]
```

### With Linux Host

```yaml
name: with-host

topology:
  nodes:
    router:
      kind: srl
      image: ghcr.io/nokia/srlinux:latest
    host:
      kind: linux
      image: alpine:latest

  links:
    - endpoints: ["router:e1-1", "host:eth1"]
```

## Links

- [Containerlab Documentation](https://containerlab.dev)
- [Topology Examples](https://github.com/srl-labs/containerlab/tree/main/lab-examples)
- [Discord Community](https://discord.gg/vAyddtaEV9)
