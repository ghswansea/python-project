import time
import requests

JENKINS_URL = "http://localhost:8081"
JOB_NAME = "python-project"
AUTH = ("admin", "11c3c4c3a3d413a0a1ad88d8caeee5e746")  # Replace with your Jenkins username and API token

def trigger_and_wait() -> None:
    # 1. Trigger jenkins job build:
    response = requests.post(f"{JENKINS_URL}/job/{JOB_NAME}/build", auth=AUTH, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(f"Triggered Jenkins job '{JOB_NAME}'. Waiting for build to start...")   
    if response.status_code != 201:
        raise ValueError("Failed to trigger Jenkins job")

    # 2. Poll the latest build status
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"
    while True:
        time.sleep(3)  # Wait for 3 seconds before checking the build status
        data = requests.get(build_url, auth=AUTH, timeout=10).json()
        if not data.get("building") :
            result = data.get("result")
            print(f"Build #{data.get('number')} completed with status: {result}")
            if result != "SUCCESS":
                raise SystemExit(1)
            break

if __name__ == "__main__":
    trigger_and_wait()
