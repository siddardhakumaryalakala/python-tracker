# 🐍 Python 30-Day Mastery Tracker & Daily Push Hub

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black.svg?logo=vercel&logoColor=white)](https://vercel.com/)
[![GitHub Actions](https://img.shields.io/badge/Automated%20Alerts-GitHub%20Actions-2088FF.svg?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![ntfy.sh](https://img.shields.io/badge/Push%20Notifications-ntfy.sh-brightgreen.svg?logo=pushover&logoColor=white)](https://ntfy.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, full-stack **Python 30-Day Mastery Tracker** designed to build bulletproof daily coding discipline. Combines an interactive glassmorphic web dashboard with **automated daily cloud push notifications**, a **1-hour deep study timer**, and **two-way mobile sync** — 100% free with **zero API keys, zero signups, and zero paid infrastructure**.

---

## ✨ Features

- 📱 **Real-Time Mobile Push Notifications (`ntfy.sh`)**:
  - Receive your daily curriculum, key concepts, and 1-hour study framework directly on your phone every morning.
  - Interactive Action Button: Tap **`[Mark Day X Done]`** directly on the phone alert or reply **`DONE`** to automatically check off the task on your web dashboard.
- ⏰ **24/7 Cloud Automation (GitHub Actions)**:
  - Runs automatically on GitHub's cloud servers every day at your chosen time (defaults to **09:00 AM IST**). Your personal computer does **not** need to stay turned on.
- 🌐 **Interactive Web Dashboard**:
  - **Sleek Dark Glassmorphism UI** with smooth CSS animations and real-time progress percentage bar.
  - **Curriculum Filters**: Toggle between *All Days (30)*, *Today's Focus*, *Pending*, and *Completed*.
  - **Copy-Ready Code**: Syntax-highlighted code snippets with 1-click clipboard copy for each of the 30 days.
- ⏱ **1-Hour Study Protocol Timer**:
  - Built directly into the dashboard following the proven 4-phase protocol:
    1. **15 mins**: Learn Concept & Read Documentation
    2. **25 mins**: Code Yourself (Hands-on in VS Code)
    3. **15 mins**: Solve Problems & Edge Cases
    4. **5 mins**: Review, Note-Taking & Git Commit
- ⚙ **Full In-App Customization**:
  - Change your `ntfy` topic name, challenge start date, and reminder time directly from the **⚙ Settings** modal.
  - Includes a safe **🔄 Reset All Tasks** button that permanently resets progress back to 0% with reload protection.
- 💻 **Dual Mode**:
  - **Cloud Mode**: Host statically on **Vercel** with GitHub Actions handling automated cloud alerts.
  - **Local Mode**: Run `python local_server.py` for a self-hosted desktop app with background scheduler and local listener.

---

## 🗺 30-Day Python Mastery Syllabus

| Week | Focus Area | Core Topics |
| :--- | :--- | :--- |
| **Week 1** | **Python Foundations** *(Days 1–7)* | Setup, Variables, Primitives, Operators, Slicing, Lists, Tuples, Sets, Dictionaries, Conditionals & Truthiness |
| **Week 2** | **Logic & Problem Solving** *(Days 8–12)* | `for` / `while` Loops, Patterns, Fibonacci, Functions, `*args`/`**kwargs`, Scopes (LEGB), List & Dict Comprehensions |
| **Week 3** | **Intermediate Python** *(Days 13–18)* | Modules, Exception Handling (`try/except/finally`), File I/O (JSON/CSV), `map`/`filter`/`reduce`, Generators, Decorators |
| **Week 4** | **OOP, APIs & Capstone** *(Days 19–30)* | Classes & Objects, Inheritance, CRUD App, HTTP Requests, Web Scraping, SQLite3, Type Hints, Concurrency, NumPy, Pandas, **Sales Analytics Capstone** |

---

## 🏗 Architecture & Flow

```
                +------------------------------------+
                |  GitHub Actions (Cloud 24/7 Cron)  |
                |   - Runs daily at 09:00 AM IST     |
                |   - Executes daily_reminder.py     |
                +-----------------+------------------+
                                  |
                                  v
                        [ ntfy.sh Topic Hub ]
                         (https://ntfy.sh)
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  📱 Your Mobile Phone |                   |  🌐 Vercel Dashboard  |
|  - Rings Notification |                   |  - Glassmorphic UI    |
|  - "Mark Day X Done"  |=== (SSE Stream) =>|  - Real-time Checkoff |
|    or reply "DONE"    |                   |  - 1-Hour Timer       |
+-----------------------+                   +-----------------------+
```

---

## 🚀 Quick Setup & Deployment

### Step 1: Deploy Frontend to Vercel (Free)

1. Fork or push this repository to your **GitHub** account.
2. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
3. Import your GitHub repository.
4. Leave settings as default (`Framework Preset: Other`) and click **Deploy**.
5. Your dashboard is now live worldwide!

---

### Step 2: Get Alerts on Your Phone (ntfy)

1. Install the free **ntfy** app on your phone:
   - [Android (Google Play)](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
   - [iOS (App Store)](https://apps.apple.com/app/ntfy/id1625396347)
   - Or open [https://ntfy.sh](https://ntfy.sh) in any mobile browser.
2. In the app, tap **Subscribe to topic** and enter:
   ```text
   python-tracker
   ```
   *(Or enter any custom topic name you chose in Settings).*

---

### Step 3: Automate Daily Cloud Alerts (GitHub Actions)

The workflow `.github/workflows/daily_reminder.yml` is already included.

- **Automated Schedule**: GitHub Actions will automatically wake up every morning at **09:00 AM IST** (03:30 UTC), run `daily_reminder.py`, and push today's study challenge to your phone.
- **Manual Test Alert**:
  1. Open your repository on GitHub.
  2. Navigate to **Actions** &rarr; **Daily Python Roadmap Notification**.
  3. Click **Run workflow** &rarr; **Run workflow**.
  4. Your phone will receive the push alert immediately!

---

## 🖥 Local Desktop Mode (Optional)

If you prefer to run the entire backend and frontend locally on your PC:

```bash
# Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Install requests
pip install requests

# Start the full-stack local server
python local_server.py
```

The app will start at `http://127.0.0.1:5000` and automatically open your default browser. It includes:
- Live scheduler loop running in a background thread.
- Direct inbound listener for phone `DONE` replies.
- Local persistence via `config.json`.

---

## ⏰ Customizing Your Daily Alert Time

To change when GitHub Actions sends your daily notification:

1. Open `.github/workflows/daily_reminder.yml`.
2. Edit line 6 with your desired UTC cron time:
   ```yaml
   on:
     schedule:
       - cron: '30 3 * * *' # 03:30 UTC = 09:00 AM IST
   ```
   *Examples for IST (Indian Standard Time = UTC + 5:30):*
   - `00 2 * * *` &rarr; 07:30 AM IST
   - `30 2 * * *` &rarr; 08:00 AM IST
   - `30 3 * * *` &rarr; 09:00 AM IST
   - `30 14 * * *` &rarr; 08:00 PM IST
3. Commit the change to GitHub.

---

## 📁 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── daily_reminder.yml    # GitHub Actions 24/7 cloud scheduler
├── index.html                    # Responsive glassmorphism web dashboard
├── daily_reminder.py             # Standalone alert dispatcher for GitHub Actions
├── local_server.py               # Local Python HTTP server & scheduler
├── config.json                   # Topic and application configuration
├── vercel.json                   # Vercel deployment configuration
├── .vercelignore                 # Ensures Vercel handles static deployment cleanly
└── README.md                     # Documentation & setup guide
```

---

## 🛡 Privacy & Transparency

- **No Passwords or Logins**: Uses open public topic pub/sub via [ntfy.sh](https://ntfy.sh).
- **Client-Side Privacy**: Your progress is stored locally in your browser's `localStorage` and optionally on your local machine via `config.json`.
- **Zero Running Costs**: Built with 100% free-tier services (GitHub Actions + Vercel + ntfy).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to fork, customize, and share your learning journey!
