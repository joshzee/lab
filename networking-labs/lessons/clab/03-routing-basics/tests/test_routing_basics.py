"""
Lesson 3: Routing Basics -- Validation Tests

Run with: pytest tests/test_routing_basics.py -v

These tests verify:
1. Required tools are installed (containerlab, docker, ansible)
2. Topology file is valid (6 nodes, 5 links, no latest tags)
3. Ansible configuration is valid (inventory, playbook, templates, host_vars)
4. Lab deploys successfully (6 containers)
5. End-to-end connectivity works (host1<->host2, host1<->host3, host2<->host3)
"""

import subprocess
import os
import pytest
import time
from pathlib import Path


LESSON_DIR = Path(__file__).parent.parent
TOPOLOGY_FILE = LESSON_DIR / "topology" / "lab.clab.yml"
ANSIBLE_DIR = LESSON_DIR / "ansible"
LAB_NAME = "routing-basics"


def run_command(cmd: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    return subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=timeout
    )


class TestEnvironment:
    """Verify the lab environment is correctly set up."""

    def test_containerlab_installed(self):
        """Containerlab CLI should be available."""
        result = run_command("containerlab version")
        assert result.returncode == 0

    def test_docker_available(self):
        """Docker should be running and accessible."""
        result = run_command("docker version")
        assert result.returncode == 0

    def test_ansible_installed(self):
        """Ansible should be available."""
        result = run_command("ansible --version")
        assert result.returncode == 0

    def test_topology_file_exists(self):
        """Topology file should exist."""
        assert TOPOLOGY_FILE.exists(), f"Not found: {TOPOLOGY_FILE}"


class TestTopologyStructure:
    """Verify topology file has correct structure."""

    @pytest.fixture
    def topology(self):
        """Load topology file."""
        import yaml
        with open(TOPOLOGY_FILE) as f:
            return yaml.safe_load(f)

    def test_has_correct_name(self, topology):
        """Topology should be named routing-basics."""
        assert topology["name"] == "routing-basics"

    def test_has_six_nodes(self, topology):
        """Topology should have 6 nodes (3 routers + 3 hosts)."""
        nodes = topology["topology"]["nodes"]
        assert len(nodes) == 6, f"Expected 6 nodes, got {len(nodes)}"

    def test_has_five_links(self, topology):
        """Topology should have 5 links."""
        links = topology["topology"]["links"]
        assert len(links) == 5, f"Expected 5 links, got {len(links)}"

    def test_no_latest_tags(self, topology):
        """No node should use 'latest' image tag."""
        nodes = topology["topology"]["nodes"]
        for name, config in nodes.items():
            image = config.get("image", "")
            assert "latest" not in image, f"Node {name} uses 'latest' tag"

    def test_routers_have_mgmt_ips(self, topology):
        """All routers should have pinned management IPs."""
        nodes = topology["topology"]["nodes"]
        for name in ["srl1", "srl2", "srl3"]:
            assert "mgmt-ipv4" in nodes[name], f"{name} missing mgmt-ipv4"

    def test_hosts_have_exec(self, topology):
        """All hosts should have exec commands for IP config."""
        nodes = topology["topology"]["nodes"]
        for name in ["host1", "host2", "host3"]:
            assert "exec" in nodes[name], f"{name} missing exec"
            exec_cmds = nodes[name]["exec"]
            assert any("ip addr add" in cmd for cmd in exec_cmds), \
                f"{name} missing IP address in exec"
            assert any("ip route add default" in cmd for cmd in exec_cmds), \
                f"{name} missing default route in exec"


class TestAnsibleStructure:
    """Verify Ansible configuration files are valid."""

    def test_inventory_exists(self):
        """Ansible inventory should exist."""
        assert (ANSIBLE_DIR / "inventory.yml").exists()

    def test_playbook_exists(self):
        """Ansible playbook should exist."""
        assert (ANSIBLE_DIR / "playbook.yml").exists()

    def test_interface_template_exists(self):
        """Interface Jinja2 template should exist."""
        assert (ANSIBLE_DIR / "templates" / "srl_interfaces.json.j2").exists()

    def test_routes_template_exists(self):
        """Routes Jinja2 template should exist."""
        assert (ANSIBLE_DIR / "templates" / "srl_routes.json.j2").exists()

    def test_host_vars_exist(self):
        """Host vars should exist for all 3 routers."""
        for name in ["srl1", "srl2", "srl3"]:
            path = ANSIBLE_DIR / "host_vars" / f"{name}.yml"
            assert path.exists(), f"Missing host_vars for {name}"

    def test_host_vars_have_routes(self):
        """All router host_vars should have static_routes defined."""
        import yaml
        for name in ["srl1", "srl2", "srl3"]:
            path = ANSIBLE_DIR / "host_vars" / f"{name}.yml"
            with open(path) as f:
                data = yaml.safe_load(f)
            assert "static_routes" in data, f"{name} missing static_routes"
            assert len(data["static_routes"]) >= 2, \
                f"{name} should have at least 2 static routes"

    def test_inventory_has_three_routers(self):
        """Inventory should list 3 routers."""
        import yaml
        with open(ANSIBLE_DIR / "inventory.yml") as f:
            data = yaml.safe_load(f)
        routers = data["all"]["children"]["routers"]["hosts"]
        assert len(routers) == 3, f"Expected 3 routers, got {len(routers)}"


class TestLabDeployment:
    """Test that the lab deploys successfully."""

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Ensure lab is destroyed after test."""
        yield
        run_command(
            f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true"
        )
        time.sleep(2)

    def test_lab_deploys(self):
        """Lab should deploy without errors."""
        run_command(
            f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true"
        )
        time.sleep(2)
        result = run_command(
            f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180
        )
        assert result.returncode == 0, f"Deploy failed: {result.stderr}"

    def test_six_containers_running(self):
        """All 6 containers should be running after deploy."""
        run_command(
            f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true"
        )
        time.sleep(2)
        run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)
        time.sleep(10)

        result = run_command(
            f"docker ps --filter 'name=clab-{LAB_NAME}' --format '{{{{.Names}}}}'"
        )
        containers = [c for c in result.stdout.strip().split("\n") if c]
        assert len(containers) == 6, f"Expected 6 containers, got: {containers}"


class TestConnectivity:
    """Test end-to-end connectivity after Ansible configuration."""

    @pytest.fixture(autouse=True)
    def deploy_and_configure(self):
        """Deploy lab and apply Ansible configuration."""
        run_command(
            f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true"
        )
        time.sleep(2)
        run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)
        time.sleep(10)
        run_command(
            f"cd {ANSIBLE_DIR} && ansible-playbook -i inventory.yml playbook.yml",
            timeout=120,
        )
        time.sleep(5)
        yield
        run_command(
            f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true"
        )

    def test_host1_to_host2(self):
        """host1 should be able to ping host2 (cross-hub)."""
        result = run_command(
            f"docker exec clab-{LAB_NAME}-host1 ping -c 3 -W 5 10.1.4.2"
        )
        assert result.returncode == 0, \
            f"host1 -> host2 failed: {result.stdout}"

    def test_host1_to_host3(self):
        """host1 should be able to ping host3 (cross-hub)."""
        result = run_command(
            f"docker exec clab-{LAB_NAME}-host1 ping -c 3 -W 5 10.1.5.2"
        )
        assert result.returncode == 0, \
            f"host1 -> host3 failed: {result.stdout}"

    def test_host2_to_host3(self):
        """host2 should be able to ping host3 (spoke-to-spoke via hub)."""
        result = run_command(
            f"docker exec clab-{LAB_NAME}-host2 ping -c 3 -W 5 10.1.5.2"
        )
        assert result.returncode == 0, \
            f"host2 -> host3 failed: {result.stdout}"
