import time
import requests

JENKINS_URL = "http://localhost:8081"
JOB_NAME = "python-project"
AUTH = ("admin", "11c3c4c3a3d413a0a1ad88d8caeee5e746")

def trigger_and_wait() -> None:
    # 1. Trigger Jenkins job build
    response = requests.post(f"{JENKINS_URL}/job/{JOB_NAME}/build", auth=AUTH, timeout=10)
    response.raise_for_status()
    if response.status_code != 201:
        raise ValueError(f"Failed to trigger Jenkins job: HTTP {response.status_code}")

    print(f"Triggered Jenkins job '{JOB_NAME}'. Waiting for build to start...")

    # 2. Wait for the queued item to receive a build URL
    queue_url = response.headers.get("Location")
    build_url = None
    while queue_url:
        time.sleep(2)
        q_data = requests.get(f"{queue_url}api/json", auth=AUTH, timeout=10).json()
        if q_data.get("cancelled"):
            raise SystemExit("Build was cancelled in the Jenkins queue.")
        executable = q_data.get("executable")
        if executable and "url" in executable:
            build_url = f"{executable['url']}api/json"
            break

    if not build_url:
        time.sleep(3)
        build_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"

    # 3. Poll the build until completion
    while True:
        time.sleep(3)
        data = requests.get(build_url, auth=AUTH, timeout=10).json()
        if not data.get("building"):
            result = data.get("result")
            print(f"Build #{data.get('number')} completed with status: {result}")
            if result != "SUCCESS":
                raise SystemExit(1)
            break

if __name__ == "__main__":
    trigger_and_wait()