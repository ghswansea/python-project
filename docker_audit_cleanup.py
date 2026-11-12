import docker
from docker.errors import DockerException

def audit_and_cleanup() -> None:
    """
    Audits the Docker environment and performs cleanup of unused resources.
    """
    try:
        client = docker.from_env()
    except DockerException as e:
        raise SystemExit(f"failed to connect to Docker daemon: {e}")

    print("=== Active containers ===")
    for container in client.containers.list(all=True):
        ports = container.ports.keys() if container.ports else "None"
        print(f"- container: {container.name:<25}, status: {container.status:<10}, ports: {ports}")

    reclaimed = client.images.prune(filters={"dangling": True})
    space_mb = reclaimed.get("SpaceReclaimed", 0) / (1024 * 1024)
    print(f"Pruned dangling images. Reclaimed space: {space_mb:.2f} MB")


if __name__ == "__main__":
    audit_and_cleanup()