# BPB Offshore Dashboard - DigiBPB

Digital dashboard for BPB Offshore Platform, NH&BS Asset, Mumbai Offshore. A static single-page web application hosted on GitHub Pages providing quick access to operational resources including the daily helicopter schedule.

## Quick Start

### Step 1: Push Code to GitHub

Clone or push this repository to GitHub:

```
https://github.com/upendrach-stack/DigiBPB
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Set **Branch** to `main` and folder to `/ (root)`
5. Click **Save**

### Step 3: Wait for Deployment

GitHub Actions will automatically build and deploy your site. You can monitor progress in the **Actions** tab of the repository.

### Step 4: Access the Dashboard

Once deployed, your dashboard is live at:

```
https://upendrach-stack.github.io/DigiBPB/
```

## Project Structure

```
DigiBPB/
├── index.html                          # Dashboard SPA (HTML/CSS/JS all-in-one)
├── files/
│   └── Daily_Helicopter_Schedule.docx  # Synced helicopter schedule file
├── sync/
│   └── sync_helicopter_schedule.py     # Python script to upload schedule to GitHub
├── docs/
│   └── custom-domain-setup.md          # Custom domain configuration guide
└── README.md                           # This file
```

## Sync Script Setup

The sync script (`sync/sync_helicopter_schedule.py`) automatically uploads the daily helicopter schedule from the intranet file server to this GitHub repository. Follow the steps below to set it up on the office PC.

### Prerequisites

- Python 3.x installed on the office PC
- Install the `requests` library:
  ```
  pip install requests
  ```

### Step 1: Create a GitHub Personal Access Token (PAT)

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name, e.g., `DigiBPB Sync`
4. Under **Select scopes**, check the `repo` scope (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** — you won't be able to see it again

### Step 2: Set the Environment Variable

On the office PC, open Command Prompt and run:

```
setx GITHUB_PAT "ghp_your_token_here"
```

Replace `ghp_your_token_here` with the token you copied in Step 1.

> **Note:** You must restart your terminal (or open a new Command Prompt window) after running `setx` for the variable to take effect.

### Step 3: Run the Script Manually to Verify

Open a new Command Prompt and run:

```
cd sync
python sync_helicopter_schedule.py
```

**Expected output on success:**

```
[2025-07-01 06:00:00] Reading file from network path...
[2025-07-01 06:00:01] File read successfully (size: XXXXX bytes)
[2025-07-01 06:00:02] Uploading to GitHub...
[2025-07-01 06:00:03] File uploaded successfully to files/Daily_Helicopter_Schedule.docx
```

If you see error messages instead, check that:
- The network path `\\10.205.122.39\mr\Helicopter Schedule\Daily Helicopter Schedule\Daily Helicopter Schedule.docx` is accessible from the office PC
- The `GITHUB_PAT` environment variable is set correctly (run `echo %GITHUB_PAT%` to verify)
- The token has not expired and has the `repo` scope enabled


## Troubleshooting

| Issue | Solution |
|-------|----------|
| PAT expired | Generate a new token at https://github.com/settings/tokens, then update the environment variable: `setx GITHUB_PAT "ghp_new_token_here"`. Restart your terminal. |
| Network path unreachable | Check that the PC can access `\\10.205.122.39` — open File Explorer and paste the path. Verify network permissions and that the file server is online. |
| File not updating on GitHub Pages | GitHub Pages may cache content for up to ~10 minutes. Hard-refresh your browser with **Ctrl+Shift+R**. Check the GitHub repository to confirm the file was actually updated. |
| Script runs but upload fails with 409 | SHA mismatch — the file was updated externally (e.g., another user or manual edit on GitHub). Re-run the script; it will fetch the latest SHA and retry. |
| `requests` module not found | Run `pip install requests` in your terminal to install the dependency. |

## Optional: Intranet Hosting

To also serve the dashboard on the intranet at **10.205.173.28:5009**, run one of the following from the project root directory:

**Using Python:**

```
python -m http.server 5009
```

**Using Node.js:**

```
npx http-server -p 5009
```

Users on the ONGC intranet can then access the dashboard at `http://10.205.173.28:5009`.

See `docs/custom-domain-setup.md` for DNS configuration to use a friendly domain name like `digiBPB.in`.
