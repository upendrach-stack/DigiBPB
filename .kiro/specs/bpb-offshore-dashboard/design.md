# Design Document

## Overview

The BPB Offshore Dashboard is a static single-page web application hosted on GitHub Pages, providing offshore platform personnel quick access to operational resources. The system consists of two components:

1. **Dashboard (Frontend)** — A self-contained HTML/CSS/JS page with ONGC corporate branding, KPI cards for resource access, and a configurable download URL system.
2. **Sync Script (Backend)** — A Python script running on the intranet office PC that automatically uploads the daily helicopter schedule from the intranet file server to GitHub using the Contents API.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     INTRANET (ONGC Network)                      │
│                                                                   │
│  ┌──────────────────┐         ┌───────────────────────────────┐ │
│  │ File Server       │         │ Office PC (10.205.173.28)     │ │
│  │ 10.205.122.39     │ ──────▶ │ - Python Sync Script          │ │
│  │                   │  Read   │ - Windows Task Scheduler      │ │
│  │ \\mr\Helicopter   │  File   │ - Optional: serve on :5009    │ │
│  │ Schedule\...docx  │         │ - GitHub PAT (env var)        │ │
│  └──────────────────┘         └──────────────┬────────────────┘ │
│                                               │                   │
└───────────────────────────────────────────────┼───────────────────┘
                                                │ HTTPS
                                                │ GitHub Contents API
                                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                   │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ GitHub Repository                                          │  │
│  │ - index.html (Dashboard SPA)                               │  │
│  │ - files/Daily_Helicopter_Schedule.docx                     │  │
│  │                                                             │  │
│  │ GitHub Pages (ongc-bpb.github.io/bpb-offshore-dashboard)  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                          │                                        │
│                          │ HTTPS                                   │
│                          ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Users (Any Browser - Offshore/Onshore/Remote)              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Component 1: Dashboard SPA (index.html)

**Purpose:** Single self-contained HTML file providing the dashboard UI with all CSS and JavaScript inline.

**Structure:**
```
index.html
├── <style> — All CSS (gradient panel, card layout, responsive grid, theme colors)
├── <body>
│   ├── Gradient_Panel (left) — Branding, title, platform info
│   ├── Content_Area (right)
│   │   ├── Header — ONGC corporate title and subtitle
│   │   ├── KPI_Cards Grid — Helicopter schedule card (expandable for future cards)
│   │   └── Footer — Role indicator badges
│   └── </body>
└── <script>
    ├── Dashboard_Config — Configurable URLs and settings
    ├── Card click handlers — Open download URLs
    └── Link health check — Fetch HEAD request to detect unreachable links
```

**Key Design Decisions:**
- All CSS and JS inline in a single HTML file for maximum portability (no build step, no dependencies)
- Dashboard_Config is a plain JavaScript object at the top of the script section for easy admin editing
- No external CDN references; all styling is custom CSS
- Link health check uses a HEAD request with CORS mode to detect unreachable resources (graceful degradation if CORS blocks the check)

### Component 2: Sync Script (sync_helicopter_schedule.py)

**Purpose:** Python script that reads the daily helicopter schedule from the intranet file server and uploads it to the GitHub repository via the Contents API.

**Structure:**
```
sync_helicopter_schedule.py
├── Configuration constants
│   ├── GITHUB_REPO — owner/repo string
│   ├── FILE_PATH_IN_REPO — files/Daily_Helicopter_Schedule.docx
│   ├── LOCAL_NETWORK_PATH — UNC path to source file
│   └── ENV_VAR_NAME — Name of environment variable holding GitHub PAT
├── read_local_file() — Read file from network path, return bytes
├── get_existing_sha() — GET /repos/{owner}/{repo}/contents/{path} → extract SHA
├── upload_to_github() — PUT /repos/{owner}/{repo}/contents/{path} with Base64 content
├── main() — Orchestrate read → get SHA → upload, with error handling
└── Logging — Print timestamped messages for success/failure
```

**Key Design Decisions:**
- Uses only the `requests` library (plus stdlib `base64`, `os`, `json`, `sys`, `datetime`) — no git binary needed
- GitHub PAT read from environment variable (never hardcoded)
- SHA retrieval before upload is required by GitHub Contents API for updating existing files; if file doesn't exist (404), SHA is omitted for initial creation
- Script is idempotent — running it multiple times with the same file produces the same result
- All errors are caught and logged with context (timestamp, error type, HTTP status if applicable)

### Component 3: Windows Task Scheduler Configuration

**Purpose:** Automate daily execution of the sync script.

**Configuration:**
- Task name: `BPB_Helicopter_Schedule_Sync`
- Trigger: Daily at a configured time (e.g., 06:00 AM)
- Action: Run `python sync_helicopter_schedule.py`
- Working directory: Directory containing the script
- Run whether user is logged in or not

### Component 4: Documentation (README.md)

**Purpose:** Setup and configuration guide covering deployment, custom domain, and troubleshooting.

**Sections:**
- Quick Start (GitHub Pages deployment)
- Sync Script Setup (PAT creation, env var, Task Scheduler)
- Optional Intranet Hosting (serving on port 5009)
- Custom Domain Configuration (GitHub Pages and intranet DNS)
- Troubleshooting

## Data Flow

### User Accessing Dashboard
1. User opens GitHub Pages URL in browser
2. Browser loads index.html (single file, all inline)
3. Dashboard renders with KPI cards
4. User clicks helicopter schedule card → browser downloads .docx from GitHub Pages hosted file

### File Sync (Daily Automated)
1. Windows Task Scheduler triggers sync script
2. Script reads file from `\\10.205.122.39\mr\Helicopter Schedule\Daily Helicopter Schedule\Daily Helicopter Schedule.docx`
3. Script encodes file content as Base64
4. Script calls GitHub API: GET existing file SHA (or detects 404 for new file)
5. Script calls GitHub API: PUT with Base64 content + SHA → file updated in repo
6. GitHub Pages automatically serves the updated file

## Correctness Properties

### Property 1: Dashboard Configuration Integrity
- **What:** The Dashboard_Config object must contain all required keys with valid URL values
- **How to verify:** Parse the config object and check that the helicopter schedule URL key exists and is a valid URL format
- **Covers:** Requirement 3 (AC 3), Requirement 5 (AC 5)

### Property 2: Sync Script Base64 Round-Trip
- **What:** For any binary file content, encoding to Base64 and decoding back must produce the original content
- **How to verify:** Property-based test — generate random byte sequences, encode with the script's encoding logic, decode, and compare
- **Covers:** Requirement 8 (AC 2)

### Property 3: Sync Script Error Handling Completeness
- **What:** The sync script must handle all failure modes (network path unreachable, API auth failure, API server error) without crashing
- **How to verify:** Simulate each failure condition and verify the script exits gracefully with a logged error message
- **Covers:** Requirement 8 (AC 6, 7)

### Property 4: Sync Script Idempotence
- **What:** Running the sync script multiple times with the same file content must not create duplicate entries or fail
- **How to verify:** Mock the GitHub API, run the script twice with identical file content, verify only one PUT request with correct SHA handling
- **Covers:** Requirement 8 (AC 2, 8)

### Property 5: Dashboard Self-Containment
- **What:** The index.html file must not reference any external domains for CSS, JS, or font resources
- **How to verify:** Parse the HTML file and check that no `<link>`, `<script>`, or `@import` references point to external URLs
- **Covers:** Requirement 5 (AC 1, 4)

### Property 6: Dashboard Accessibility and Interactivity
- **What:** All KPI cards must be keyboard-accessible and have appropriate ARIA attributes
- **How to verify:** Check that card elements have tabindex, role, and aria-label attributes; verify Enter/Space key triggers the click action
- **Covers:** Requirement 3 (AC 1, 2, 4)

## File Structure

```
bpb-offshore-dashboard/
├── index.html                          # Dashboard SPA (all-in-one)
├── files/
│   └── Daily_Helicopter_Schedule.docx  # Synced file (uploaded by script)
├── sync/
│   ├── sync_helicopter_schedule.py     # Python sync script
│   └── setup_task_scheduler.md         # Task Scheduler setup guide
├── docs/
│   └── custom-domain-setup.md          # Custom domain documentation
└── README.md                           # Main project documentation
```

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Dashboard | Vanilla HTML/CSS/JS | No build step, maximum portability, single file deployment |
| Hosting | GitHub Pages | Free, internet-accessible, automatic HTTPS, no server maintenance |
| Sync Script | Python + requests | Available on office PC, no git binary needed, simple HTTP client |
| Scheduling | Windows Task Scheduler | Native to Windows, no additional software, reliable daily execution |
| API | GitHub Contents API | RESTful, well-documented, supports file CRUD with PAT auth |
| Intranet Server | Python http.server or Node.js http-server | Optional, uses tools already installed on office PC |
