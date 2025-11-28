# 🚀 GitHub Actions Setup Guide for CEACStatusBot

This guide will help you set up automated CEAC visa status checking on GitHub Actions.

## ✅ Prerequisites

Before starting, make sure you have:

- A GitHub account
- Forked this repository to your GitHub account (or pushed your local repo to GitHub)
- Your `.env` file values handy

---

## 📋 Step-by-Step Setup

### Step 1: Push Your Code to GitHub

If you haven't already, push your local repository to GitHub:

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit with CEAC status bot"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/CEACStatusBot.git
git branch -M main
git push -u origin main
```

### Step 2: Set Up GitHub Secrets

GitHub Secrets keep your sensitive information (passwords, tokens, etc.) encrypted and secure.

1. **Go to your repository on GitHub**

   - Visit: `https://github.com/YOUR_USERNAME/CEACStatusBot`

2. **Navigate to Settings → Secrets and variables → Actions**

   - Click on the **Settings** tab (top menu)
   - Click **Secrets and variables** in the left sidebar
   - Click **Actions**

3. **Add the following secrets** by clicking **"New repository secret"** for each:

   | Secret Name       | Value (from your `.env` file) | Example/Notes                     |
   | ----------------- | ----------------------------- | --------------------------------- |
   | `LOCATION`        | NEPAL, KATHMANDU              | Must match LOCATION.md format     |
   | `NUMBER`          | AA00F4BXJT                    | Your Application ID               |
   | `PASSPORT_NUMBER` | 11040400                      | Your passport number              |
   | `SURNAME`         | DHUNG                         | First 5 letters of surname        |
   | `GH_TOKEN`        | github_pat_11AMMY7LQ0...      | Your GitHub Personal Access Token |
   | `TIMEZONE`        | Asia/Kathmandu                | Your timezone                     |
   | `ACTIVE_HOURS`    | 08:00-22:00                   | Notification active hours         |
   | `FROM`            | ahkongtmoktan@gmail.com       | Sender email                      |
   | `TO`              | dhunganaswaroop@gmail.com     | Recipient email                   |
   | `PASSWORD`        | hwvm djcy jjuz tfzp           | Email app password                |
   | `SMTP`            | smtp.gmail.com:465            | SMTP server                       |

   **Optional (if not using, leave empty):**

   - `TG_BOT_TOKEN` - Telegram bot token (leave blank if not using)
   - `TG_CHAT_ID` - Telegram chat ID (leave blank if not using)

### Step 3: Enable GitHub Actions

1. **Go to the Actions tab** in your repository
2. If workflows are disabled, click **"I understand my workflows, go ahead and enable them"**

### Step 4: Test the Workflow

1. **Manual Test Run:**

   - Go to **Actions** tab
   - Click on **"run main.py"** workflow in the left sidebar
   - Click **"Run workflow"** dropdown button (right side)
   - Click the green **"Run workflow"** button
   - Wait 1-2 minutes and refresh the page

2. **Check the Results:**

   - Click on the running/completed workflow
   - Click on the **"build"** job
   - Expand each step to see the output
   - Look for: "Current status: Refused - Last updated: 24-Nov-2025"

3. **Verify Email:**
   - If this is the first run, you should receive an email since the status file won't exist on GitHub yet
   - Check your inbox at the `TO` email address

---

## 🔄 How It Works

Once set up, the workflow will:

- ✅ Run automatically **every 2 hours** (00:00, 02:00, 04:00, etc. UTC)
- ✅ Check your CEAC visa status
- ✅ Send email notification **only when status changes**
- ✅ Respect your active hours (08:00-22:00 Kathmandu time)
- ✅ Store status history in artifacts

---

## 📊 Monitoring Your Workflow

### View Workflow Runs

- Go to **Actions** tab to see all workflow runs
- Green checkmark ✅ = Success
- Red X ❌ = Failed (click to see error details)

### Check Status History

1. Go to a completed workflow run
2. Scroll down to **Artifacts** section
3. Download `status-artifact` to see your status history

### Manual Trigger

You can manually run the workflow anytime:

- Go to **Actions** → **run main.py** → **Run workflow**

---

## 🎉 You're All Set!

Your bot will now:

- Check your visa status every 2 hours
- Email you when your status changes from "Refused" to anything else
- Run completely free in GitHub Actions

---

## ⚠️ Important Security Notes

- ✅ **Never commit your `.env` file** to GitHub (it's already in `.gitignore`)
- ✅ All sensitive data is stored in GitHub Secrets (encrypted)
- ✅ Your secrets are never visible in workflow logs
- ✅ Make your repository **public** for unlimited free Actions minutes

---

## 🐛 Troubleshooting

### Workflow Fails

- Check if all secrets are set correctly (Settings → Secrets and variables → Actions)
- Make sure secret names match EXACTLY (case-sensitive)
- Check the workflow run logs for specific error messages

### No Email Received

- Verify your email settings are correct in GitHub Secrets
- Check spam folder
- Verify SMTP port is 465 (not 587)
- Remember: emails only send when status **changes**, not on every run

### Status Not Updating

- Check if CEAC website is accessible
- Verify your LOCATION format matches LOCATION.md
- Check workflow logs for CAPTCHA solving success

---

## 📝 Need Help?

If you encounter issues:

1. Check the workflow logs in the Actions tab
2. Verify all secrets are set correctly
3. Try running the bot locally first: `source venv/bin/activate && python trigger.py`
4. Check for error messages in the workflow output
