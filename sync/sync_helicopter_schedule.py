"""
BPB Offshore Dashboard - Helicopter Schedule Sync Script
Syncs the daily helicopter schedule from intranet file server to GitHub.
No git binary required — uses GitHub REST API (Contents API).
"""

import os
import sys
import base64
import json
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

# ============================================================
# Configuration — Edit these values for your setup
# ============================================================
GITHUB_REPO = "upendrach-stack/DigiBPB"  # owner/repo
FILE_PATH_IN_REPO = "files/Daily_Helicopter_Schedule.docx"
LOCAL_NETWORK_PATH = r"\\10.205.122.39\mr\Helicopter Schedule\Daily Helicopter Schedule\Daily Helicopter Schedule.docx"
ENV_VAR_NAME = "GITHUB_PAT"
GITHUB_API_BASE = "https://api.github.com"

def read_local_file(path):
    """Read the helicopter schedule file from the network path.
    
    Args:
        path: UNC path or local path to the file.
    
    Returns:
        bytes: File content as bytes, or None if reading failed.
    """
    try:
        with open(path, 'rb') as f:
            content = f.read()
        print(f"[{datetime.now().isoformat()}] SUCCESS: Read file ({len(content)} bytes) from {path}")
        return content
    except FileNotFoundError:
        print(f"[{datetime.now().isoformat()}] ERROR: File not found at {path}")
        return None
    except PermissionError:
        print(f"[{datetime.now().isoformat()}] ERROR: Permission denied when reading {path}")
        return None
    except OSError as e:
        print(f"[{datetime.now().isoformat()}] ERROR: OS error reading {path}: {e}")
        return None


def get_existing_sha(token):
    """Get the SHA of the existing file in the GitHub repo.
    
    Required by the GitHub Contents API to update an existing file.
    
    Args:
        token: GitHub Personal Access Token.
    
    Returns:
        str: SHA hash of the existing file, or None if file doesn't exist (404).
    """
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/contents/{FILE_PATH_IN_REPO}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        sha = response.json().get("sha")
        print(f"[{datetime.now().isoformat()}] INFO: Existing file found, SHA: {sha[:8]}...")
        return sha
    elif response.status_code == 404:
        print(f"[{datetime.now().isoformat()}] INFO: File not found in repo (will create new)")
        return None
    else:
        print(f"[{datetime.now().isoformat()}] ERROR: GitHub API returned {response.status_code}: {response.text[:200]}")
        return None


def upload_to_github(token, file_content, sha=None):
    """Upload the file to GitHub using the Contents API.
    
    Args:
        token: GitHub Personal Access Token.
        file_content: File content as bytes.
        sha: SHA of the existing file (required for updates, None for creation).
    
    Returns:
        bool: True if upload succeeded, False otherwise.
    """
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/contents/{FILE_PATH_IN_REPO}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Base64 encode the file content
    encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    # Build request body
    today = datetime.now().strftime("%Y-%m-%d")
    body = {
        "message": f"Update Daily Helicopter Schedule - {today}",
        "content": encoded_content
    }
    
    # Include SHA if updating an existing file
    if sha:
        body["sha"] = sha
    
    response = requests.put(url, headers=headers, json=body)
    
    if response.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        print(f"[{datetime.now().isoformat()}] SUCCESS: {action} file in GitHub repo")
        return True
    else:
        print(f"[{datetime.now().isoformat()}] ERROR: Upload failed with status {response.status_code}: {response.text[:200]}")
        return False


def main():
    """Main orchestration function.
    
    Flow: Read PAT from env → Read local file → Get existing SHA → Upload to GitHub.
    """
    print(f"\n{'='*60}")
    print(f"[{datetime.now().isoformat()}] Starting Helicopter Schedule Sync")
    print(f"{'='*60}")
    
    try:
        # Step 1: Read GitHub PAT from environment variable
        token = os.environ.get(ENV_VAR_NAME)
        if not token:
            print(f"[{datetime.now().isoformat()}] ERROR: Environment variable '{ENV_VAR_NAME}' not set.")
            print(f"  Set it with: setx {ENV_VAR_NAME} \"your_github_personal_access_token\"")
            return False
        
        # Step 2: Read the file from the network path
        file_content = read_local_file(LOCAL_NETWORK_PATH)
        if file_content is None:
            return False
        
        # Step 3: Get existing file SHA (needed for updates)
        sha = get_existing_sha(token)
        
        # Step 4: Upload to GitHub
        success = upload_to_github(token, file_content, sha)
        
        if success:
            print(f"[{datetime.now().isoformat()}] Sync completed successfully!")
        else:
            print(f"[{datetime.now().isoformat()}] Sync failed.")
        
        return success
        
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] UNEXPECTED ERROR: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
