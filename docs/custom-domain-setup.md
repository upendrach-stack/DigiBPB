# Custom Domain Setup Guide

This guide explains how to configure a custom domain for the BPB Offshore Dashboard, covering both internet-facing GitHub Pages and intranet access scenarios.

---

## 1. GitHub Pages Custom Domain (Internet)

By default, the dashboard is accessible at:

```
https://upendrach-stack.github.io/DigiBPB/
```

If you want a custom domain (e.g., `digibpb.com`) for internet access, follow these steps:

### Prerequisites

- You must **purchase a domain name** from a registrar (e.g., GoDaddy, Namecheap, Google Domains).

### Steps

1. **Add a CNAME file to the repository**

   Create a file named `CNAME` in the root of the repository with your custom domain:

   ```
   digibpb.com
   ```

2. **Configure DNS at your domain registrar**

   Add the following DNS records at your registrar:

   | Type  | Name | Value                              |
   |-------|------|------------------------------------|
   | CNAME | www  | upendrach-stack.github.io          |
   | A     | @    | 185.199.108.153                    |
   | A     | @    | 185.199.109.153                    |
   | A     | @    | 185.199.110.153                    |
   | A     | @    | 185.199.111.153                    |

   > The A record IPs are GitHub Pages servers. Check [GitHub docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) for the latest IPs.

3. **Configure custom domain in GitHub Pages settings**

   - Go to your repository on GitHub → **Settings** → **Pages**
   - Under **Custom domain**, enter your domain (e.g., `digibpb.com`)
   - Click **Save**
   - Optionally enable **Enforce HTTPS**

4. **Wait for DNS propagation**

   DNS changes can take up to 24–48 hours to propagate globally.

---

## 2. Intranet Custom Domain (No Purchase Needed)

To access the dashboard on the intranet at a friendly URL like `http://digiBPB.in:5009`, **no domain purchase is needed**. You only need an internal DNS entry.

### Option A: Internal DNS Server (Recommended)

Contact your **network/IT admin** and request them to add an A record in the internal DNS server:

| Type | Name       | Value          |
|------|------------|----------------|
| A    | digiBPB.in | 10.205.173.28  |

Once configured, all users on the intranet can access the dashboard at:

```
http://digiBPB.in:5009
```

### Option B: Local Hosts File (Per-Machine)

If modifying the DNS server is not possible, you can add the mapping on each client PC manually:

1. Open Notepad **as Administrator**
2. Open the file:

   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

3. Add the following line at the end:

   ```
   10.205.173.28  digiBPB.in
   ```

4. Save the file and close Notepad.

After this, the machine can access:

```
http://digiBPB.in:5009
```

> **Note:** This must be done on every client PC that needs access. The DNS server approach (Option A) is preferred for organization-wide access.

---

## 3. Serving the Dashboard on Intranet (Optional)

To serve the dashboard locally on the intranet server (10.205.173.28) on port 5009, use one of the following methods:

### Using Python (pre-installed on server)

```bash
cd "C:\path\to\dashboard\folder"
python -m http.server 5009
```

### Using Node.js (pre-installed on server)

```bash
cd "C:\path\to\dashboard\folder"
npx http-server -p 5009
```

Either command will serve the dashboard files at `http://10.205.173.28:5009` (or `http://digiBPB.in:5009` if DNS is configured).

> **Tip:** To keep the server running in the background, consider creating a Windows Task Scheduler task or running it as a Windows service using tools like `nssm`.

---

## Summary

| Scenario         | URL                                              | Requires Domain Purchase? |
|------------------|--------------------------------------------------|---------------------------|
| GitHub Pages     | https://upendrach-stack.github.io/DigiBPB/       | No (free URL)             |
| Custom Internet  | https://digibpb.com (example)                    | Yes                       |
| Intranet         | http://digiBPB.in:5009                           | No                        |
| Intranet (IP)    | http://10.205.173.28:5009                        | No                        |
