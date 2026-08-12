# Tasks

## Task 1: Create Dashboard SPA HTML Structure

**Requirements:** 1, 2, 4, 5

### Subtasks

- [x] 1.1 Create `index.html` with HTML5 boilerplate, meta viewport tag, and page title "BPB Offshore Dashboard"
- [x] 1.2 Add the Gradient_Panel section (left panel) with dark navy-to-teal vertical gradient CSS, containing the application title "BPB Platform" and platform identification text
- [x] 1.3 Add the Content_Area section (right panel) with the corporate header displaying "Oil and Natural Gas Corporation Ltd." and subtitle "BPB PLATFORM • NH&BS ASSET • MUMBAI OFFSHORE"
- [x] 1.4 Add a responsive CSS grid/flexbox layout for KPI_Cards within the Content_Area
- [x] 1.5 Add the footer section with role indicator badges ("Admin", "Departments", "OIM", "Viewer") styled as colored teal/navy badges
- [x] 1.6 Add CSS for white card panels with subtle box-shadow and border-radius, teal/cyan accent colors for interactive elements, and responsive breakpoints

## Task 2: Implement KPI Card for Helicopter Schedule

**Requirements:** 3, 5

### Subtasks

- [x] 2.1 Add the Dashboard_Config JavaScript object at the top of the `<script>` section with the helicopter schedule download URL key defaulting to the GitHub Pages hosted file path (e.g., `https://ongc-bpb.github.io/bpb-offshore-dashboard/files/Daily_Helicopter_Schedule.docx`)
- [x] 2.2 Create the KPI_Card element for "Daily Helicopter Schedule" with a helicopter SVG icon, title, description, and appropriate ARIA attributes (role="link", aria-label, tabindex="0")
- [x] 2.3 Implement click handler and keyboard handler (Enter/Space) on the KPI_Card that opens the configured URL from Dashboard_Config
- [x] 2.4 Add CSS hover state for the KPI_Card with teal/cyan accent highlight and smooth transition
- [x] 2.5 Implement link health check using a HEAD fetch request; if the link is unreachable, add a CSS class to visually dim the card and show a small "unavailable" indicator

## Task 3: Create Python Sync Script

**Requirements:** 8

### Subtasks

- [x] 3.1 Create `sync/sync_helicopter_schedule.py` with configuration constants: GITHUB_REPO, FILE_PATH_IN_REPO (`files/Daily_Helicopter_Schedule.docx`), LOCAL_NETWORK_PATH (UNC path), and ENV_VAR_NAME for the GitHub PAT
- [x] 3.2 Implement `read_local_file()` function that reads the file from the network path and returns bytes; catches `FileNotFoundError` and `PermissionError` with logged error messages
- [x] 3.3 Implement `get_existing_sha()` function that calls GET `/repos/{owner}/{repo}/contents/{path}` with Authorization header, returns the SHA string if file exists (200) or None if not found (404)
- [x] 3.4 Implement `upload_to_github()` function that calls PUT `/repos/{owner}/{repo}/contents/{path}` with JSON body containing Base64-encoded content, commit message, and SHA (if updating); logs success or failure with HTTP status
- [x] 3.5 Implement `main()` function that orchestrates: read PAT from env → read local file → get existing SHA → upload; wraps in try/except with timestamped error logging
- [x] 3.6 Add `if __name__ == "__main__": main()` entry point and ensure script exits with code 0 on success, 1 on failure

## Task 4: Create Documentation

**Requirements:** 7, 5

### Subtasks

- [x] 4.1 Create `README.md` with Quick Start section explaining GitHub Pages deployment (enable Pages on main branch, verify URL)
- [x] 4.2 Add Sync Script Setup section to README covering: creating a GitHub PAT with `repo` scope, setting the environment variable (`setx GITHUB_PAT "your_token"`), and running the script manually to verify
- [x] 4.3 Create `sync/setup_task_scheduler.md` with step-by-step instructions for creating a Windows Task Scheduler task (task name, trigger time, action command, working directory, "run whether logged in or not" setting)
- [x] 4.4 Create `docs/custom-domain-setup.md` explaining GitHub Pages custom domain configuration and intranet DNS A record setup for digiBPB.in pointing to 10.205.173.28
- [x] 4.5 Add Troubleshooting section to README covering common issues: PAT expired, network path unreachable, file not updating on GitHub Pages (cache), and optional intranet hosting with `python -m http.server 5009`

## Task 5: Create GitHub Repository Structure

**Requirements:** 5, 8

### Subtasks

- [x] 5.1 Create the `files/` directory with a placeholder `.gitkeep` file (the actual .docx will be uploaded by the sync script)
- [x] 5.2 Create a `.nojekyll` file in the repository root to ensure GitHub Pages serves all files without Jekyll processing
- [x] 5.3 Verify the complete file structure matches the design: `index.html`, `files/`, `sync/sync_helicopter_schedule.py`, `sync/setup_task_scheduler.md`, `docs/custom-domain-setup.md`, `README.md`
