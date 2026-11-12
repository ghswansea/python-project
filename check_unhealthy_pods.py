import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def check_unhealthy_pods(namespace: str = "default") -> None:
    """
    Checks for unhealthy pods in the Kubernetes cluster and prints their details.
    """
    try:
        config.load_kube_config()    # use .kube/config file for local development
    except Exception as e:
        raise SystemExit(f"failed to load Kubernetes configuration: {e}")

    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)
    # list comprehension to filter unhealthy pods
    unhealthy_pods = [pod for pod in pods.items if pod.status.phase not in ["Running", "Succeeded"]]  
    
    if not unhealthy_pods:
        print(f"All pods in namespace '{namespace}' are healthy.")
        return

    print("=== Unhealthy pods ===")
    for pod in unhealthy_pods:
        print(f"Alert: Pod: {pod.metadata.name} | Status: {pod.status.phase}")
        for cs in pod.status.container_statuses or []:
            if cs.state.waiting:
                print(f"  - Container: {cs.name} | Waiting Reason: {cs.state.waiting.reason}")
            elif cs.state.terminated:
                print(f"  - Container: {cs.name} | Terminated Reason: {cs.state.terminated.reason}")

if __name__ == "__main__":
    ns = sys.argv[1] if len(sys.argv) > 1 else "default"
    check_unhealthy_pods(namespace=ns)