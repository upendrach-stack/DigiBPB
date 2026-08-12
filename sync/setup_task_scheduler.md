# Setting Up Windows Task Scheduler for Daily Sync

This guide walks you through creating a scheduled task that automatically runs the helicopter schedule sync script every day.

## Prerequisites

- Python installed and accessible from the command line
- `sync_helicopter_schedule.py` script configured and tested manually
- `GITHUB_PAT` environment variable set (see README for instructions)

---

## Method 1: Task Scheduler GUI

### Step 1: Open Task Scheduler

Press `Win + R`, type `taskschd.msc`, and press Enter. Alternatively, search for "Task Scheduler" in the Start menu.

### Step 2: Create a New Task

In the right-hand Actions panel, click **"Create Task..."** (not "Create Basic Task" — this gives more control).

### Step 3: General Tab

| Setting | Value |
|---------|-------|
| **Name** | `BPB_Helicopter_Schedule_Sync` |
| **Description** | Syncs daily helicopter schedule to GitHub Pages |
| **Security options** | Select **"Run whether user is logged on or not"** |
| **Configure for** | Windows 10 (or your OS version) |

> **Note:** You will be prompted for your Windows password when saving the task with "Run whether user is logged on or not" enabled.

### Step 4: Triggers Tab

1. Click **"New..."**
2. Set **Begin the task** to "On a schedule"
3. Select **Daily**
4. Set **Start time** to `06:00:00` (adjust as needed — this should run before office hours so the file is ready)
5. Set **Recur every** to `1` day
6. Ensure **Enabled** is checked
7. Click **OK**

### Step 5: Actions Tab

1. Click **"New..."**
2. Set **Action** to "Start a program"
3. Configure the following:

| Field | Value |
|-------|-------|
| **Program/script** | `python` (or full path, e.g., `C:\Python312\python.exe`) |
| **Add arguments** | `sync_helicopter_schedule.py` |
| **Start in** | Full path to the sync folder, e.g., `C:\Users\Priyanka\OneDrive\Desktop\July2026\Helicopter schedule\sync` |

4. Click **OK**

> **Tip:** If `python` is not in your system PATH, use the full path to `python.exe`. You can find it by running `where python` in Command Prompt.

### Step 6: Conditions Tab

- **Uncheck** "Start the task only if the computer is on AC power" (important for desktops that are always on)
- **Uncheck** "Stop if the computer switches to battery power"
- Optionally check "Wake the computer to run this task" if the PC may be in sleep mode at the scheduled time

### Step 7: Settings Tab

- **Check** "Allow task to be run on demand" (allows manual triggering)
- **Check** "Run task as soon as possible after a scheduled start is missed"
- **Check** "If the task fails, restart every" → set to 5 minutes, up to 3 times
- Set "Stop the task if it runs longer than" → `1 hour`
- Set "If the running task does not end when requested, force it to stop"

### Step 8: Save the Task

Click **OK**. Enter your Windows password when prompted.

---

## Verification Steps

### Check the Task Exists

1. In Task Scheduler, expand **Task Scheduler Library** in the left panel
2. Look for `BPB_Helicopter_Schedule_Sync` in the list
3. Verify the Status shows "Ready"

### Test Run the Task

1. Right-click on `BPB_Helicopter_Schedule_Sync`
2. Select **"Run"**
3. Check the **"Last Run Result"** column — `0x0` means success
4. Verify the file was updated on GitHub by checking the repository

### Check History

1. Select the task in the list
2. Click the **"History"** tab at the bottom
3. Look for "Action completed" and "Task completed" entries
4. If history is disabled, click **"Enable All Tasks History"** in the right Actions panel

---

## Method 2: Command-Line Alternative (schtasks)

For those who prefer the command line, you can create the task using `schtasks`:

```cmd
schtasks /create ^
  /tn "BPB_Helicopter_Schedule_Sync" ^
  /tr "python sync_helicopter_schedule.py" ^
  /sc daily ^
  /st 06:00 ^
  /rl highest ^
  /f
```

### Full path version (recommended):

```cmd
schtasks /create ^
  /tn "BPB_Helicopter_Schedule_Sync" ^
  /tr "C:\Python312\python.exe \"C:\Users\Priyanka\OneDrive\Desktop\July2026\Helicopter schedule\sync\sync_helicopter_schedule.py\"" ^
  /sc daily ^
  /st 06:00 ^
  /rl highest ^
  /f
```

### Useful schtasks commands:

```cmd
:: Check task status
schtasks /query /tn "BPB_Helicopter_Schedule_Sync"

:: Run the task immediately
schtasks /run /tn "BPB_Helicopter_Schedule_Sync"

:: Delete the task
schtasks /delete /tn "BPB_Helicopter_Schedule_Sync" /f

:: Change the scheduled time to 07:30
schtasks /change /tn "BPB_Helicopter_Schedule_Sync" /st 07:30
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task shows "Last Run Result: 0x1" | Script encountered an error. Check that `GITHUB_PAT` env var is set and the network path is accessible. Run the script manually to see the error. |
| Task shows "Could not start" | Verify the python path is correct. Use `where python` to find the full path. |
| Task runs but file not updated | Check that the source file exists at the UNC path. Verify the PAT has not expired. |
| "Run whether user is logged on or not" greyed out | You need administrator privileges. Right-click Task Scheduler and select "Run as Administrator". |
| Task doesn't run at scheduled time | Ensure the PC is powered on. Check the Conditions tab settings. Enable "Run task as soon as possible after a scheduled start is missed". |
