---
title: DriveBase PRO
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: true
---

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/1/12/Google_Drive_icon_%282020%29.svg" width="80" alt="Google Drive Logo">
  <h1>DriveBase PRO 🚀</h1>
  <p><b>The Ultimate High-Speed Google Drive Proxy & Streaming Platform</b></p>
  <p><i>One-Click Google Sign-In · Database Persistence · Multi-Drive · Always Online</i></p>
</div>

<p align="center">
  <b><a href="https://dotsrival-reclone.hf.space">🔥 Live Demo 🔥</a></b>
</p>

<hr>

## 🌟 What is DriveBase PRO?

DriveBase PRO is a completely custom-built, heavily optimized **Google Drive proxy engine** designed and engineered by **DOTSRIVAL**. Built on **FastAPI + asyncio + httpx**, it acts as a robust high-performance streaming server.

Designed for **Anime/Movie websites, File Hosts, and heavy downloaders** who need to bypass Google Drive's strict quota errors and serve files at maximum speed.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔑 **One-Click Google Sign-In** | Add Google Drives using OAuth2 — no manual token generation needed |
| 🌐 **Global OAuth App** | Set Client ID & Secret once in Settings → all users reuse it |
| 💾 **Full Database Persistence** | All drives, users, and settings saved permanently to **PostgreSQL / MongoDB** |
| 🚀 **High-Speed Proxy** | Async streaming engine; supports `Range` headers for IDM/ADM multi-connection downloads |
| 📊 **Real-Time Analytics** | Live data transfer (MB/GB) and unique active user count in the top bar |
| 🔒 **Expiring Signed Links** | HMAC-signed URLs that expire after X hours — stop link stealers |
| 🛑 **Speed Limiter** | Set per-connection bandwidth cap (MB/s) to prevent server abuse |
| 🎬 **In-Browser Player** | Stream 1080p video natively — no download needed |
| 👥 **Multi-User Auth** | Login / Register system with Admin, User, and Guest roles |
| 🔐 **Admin-Only Settings** | Settings gear hidden from guests and users — only Admin can configure |
| 🛡️ **Anti-Bot Proxy** | Fully proxied stream; bypasses Google's "Automated Bot" quota errors |
| ⏰ **Keep-Alive** | Self-ping every 25 minutes to prevent Hugging Face sleep mode |

---

## 🔑 New: Global OAuth2 — One Setup, Unlimited Drives

No more manual `Refresh Token` generation! DriveBase PRO now supports a **centralized OAuth2 flow**:

1. **Admin** goes to Settings → **🔑 OAuth App** tab
2. Enters the **Global Client ID** and **Client Secret** (from Google Cloud Console) — saved to DB
3. When **anyone** adds a new drive → clicks **🔑 Fill from OAuth App** → credentials auto-fill
4. Clicks **Sign in with Google** → picks Gmail account → grants permission
5. `Refresh Token` is automatically retrieved and filled → click **Save Drive** → done!

Multiple Gmail accounts can be connected — each gets its own drive entry with its own refresh token.

---

## 🔐 Authentication & User Roles

| Role | Access |
|---|---|
| **Admin** | Full access — Settings, Drive management, User list, OAuth config |
| **Registered User** | Browse and stream files — no settings access |
| **Guest** | Browse and stream files without an account |

- Admin credentials are set via `ADMIN_USER` and `ADMIN_PASS` environment variables
- Default: `admin` / `admin123` (change this in HF Secrets!)
- All registered users stored in the database

---

## ⚡ Deployment Guide (Hugging Face Spaces)

### Step 1: Create a Free Database

Go to [neon.tech](https://neon.tech) and create a free PostgreSQL database. Copy the `DATABASE_URL` connection string.

> **Alternatively:** Use MongoDB Atlas free tier and set `DATABASE_URL` to your MongoDB URI.

### Step 2: Deploy to Hugging Face

1. Go to [huggingface.co](https://huggingface.co) → **New Space**
2. Choose **Docker** SDK → **Blank** template
3. Upload all files from this repo (`app.py`, `Dockerfile`, `requirements.txt`, `preview.html`)
4. HF will auto-build from the `Dockerfile`

### Step 3: Configure Secrets

Go to Space **Settings → Variables and Secrets** and add:

| Secret Name | Value | Required |
|---|---|---|
| `DATABASE_URL` | Your NeonDB / MongoDB URL | ✅ Yes |
| `ADMIN_USER` | Your admin username | Optional (default: `admin`) |
| `ADMIN_PASS` | Your admin password | Optional (default: `admin123`) |
| `APP_SECRET` | Any random string for link signing | Optional |

> ⚠️ `SPACE_HOST` is **automatically set by Hugging Face** — do NOT add it manually!

### Step 4: Setup Google OAuth App

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project → Enable **Google Drive API**
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**
4. Application type: **Web Application**
5. Add to **Authorized Redirect URIs**:
   ```
   https://YOUR-SPACE-NAME.hf.space/preview.html
   ```
6. Copy the `Client ID` and `Client Secret`

### Step 5: Add Your First Drive

1. Open your DriveBase PRO URL
2. Login as Admin
3. Click ⚙️ Settings → **🔑 OAuth App** tab
4. Enter `Client ID` and `Client Secret` → click **Save OAuth App Settings**
5. Go to **☁ Drives** tab → click **Add Drive**
6. Click **🔑 Fill from OAuth App** → credentials auto-fill
7. Click **Sign in with Google** → choose Gmail account → allow access
8. Enter a Drive Name → click **Save Drive** → ✅ Done!

---

## 🌍 Alternative Hosting

Since the app is fully Dockerized, you can deploy anywhere:

```bash
# Clone the repo
git clone https://github.com/DOTSRIVAL/DriveBase-PRO.git
cd DriveBase-PRO

# Build and run with Docker
docker build -t drivebase .
docker run -d -p 7860:7860 \
  -e DATABASE_URL="your_db_url" \
  -e ADMIN_USER="admin" \
  -e ADMIN_PASS="yourpassword" \
  drivebase
```

Works on: **Koyeb, Render, Railway, Contabo VPS, Hetzner, AWS, DigitalOcean**

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI + asyncio |
| HTTP Client | httpx (async streaming) |
| Database | PostgreSQL (psycopg2) or MongoDB (pymongo) |
| Frontend | Vanilla HTML/CSS/JS (single file) |
| Auth | Custom JWT-like token + HMAC signing |
| Hosting | Docker (Hugging Face Spaces) |

---

## 🔧 Pro Tips for Webmasters

- **Remote Upload:** Copy DriveBase direct links and paste into Vidmoly/Vidoza remote upload — transfers 500MB in under 60 seconds!
- **IDM/ADM Support:** DriveBase supports HTTP `Range` headers, allowing 16 parallel connections — max download speeds!
- **Link Expiry:** Enable HMAC Link Security in Settings. Embed signed URLs on your site — they expire after X hours, preventing scraping.
- **Speed Limiter:** Set 1.5 MB/s per user to fairly distribute bandwidth across your audience.
- **Multiple Drives:** Connect unlimited Gmail accounts, each with its own isolated Google Drive.

---

## ⚖️ Disclaimer

This project is designed for personal backups and webmaster file management. Please ensure you comply with Google Drive's Terms of Service and applicable copyright laws when distributing content.

---

<div align="center">
  <b>Built with ❤️ by DOTSRIVAL</b><br>
  <a href="https://github.com/DOTSRIVAL/DriveBase-PRO">GitHub</a>
</div>
