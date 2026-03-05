# AI Inbox Digest 

An automated **AI-powered email digest system** that reads your Gmail inbox daily, extracts important information, and sends a concise summary to **Telegram**.

Instead of manually reading dozens of emails, the system generates a clean daily digest containing:
- Important updates
- Action items
- Key highlights from emails

The workflow runs automatically every day using **GitHub Actions**, so your inbox gets summarized without running anything locally.

# Architecture
    
    GitHub Actions (8 AM daily)
            ↓
    Python Script
            ↓
    Gmail API
    (fetch last 24h emails)
            ↓
    LangChain
            ↓
    LLM (Mistral)
            ↓
    Extract:
       - Important Digest
       - Action Items
            ↓
    Send Summary
    to Telegram

# Setup

## Clone the Repository

    git clone https://github.com/yourusername/ai-inbox-digest.git
    cd ai-inbox-digest

## Install Dependencies

    pip install -r requirements.txt

## Setup Gmail API

Enable the Gmail API in the Google Cloud Console, create an OAuth Client ID, and download the credentials.json. Run the script locally once to generate token.json, then use these credentials to integrate Gmail with your Telegram bot and automate it through GitHub Actions.


