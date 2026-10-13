"""
Lesson 1: Containerlab Primer - Validation Tests

Run with: pytest tests/test_lab.py -v

These tests verify:
1. Containerlab is installed and working
2. Docker is available
3. Lab topology files are valid
4. Labs can be deployed and destroyed
"""

import subprocess
import json
import os
import pytest
import time
from pathlib import Path


LESSON_DIR = Path(__file__).parent.parent
TOPOLOGY_FILE = LESSON_DIR / "topology" / "lab.clab.yml"


def run_command(cmd: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )


class TestEnvironment:
    """Verify the lab environment is correctly set up."""

    def test_containerlab_installed(self):
        """Containerlab CLI should be available."""
        result = run_command("containerlab version")
        assert result.returncode == 0
        assert "containerlab" in result.stdout.lower() or "version" in result.stdout.lower()

    def test_docker_available(self):
        """Docker should be running and accessible."""
        result = run_command("docker version")
        assert result.returncode == 0
        assert "Version" in result.stdout

    def test_topology_file_exists(self):
        """Main topology file should exist."""
        assert TOPOLOGY_FILE.exists(), f"Topology file not found: {TOPOLOGY_FILE}"

    def test_topology_file_valid_yaml(self):
        """Topology file should be valid YAML."""
        import yaml
        with open(TOPOLOGY_FILE) as f:
            try:
                data = yaml.safe_load(f)
                assert data is not None
                assert "topology" in data
                assert "nodes" in data["topology"]
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML: {e}")


class TestTopologyStructure:
    """Verify topology file has correct structure."""

    @pytest.fixture
    def topology(self):
        """Load topology file."""
        import yaml
        with open(TOPOLOGY_FILE) as f:
            return yaml.safe_load(f)

    def test_has_name(self, topology):
        """Topology should have the expected name."""
        assert "name" in topology
        assert topology["name"] == "first-lab"

    def test_has_nodes(self, topology):
        """Topology should define nodes."""
        nodes = topology["topology"]["nodes"]
        assert len(nodes) >= 2, "Expected at least 2 nodes"

    def test_nodes_have_kind(self, topology):
        """Each node should have a kind specified."""
        nodes = topology["topology"]["nodes"]
        for name, config in nodes.items():
            assert "kind" in config, f"Node {name} missing 'kind'"

    def test_nodes_have_image(self, topology):
        """Each node should have an image specified."""
        nodes = topology["topology"]["nodes"]
        for name, config in nodes.items():
            assert "image" in config, f"Node {name} missing 'image'"

    def test_has_links(self, topology):
        """Topology should define at least one link."""
        links = topology["topology"].get("links", [])
        assert len(links) >= 1, "Expected at least 1 link"

    def test_links_have_endpoints(self, topology):
        """Each link should have endpoints."""
        links = topology["topology"]["links"]
        for i, link in enumerate(links):
            assert "endpoints" in link, f"Link {i} missing 'endpoints'"
            assert len(link["endpoints"]) == 2, f"Link {i} should have exactly 2 endpoints"

    def test_no_latest_tags(self, topology):
        """No node should use 'latest' image tag."""
        nodes = topology["topology"]["nodes"]
        for name, config in nodes.items():
            image = config.get("image", "")
            assert "latest" not in image, f"Node {name} uses 'latest' tag -- pin a specific version"


class TestLabDeployment:
    """Test that the lab can be deployed and destroyed."""

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Ensure lab is destroyed after test."""
        yield
        # Cleanup
        run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true")
        time.sleep(2)

    def test_lab_deploys_successfully(self):
        """Lab should deploy without errors."""
        # First ensure it's not running
        run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true")
        time.sleep(2)

        # Deploy
        result = run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)

        assert result.returncode == 0, f"Deploy failed: {result.stderr}"
        assert "running" in result.stdout.lower() or "clab" in result.stdout.lower()

    def test_containers_running_after_deploy(self):
        """Containers should be running after deployment."""
        # Deploy first
        run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true")
        time.sleep(2)
        run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)
        time.sleep(5)  # Wait for containers to stabilize

        # Check containers
        result = run_command("docker ps --filter 'name=clab' --format '{{.Names}}'")
        containers = result.stdout.strip().split('\n')
        containers = [c for c in containers if c]  # Remove empty strings

        assert len(containers) == 2, f"Expected 2 containers, got: {containers}"

    def test_inspect_returns_data(self):
        """containerlab inspect should return lab information."""
        # Deploy first
        run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true")
        time.sleep(2)
        run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)
        time.sleep(5)

        # Inspect
        result = run_command(f"containerlab inspect -t {TOPOLOGY_FILE}")

        assert result.returncode == 0
        assert "srl1" in result.stdout or "srl2" in result.stdout

    def test_lab_destroys_successfully(self):
        """Lab should destroy without errors."""
        # Deploy first
        run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup 2>/dev/null || true")
        time.sleep(2)
        run_command(f"containerlab deploy -t {TOPOLOGY_FILE}", timeout=180)
        time.sleep(5)

        # Destroy
        result = run_command(f"containerlab destroy -t {TOPOLOGY_FILE} --cleanup")

        assert result.returncode == 0

        # Verify no containers remain
        time.sleep(2)
        check = run_command("docker ps --filter 'name=clab-first-lab' --format '{{.Names}}'")
        assert check.stdout.strip() == "", f"Containers still running: {check.stdout}"


class TestExerciseFiles:
    """Verify exercise solution files exist and are valid."""

    def test_solutions_directory_exists(self):
        """Solutions directory should exist."""
        solutions_dir = LESSON_DIR / "solutions"
        assert solutions_dir.exists()

    def test_solution_topologies_valid(self):
        """Solution topology files should be valid YAML."""
        import yaml
        solutions_dir = LESSON_DIR / "solutions"

        for clab_file in solutions_dir.glob("*.clab.yml"):
            with open(clab_file) as f:
                data = yaml.safe_load(f)
                assert data is not None, f"Empty file: {clab_file}"
                assert "topology" in data, f"Missing topology key: {clab_file}"

    def test_solution_topologies_no_latest_tags(self):
        """Solution topology files should not use 'latest' image tags."""
        import yaml
        solutions_dir = LESSON_DIR / "solutions"

        for clab_file in solutions_dir.glob("*.clab.yml"):
            with open(clab_file) as f:
                data = yaml.safe_load(f)
                if data and "topology" in data and "nodes" in data["topology"]:
                    for name, config in data["topology"]["nodes"].items():
                        image = config.get("image", "")
                        assert "latest" not in image, \
                            f"{clab_file.name}: node {name} uses 'latest' tag"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
