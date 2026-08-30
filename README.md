# Digestify

> Your inbox, boiled down to what matters.

Digestify is an automated AI-powered email digest system that reads your Gmail inbox daily, extracts the important stuff, and sends a clean summary straight to Telegram.

Instead of scrolling through dozens of emails every morning, Digestify gives you one short message with the day's real action items, deadlines, mandatory tasks, and time-sensitive notices, while skipping newsletters and promotional noise.

The whole thing runs automatically every day via GitHub Actions, nothing to run locally, nothing to babysit.

## How it works

```
GitHub Actions (8:00 AM IST daily)
        ↓
main.py
        ↓
Gmail API
(fetch emails from the last 24h)
        ↓
LangChain agent
        ↓
Mistral LLM
(extract action items only)
        ↓
Send summary
to Telegram
```

## Features

- Fetches emails from the last 24 hours via the Gmail API
- Uses an LLM (Mistral, via LangChain) to filter out only real action items — deadlines, mandatory tasks, restricted-entry notices, etc.
- Ignores optional, informational, or promotional emails
- Sends the digest straight to Telegram as a formatted message
- Runs entirely on GitHub Actions on a daily schedule (8:00 AM IST), free, serverless, set-and-forget
- Can also be triggered manually via workflow_dispatch

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aeonioo/Digestify.git
cd Digestify
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the Gmail API and generate token.json

1. Enable the Gmail API in the [Google Cloud Console](https://console.cloud.google.com/).
2. Create an OAuth Client ID (Desktop app) and download `credentials.json`.
3. `main.py` expects a `token.json` to already exist — it does not run the OAuth flow itself. Generate `token.json` once, locally, using a short OAuth script (e.g. `InstalledAppFlow.from_client_secrets_file` with the `https://www.googleapis.com/auth/gmail.readonly` scope), authorize in the browser, and save the resulting credentials to `token.json`.

### 4. Set up Telegram

Create a bot via [@BotFather](https://t.me/BotFather) and note down the bot token and your chat ID.

### 5. Get a Mistral API key

Sign up at [Mistral AI](https://mistral.ai/) and generate an API key.

### 6. Add GitHub Actions secrets

In your repo, go to **Settings -> Secrets and variables -> Actions** and add:

| Secret | Value |
|---|---|
| `TOKEN_JSON` | The full contents of your local `token.json` file |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `MISTRAL_API_KEY` | Your Mistral API key |

### 7. Enable the workflow

Push to `main`. The workflow in `.github/workflows/daily.yml` runs automatically every day at 8:00 AM IST, and can also be triggered manually from the Actions tab.

## Tech Stack

- Python
- Gmail API
- LangChain
- Mistral (LLM)
- Telegram Bot API
- GitHub Actions

## Project Structure

```
Digestify/
├── .github/workflows/
│   └── daily.yml
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── .python-version
└── README.md
```

---

Built to keep your inbox out of your head, and in one message instead.
