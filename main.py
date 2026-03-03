# IMPORTS
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
import base64
from dataclasses import dataclass
import re
import os
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") 


# EMAIL FETCH LOGIC

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Use token.json generated locally
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('gmail', 'v1', credentials=creds)

results = service.users().messages().list(
    userId='me',
    q='newer_than:1d'
).execute()

messages = results.get('messages', [])

print("Emails in last 24 hours:", len(messages))

for msg in messages:
    email = service.users().messages().get(
        userId='me',
        id=msg['id']
    ).execute()
    
import base64

emails_list = []

for i, msg in enumerate(messages, start=1):
    email = service.users().messages().get(userId='me', id=msg['id']).execute()
    
    # Extract headers
    headers = email['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    time = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')

    # Extract plain text body
    def get_body(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        # fallback
        data = payload.get('body', {}).get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')
        return ""
    
    body = get_body(email['payload'])
    
    body_clean = body.replace('\r\n', '\n').strip()       # normalize newlines
    body_clean = re.sub(r'\*', '', body_clean)           # remove asterisks

    # Add structured email to list
    emails_list.append({
        "email_no": i,
        "sender": sender,
        "subject": subject,
        "body": body_clean,
        "time": time
    })

# LANGCHAIN + LLM LOGIC

model = ChatMistralAI(
    model="mistral-large-latest",   # or "mistral-small-latest"
    temperature=0,
)

system_prompt = f"""
You are an AI inbox assistant.

Your task: Read the emails provided and return a **clean, concise list of only real action items** that require attention today or in the near future.

Rules:
1. Include only tasks or events that are **mandatory, have deadlines, or require user action**.
2. Include campus events that have rules, deadlines, or restrictions (e.g., Holi celebrations, official notices).
3. Ignore optional tasks, informational messages, newsletters, or promotional content.
4. Output a **numbered list**, 1–3 lines per item.
5. Do NOT create extra sections, headings, or repeat information.
6. If multiple instructions are in the same email, combine them into a single action item where possible.

Format the output exactly like this:

<b> Daily Inbox Action Summary </b>
━━━━━━━━━━━━━━━━━━
Date: {datetime.now().strftime("%d %b %Y")}
Total Emails Today: {len(messages)}

<action items> 

━━━━━━━━━━━━━━━━━━
This summary includes only important and time-sensitive tasks.
"""

user_message = f"""
Here are the emails received in the last 24 hours:

{emails_list}

Please extract a **balanced list of actionable items** based on your instructions (keep one line gap between them)

RULES: DO NOT USE ** IN THE WHOLE OUTPUT
"""
    
agent = create_agent(
    model = model,
    system_prompt=system_prompt,
)

response = agent.invoke({
    "messages": [
    {"role": "user", "content": user_message}
    ]}
)

output_content = response['messages'][-1].content


# DISPLAYING OUTPUT ON TELEGRAM BOT

def send_to_telegram(content: str):
    """
    Sends the summary text to Telegram.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": content,
        "parse_mode": 'HTML'  # optional, for bold/italics formatting
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Summary sent to Telegram successfully")
    else:
        print(f"Failed to send message: {response.status_code} | {response.text}")
        
send_to_telegram(output_content)






    
