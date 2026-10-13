# Lesson 1 Exercises: Containerlab Primer

Complete these exercises to solidify your containerlab skills.

```bash
cd lessons/clab/01-containerlab-primer
```

## Exercise 1: Deploy and Explore

**Objective:** Deploy the lab topology and explore the running environment.

### Steps

1. Deploy the provided topology:
   ```bash
   containerlab deploy -t topology/lab.clab.yml
   ```

2. Inspect the running lab:
   ```bash
   containerlab inspect -t topology/lab.clab.yml
   ```

3. Connect to `srl1` and explore:
   ```bash
   docker exec -it clab-first-lab-srl1 sr_cli
   ```

4. Run these commands inside SR Linux and record the output:
   ```
   show version
   show interface brief
   show system information
   ```

5. Exit and connect to `srl2`, verify it's also running:
   ```bash
   docker exec -it clab-first-lab-srl2 sr_cli
   ```

### Deliverables

Create a file `exercises/exercise1-output.md` with:
- Output of `containerlab inspect`
- SR Linux version from `show version`
- List of interfaces from `show interface brief`
- Your explanation: why is `ethernet-1/1` showing `oper: up` while other ethernet interfaces show `oper: down`?

---

## Exercise 2: Modify the Topology

**Objective:** Add a third node to the topology.

### Steps

1. First, destroy the current lab:
   ```bash
   containerlab destroy -t topology/lab.clab.yml
   ```

2. Create a new topology file `exercises/three-node.clab.yml` with:
   - Three SR Linux nodes: `srl1`, `srl2`, `srl3`
   - Linear connectivity: srl1 -- srl2 -- srl3
   - Use interface `e1-1` for srl1-srl2 link
   - Use interface `e1-2` for srl2-srl3 link

3. Deploy your topology:
   ```bash
   containerlab deploy -t exercises/three-node.clab.yml
   ```

4. Verify all three nodes are running:
   ```bash
   containerlab inspect -t exercises/three-node.clab.yml
   ```

5. Connect to `srl2` and verify it has two interfaces connected:
   ```bash
   docker exec -it clab-<your-lab-name>-srl2 sr_cli
   show interface brief
   ```

### Topology Diagram

Your topology should look like:

```mermaid
graph LR
    srl1[srl1] -- e1-1 --- srl2[srl2] -- e1-2 --- srl3[srl3]
```

### Deliverables

- File: `exercises/three-node.clab.yml`
- Verify: `srl2` shows both `ethernet-1/1` and `ethernet-1/2`

---

## Exercise 3: Generate Documentation

**Objective:** Generate and save a topology graph.

### Steps

1. With your three-node lab running, generate the graph:
   ```bash
   containerlab graph -t exercises/three-node.clab.yml -o exercises/topology.png
   ```

   If the above doesn't work (no GUI), try:
   ```bash
   containerlab graph -t exercises/three-node.clab.yml --drawio
   ```

2. Take a screenshot or save the output

3. Also try the inspect output in different formats:
   ```bash
   containerlab inspect -t exercises/three-node.clab.yml --format json > exercises/lab-info.json
   ```

### Deliverables

- `exercises/topology.png` or screenshot
- `exercises/lab-info.json`

---

## Exercise 4: Find Resources

**Objective:** Navigate containerlab documentation and community.

### Steps

1. **Documentation:** Find the containerlab documentation page for SR Linux and note:
   - What startup configuration options are available?
   - How do you specify a license file (if needed)?

2. **GitHub:** Search GitHub for "containerlab" topic and find:
   - One repository with an interesting lab topology
   - Note the repo URL and what the lab demonstrates

3. **Community:** Visit the containerlab Discord (link in docs) and:
   - Note one recent question asked by a user
   - Find the channel for lab examples

### Deliverables

Create `exercises/resources.md` with:
- Link to SR Linux documentation page
- Link to an interesting community lab repo with brief description
- One observation from the Discord community

---

## Exercise 5: Challenge - Add a Linux Host

**Objective:** Create a topology mixing network OS and Linux containers.

### Steps

1. Create `exercises/mixed-topology.clab.yml` with:
   - One SR Linux node (`router`)
   - One Alpine Linux host (`host1`)
   - Connected via router's `e1-1` and host's `eth1`

2. Use this for the Linux node:
   ```yaml
   host1:
     kind: linux
     image: alpine:3.20
   ```

3. Deploy and verify both containers are running

4. Connect to the host:
   ```bash
   docker exec -it clab-<lab>-host1 sh
   ```

5. Inside the host, verify the interface exists:
   ```bash
   ip addr show eth1
   ```

### Topology

```mermaid
graph LR
    router[router<br/>SR Linux] -- e1-1:eth1 --- host1[host1<br/>Alpine Linux]
```

### Deliverables

- `exercises/mixed-topology.clab.yml`
- Verification that `eth1` exists in the Alpine container

---

## Exercise 6: Break/Fix -- Container Stopped

**Objective:** Diagnose why a node is unreachable when its container has stopped.

### Setup (break it)

First, make sure the two-node lab is running:

```bash
cd lessons/clab/01-containerlab-primer
containerlab deploy -t topology/lab.clab.yml
```

Now stop one of the containers:

```bash
docker stop clab-first-lab-srl2
```

### Symptom

```bash
# Try to connect to srl2
docker exec -it clab-first-lab-srl2 sr_cli
# ERROR: container is not running

# Inspect shows something wrong
containerlab inspect -t topology/lab.clab.yml
# srl2 shows state: "exited" instead of "running"
```

### Your Task

1. **Diagnose:** Run `containerlab inspect` and identify which node is down. Check `docker ps -a --filter name=clab-first-lab` to see stopped containers.
2. **Fix:** Restart the stopped container and verify it returns to a running state.
3. **Verify:** Connect to srl2 with `docker exec` and confirm `show interface brief` shows `ethernet-1/1` as up.

### Deliverables

Document:
- The commands you used to diagnose the problem
- How you fixed it (hint: `docker start` vs. redeploying the lab)
- Why `docker ps` alone wouldn't show the stopped container (you need `-a`)

---

## Exercise 7: Break/Fix -- Missing Link

**Objective:** Diagnose why two nodes cannot see each other when a link is missing from the topology.

### Setup (break it)

1. Destroy the current lab:
   ```bash
   containerlab destroy -t topology/lab.clab.yml --cleanup
   ```

2. Create a broken topology file `exercises/broken-topology.clab.yml`:
   ```yaml
   name: broken-lab

   topology:
     nodes:
       srl1:
         kind: srl
         image: ghcr.io/nokia/srlinux:24.10.1

       srl2:
         kind: srl
         image: ghcr.io/nokia/srlinux:24.10.1

     links: []
   ```

3. Deploy the broken topology:
   ```bash
   containerlab deploy -t exercises/broken-topology.clab.yml
   ```

### Symptom

Both containers are running, but:

```bash
docker exec -it clab-broken-lab-srl1 sr_cli -c "show interface brief"
# ethernet-1/1 shows "down" (no link partner)
```

### Your Task

1. **Diagnose:** Both nodes are running, so it's not a container problem. Check `show interface brief` on both nodes -- what's different from the working lab?
2. **Explain:** Why does `ethernet-1/1` show `oper: down`? What's missing?
3. **Fix:** Destroy the broken lab, add the missing link to the topology file, and redeploy.
4. **Verify:** Confirm `ethernet-1/1` is now `oper: up` on both nodes.

### Deliverables

- Your fixed `exercises/broken-topology.clab.yml`
- Explanation of the difference between a node being "running" and an interface being "up"

---

## Cleanup

After completing all exercises:

```bash
# Destroy any running labs
containerlab destroy --all

# Verify
docker ps | grep clab
```

## Validation

Run the automated tests:

```bash
pytest tests/ -v
```

## Completion Checklist

- [ ] Exercise 1: Deployed and explored the two-node lab
- [ ] Exercise 2: Created and deployed three-node topology
- [ ] Exercise 3: Generated topology graph and JSON output
- [ ] Exercise 4: Found documentation and community resources
- [ ] Exercise 5: Created mixed network/Linux topology
- [ ] Exercise 6: Diagnosed and fixed a stopped container
- [ ] Exercise 7: Diagnosed and fixed a missing link

## Next Steps

Commit your exercises to your fork and proceed to [Lesson 2: IP Fundamentals](../02-ip-fundamentals/).
