import requests
import os

GITHUB_API_URL = "https://api.github.com"
SOURCE_REPO = "ilyazinkovich/sync"
TARGET_REPO = "ilyazinkovich/sync-target"
HEADERS = {
    "Authorization": f"token {os.environ['GH_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}

def sync_issues():
    issues = requests.get(f"{GITHUB_API_URL}/repos/{SOURCE_REPO}/issues", headers=HEADERS).json()
    for issue in issues:
        if 'pull_request' not in issue:
            data = {
                "title": issue["title"],
                "body": issue["body"],
                "labels": [label["name"] for label in issue["labels"]]
            }
            response = requests.post(f"{GITHUB_API_URL}/repos/{TARGET_REPO}/issues", headers=HEADERS, json=data)
            if response.status_code == 201:
                print(f"Issue '{issue['title']}' replicated successfully.")
            else:
                print(f"Failed to replicate issue '{issue['title']}': {response.content}")

def sync_pull_requests():
    pulls = requests.get(f"{GITHUB_API_URL}/repos/{SOURCE_REPO}/pulls", headers=HEADERS).json()
    for pr in pulls:
        data = {
            "title": pr["title"],
            "body": pr["body"],
            "head": pr["head"]["ref"],
            "base": pr["base"]["ref"]
        }
        response = requests.post(f"{GITHUB_API_URL}/repos/{TARGET_REPO}/pulls", headers=HEADERS, json=data)
        if response.status_code == 201:
            print(f"Pull Request '{pr['title']}' replicated successfully.")
        else:
            print(f"Failed to replicate Pull Request '{pr['title']}': {response.content}")

if __name__ == "__main__":
    sync_issues()
    sync_pull_requests()
