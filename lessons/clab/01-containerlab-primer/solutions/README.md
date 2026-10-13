# Lesson 1 Solutions

Reference solutions for the Containerlab Primer exercises.

## Exercise 1: Deploy and Explore

**`containerlab inspect` output:**

```
+---+---------------------+--------------+-------------------------------+------+---------+----------------+----------------------+
| # |        Name         | Container ID |             Image             | Kind |  State  |  IPv4 Address  |     IPv6 Address     |
+---+---------------------+--------------+-------------------------------+------+---------+----------------+----------------------+
| 1 | clab-first-lab-srl1 | abc123def456 | ghcr.io/nokia/srlinux:24.10.1 | srl  | running | 172.20.20.2/24 | 2001:172:20:20::2/64 |
| 2 | clab-first-lab-srl2 | 789ghi012jkl | ghcr.io/nokia/srlinux:24.10.1 | srl  | running | 172.20.20.3/24 | 2001:172:20:20::3/64 |
+---+---------------------+--------------+-------------------------------+------+---------+----------------+----------------------+
```

The IPv4 Address column shows the management IP that containerlab assigns automatically. These are on the management network (172.20.20.0/24), separate from any data-plane interfaces. You'll use pinned management IPs in Lesson 2 for Ansible.

**`show version` output (inside srl1):**

```
A:srl1# show version
--------------------------------------------------
Hostname          : srl1
Chassis Type      : 7220 IXR-D2L
Part Number       : Sim Part No.
Serial Number     : Sim Serial No.
System HW MAC Address: 1A:2B:00:00:00:00
Software Version  : v24.10.1
Build Number      : 000-000000
Architecture      : x86_64
Last Booted       : 2026-02-28T12:00:00.000Z
Total Memory      : 24052875 kB
Free Memory       : 18234567 kB
--------------------------------------------------
```

**`show interface brief` output:**

```
A:srl1# show interface brief
+---------------------+----------+----------+--------+----------+
|      Interface      |  Admin   |  Oper    | Speed  |   Type   |
+=====================+==========+==========+========+==========+
| ethernet-1/1        | enable   | up       | 25G    | ethernet |
| ethernet-1/2        | enable   | down     | 25G    | ethernet |
| ...                 |          |          |        |          |
| mgmt0               | enable   | up       | 1G     | None     |
+---------------------+----------+----------+--------+----------+
```

Only `ethernet-1/1` is operationally up because that's the only interface with a link (connected to srl2). The rest show `down` because nothing is plugged into them. The `mgmt0` interface is the management port containerlab uses.

---

## Exercise 2: Three-Node Topology

**File: `three-node.clab.yml`**

```yaml
name: three-node-lab

topology:
  nodes:
    srl1:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    srl2:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    srl3:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

  links:
    # srl1 to srl2
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
    # srl2 to srl3
    - endpoints: ["srl2:e1-2", "srl3:e1-1"]
```

**Verification:**
```bash
docker exec -it clab-three-node-lab-srl2 sr_cli -c "show interface brief"
```

Expected output shows both `ethernet-1/1` and `ethernet-1/2`.

---

## Exercise 3: Generate Documentation

**Topology graph:**

The `containerlab graph` command generates an HTML page with an interactive topology diagram. In headless environments, use the `--drawio` flag to export a Draw.io file instead.

```bash
containerlab graph -t exercises/three-node.clab.yml --drawio
```

This creates a `.drawio` file in the current directory that you can open in [draw.io](https://app.diagrams.net/).

**JSON inspect output:**

```bash
containerlab inspect -t exercises/three-node.clab.yml --format json > exercises/lab-info.json
```

The JSON output contains structured data for each node including container ID, image, kind, state, and management IP. This format is useful for automation -- you can parse it with `jq` or Python to build scripts that interact with your lab programmatically.

```json
{
  "containers": [
    {
      "name": "clab-three-node-lab-srl1",
      "container_id": "abc123",
      "image": "ghcr.io/nokia/srlinux:24.10.1",
      "kind": "srl",
      "state": "running",
      "ipv4_address": "172.20.20.2/24"
    },
    ...
  ]
}
```

---

## Exercise 4: Resources

**SR Linux Documentation:**
https://containerlab.dev/manual/kinds/srl/

Key configuration options:
- `startup-config`: Path to configuration file
- `license`: Path to license file (not needed for basic features)
- `type`: SR Linux variant (ixrd1, ixrd2, etc.)

**Example Community Labs:**
- https://github.com/srl-labs/srl-labs - Nokia's official examples
- https://github.com/srl-labs/containerlab/tree/main/lab-examples - Built-in examples
- https://clabs.netdevops.me/ - Community lab collection

---

## Exercise 5: Mixed Topology

**File: `mixed-topology.clab.yml`**

```yaml
name: mixed-lab

topology:
  nodes:
    router:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    host1:
      kind: linux
      image: alpine:3.20

  links:
    - endpoints: ["router:e1-1", "host1:eth1"]
```

**Verification steps:**

1. Deploy:
   ```bash
   containerlab deploy -t exercises/mixed-topology.clab.yml
   ```

2. Check router:
   ```bash
   docker exec -it clab-mixed-lab-router sr_cli -c "show interface brief"
   ```

3. Check host:
   ```bash
   docker exec -it clab-mixed-lab-host1 ip addr show eth1
   ```

Expected host output:
```
3: eth1@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9500 qdisc noqueue state UP
    link/ether aa:c1:ab:xx:xx:xx brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

Note: The interface exists but has no IP address assigned. That's normal - we'll configure IP addresses in Lesson 2.

---

## Exercise 6: Break/Fix -- Container Stopped

**Diagnosis:**

```bash
containerlab inspect -t topology/lab.clab.yml
```

The inspect output shows srl2 with state `exited` instead of `running`.

```bash
docker ps -a --filter name=clab-first-lab
```

```
CONTAINER ID   IMAGE                          COMMAND   STATE    NAMES
abc123         ghcr.io/nokia/srlinux:24.10.1  ...       Up      clab-first-lab-srl1
def456         ghcr.io/nokia/srlinux:24.10.1  ...       Exited  clab-first-lab-srl2
```

The `-a` flag is critical -- `docker ps` without it only shows running containers, so the stopped srl2 would be invisible. This is a common gotcha.

**Fix:**

```bash
docker start clab-first-lab-srl2
```

Wait 10-15 seconds for SR Linux to boot, then verify:

```bash
docker exec -it clab-first-lab-srl2 sr_cli -c "show interface brief"
```

`ethernet-1/1` should show `oper: up` because the link to srl1 is re-established.

Alternatively, you could destroy and redeploy the entire lab with `containerlab deploy`. `docker start` is faster for a single node, but redeploying guarantees a clean state.

---

## Exercise 7: Break/Fix -- Missing Link

**Diagnosis:**

Both containers are running (`docker ps` shows them), but `show interface brief` on both nodes shows `ethernet-1/1` as `oper: down`. In the working lab, this interface was `oper: up`.

The topology file has `links: []` -- no virtual links are created between the nodes. Without a link, there's no veth pair connecting the interfaces, so the operational state stays down.

This is the containerlab equivalent of a missing cable. The node is fine, the interface exists, but nothing is plugged into it.

**Fix:**

Add the missing link to `exercises/broken-topology.clab.yml`:

```yaml
  links:
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
```

```bash
containerlab destroy -t exercises/broken-topology.clab.yml --cleanup
containerlab deploy -t exercises/broken-topology.clab.yml
```

**Key lesson:** A container being "running" only means the process is alive. An interface being "up" requires a link partner on the other end. Always check both the node state AND the interface state when troubleshooting.

---

## Key Takeaways

1. **Topology files are YAML** -- this means you can version-control your network labs in Git, diff changes between versions, and template them for different environments
2. **Lab names drive container names** -- the pattern `clab-<name>-<node>` is how you'll `docker exec` into devices; pick short, meaningful names so your commands stay readable
3. **Interface naming maps between shorthand and full names** -- `e1-1` in the topology file becomes `ethernet-1/1` inside SR Linux; Linux hosts use `eth1`, `eth2`, etc. Understanding this mapping avoids confusion when troubleshooting
4. **Mixed topologies bridge network OS and Linux** -- combining SR Linux routers with Alpine hosts lets you simulate real scenarios where applications (in Linux) communicate through network infrastructure
5. **`containerlab inspect` is your first troubleshooting command** -- it shows state, management IPs, and container IDs; always run it before debugging individual nodes
6. **Pin image versions for reproducibility** -- `alpine:3.20` not `alpine:latest`; a lab that works today should work identically next month
