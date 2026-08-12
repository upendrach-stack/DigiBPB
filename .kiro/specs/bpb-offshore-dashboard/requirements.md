# Requirements Document

## Introduction

A digital dashboard for BPB Offshore Platform (NH&BS Asset, Mumbai Offshore) that provides a modern, professional single-page web application. The dashboard serves as a centralized hub for quick access to critical offshore operational resources, starting with daily helicopter schedule downloads. The application follows ONGC corporate branding with a dark navy/teal gradient aesthetic. The dashboard is hosted on GitHub Pages for internet access (e.g., https://ongc-bpb.github.io/bpb-offshore-dashboard) and can optionally be served on the intranet at 10.205.173.28:5009. A Python-based sync script running on the office PC automatically uploads the daily helicopter schedule file from the intranet file server to GitHub using the GitHub REST API.

## Glossary

- **Dashboard**: The single-page web application serving as the main interface for BPB offshore platform digital operations
- **KPI_Card**: A clickable card component displaying a key performance indicator or resource shortcut with icon, title, and description
- **Gradient_Panel**: The left-side navigation/branding panel with dark navy-to-teal gradient background
- **Content_Area**: The right-side main content area with clean white card panels
- **Helicopter_Schedule**: The daily helicopter schedule document hosted on GitHub Pages at the configured URL (e.g., https://{username}.github.io/{repo}/files/Daily_Helicopter_Schedule.docx)
- **Intranet_Server**: The office desktop at IP 10.205.173.28 (has Python and Node.js installed, cannot install git) that optionally hosts the dashboard on port 5009 and runs the automated file sync script
- **Dashboard_Config**: A JavaScript configuration object within the application code where an admin can set configurable values such as download URLs without modifying core application logic
- **Sync_Script**: A Python script running on the Intranet_Server that uploads the daily helicopter schedule file from the intranet file server to the GitHub repository using the GitHub Contents API
- **GitHub_Pages**: GitHub's static site hosting service that serves the dashboard and hosted files at a free public URL (e.g., https://ongc-bpb.github.io/bpb-offshore-dashboard)
- **GitHub_PAT**: A GitHub Personal Access Token stored as an environment variable on the Intranet_Server, used by the Sync_Script to authenticate with the GitHub Contents API

## Requirements

### Requirement 1: Corporate Branding Header

**User Story:** As an offshore platform user, I want to see clear ONGC corporate branding on the dashboard, so that I can identify the application as an official BPB platform tool.

#### Acceptance Criteria

1. THE Dashboard SHALL display the header text "Oil and Natural Gas Corporation Ltd." prominently at the top of the page
2. THE Dashboard SHALL display the subtitle "BPB PLATFORM • NH&BS ASSET • MUMBAI OFFSHORE" below the main header
3. THE Dashboard SHALL use the ONGC corporate color scheme with dark navy and teal accent colors throughout the interface

### Requirement 2: Dark Gradient Side Panel

**User Story:** As an offshore platform user, I want a visually appealing dark gradient side panel, so that the interface feels modern and professional.

#### Acceptance Criteria

1. THE Gradient_Panel SHALL render on the left side of the page with a dark navy-to-teal vertical gradient background
2. THE Gradient_Panel SHALL contain the application branding including title and platform identification
3. THE Gradient_Panel SHALL remain visible and fixed during page scroll on desktop viewports

### Requirement 3: KPI Card for Helicopter Schedule Download

**User Story:** As an offshore platform user, I want a clearly visible KPI card for the daily helicopter schedule, so that I can quickly download the schedule with a single click.

#### Acceptance Criteria

1. THE Content_Area SHALL display a KPI_Card with a helicopter-related icon, a title of "Daily Helicopter Schedule", and a brief description indicating the document type
2. WHEN the user clicks the KPI_Card, THE Dashboard SHALL open or download the file using the URL defined in the Dashboard_Config object under the helicopter schedule download URL key
3. THE Dashboard_Config SHALL store the helicopter schedule download URL with a default value pointing to the GitHub Pages hosted file (e.g., https://{username}.github.io/{repo}/files/Daily_Helicopter_Schedule.docx)
4. THE KPI_Card SHALL display a hover state with a teal/cyan accent color highlight to indicate interactivity
5. IF the download link is unreachable, THEN THE Dashboard SHALL display the KPI_Card in a visually distinct state indicating the resource may be unavailable

### Requirement 4: Modern Card-Based Layout

**User Story:** As an offshore platform user, I want a clean card-based layout for dashboard content, so that information is organized and easy to scan.

#### Acceptance Criteria

1. THE Content_Area SHALL use white or light-colored card panels with subtle shadow and rounded corners for each content section
2. THE Dashboard SHALL arrange KPI_Cards in a responsive grid layout that adapts to different screen widths
3. THE Dashboard SHALL use teal/cyan accent colors for interactive elements, highlights, and status indicators

### Requirement 5: Single-Page Application Hosting on GitHub Pages

**User Story:** As an IT administrator, I want the dashboard hosted on GitHub Pages for internet access, so that offshore and onshore users can access it from any network without complex infrastructure.

#### Acceptance Criteria

1. THE Dashboard SHALL be implemented as a static single-page application using HTML, CSS, and JavaScript without requiring a backend framework
2. THE Dashboard SHALL be hosted on GitHub_Pages providing a free public URL accessible from the internet (e.g., https://ongc-bpb.github.io/bpb-offshore-dashboard)
3. THE Dashboard SHALL optionally be servable from port 5009 on the Intranet_Server at 10.205.173.28 for intranet access
4. THE Dashboard SHALL load all assets from the GitHub Pages hosted repository or inline within the HTML file
5. THE Dashboard SHALL include a Dashboard_Config section (JavaScript configuration object) where the admin can set download URLs and other configurable values without modifying the core application code

### Requirement 6: Footer with Role Indicators

**User Story:** As an offshore platform user, I want to see role-based labels in the footer, so that I understand the intended audience of the dashboard.

#### Acceptance Criteria

1. THE Dashboard SHALL display a footer section containing role-based labels including "Admin", "Departments", "OIM", and "Viewer"
2. THE Dashboard SHALL style role labels as colored indicator badges consistent with the teal/navy theme

### Requirement 7: Custom Domain Support

**User Story:** As an IT administrator, I want guidance on configuring custom domain access for the dashboard, so that users can access it via a friendly URL on both intranet and internet.

#### Acceptance Criteria

1. THE Dashboard SHALL include documentation explaining that GitHub_Pages provides a free public URL by default and that a custom domain can optionally be configured in the GitHub Pages repository settings
2. THE Dashboard SHALL include documentation explaining that a custom intranet domain name (e.g., digiBPB.in) can be resolved to 10.205.173.28 by adding an A record in the internal DNS server for intranet access
3. THE Dashboard SHALL include documentation noting that no domain purchase is required for intranet-only use and that the network/IT admin should be contacted to configure the DNS entry

### Requirement 8: Automated File Sync to GitHub

**User Story:** As an IT administrator, I want the daily helicopter schedule file to be automatically uploaded from the intranet file server to GitHub, so that the latest schedule is always available on the GitHub Pages hosted dashboard without manual intervention.

#### Acceptance Criteria

1. THE Sync_Script SHALL read the helicopter schedule file from the network path \\10.205.122.39\mr\Helicopter Schedule\Daily Helicopter Schedule\Daily Helicopter Schedule.docx
2. THE Sync_Script SHALL upload the file to the GitHub repository using the GitHub Contents API (PUT /repos/{owner}/{repo}/contents/{path}) with the file content encoded in Base64
3. THE Sync_Script SHALL authenticate with the GitHub Contents API using the GitHub_PAT stored as an environment variable on the Intranet_Server
4. THE Sync_Script SHALL be implemented using only the Python requests library without requiring a git binary installation
5. THE Sync_Script SHALL be scheduled to run daily via Windows Task Scheduler on the Intranet_Server
6. IF the network path is unreachable, THEN THE Sync_Script SHALL log an error message indicating the file could not be read from the intranet file server
7. IF the GitHub API request fails, THEN THE Sync_Script SHALL log an error message including the HTTP status code and response details
8. THE Sync_Script SHALL retrieve the existing file SHA from the GitHub repository before uploading to support file updates via the Contents API
