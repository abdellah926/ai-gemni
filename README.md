# 🚀 AI Daily Learning Bot (Powered by Google Gemini)

An automated educational bot that generates and delivers personalized, hands-on daily lessons directly to your inbox every morning at 10:00 AM. 

Built with Python, Google Gemini AI, and GitHub Actions for **100% serverless, cloud-based execution**—no need to keep your computer running!

---

## ✨ Key Features

- **Hands-on Practical Content:** Explains core concepts clearly with real-world, executable code examples.
- **Daily Coding Challenges:** Includes practical exercises and step-by-step solutions to test your understanding.
- **Curated Video Recommendations:** Automatically provides direct links and buttons to top-rated YouTube tutorials (FreeCodeCamp, Corey Schafer, etc.).
- **Rich HTML Email Design:** Modern, clean, responsive email styling with highlighted code blocks.
- **Zero-Maintenance Automation:** Powered by GitHub Actions to run autonomously in the cloud 24/7 for free.

---

## ⚙️ Quick Setup Guide (Takes under 3 minutes)

### Step 1: Get your Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key** and generate a new key.

### Step 2: Generate a Gmail App Password
1. Visit your Google Account Security: [App Passwords](https://myaccount.google.com/apppasswords).
2. Create a new App Password (16 letters, e.g., `gvpuqsrampmllhgn`).  
*(Note: Do not use your regular Gmail password; use this generated 16-character token).*

### Step 3: Configure Credentials

#### Option A: Running in Cloud with GitHub Actions (Recommended)
1. In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add the following 4 secrets:

| Secret Name | Description | Example |
| :--- | :--- | :--- |
| GEMINI_API_KEY | Your Google Gemini API Key | AQ.Ab8RN... |
| SENDER_EMAIL | Your Gmail address used to send emails | you@gmail.com |
| SENDER_PASSWORD | Your 16-character Gmail App Password | bcd efgh ijkl mnop |
| RECEIVER_EMAIL | The recipient address where lessons arrive | you@gmail.com |

#### Option B: Running Locally on your Computer
Create a .env file in the project folder with:
`env
GEMINI_API_KEY=your_gemini_api_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=your_email@gmail.com
`

---

## 🎯 How to Customize

### 1. Change the Topic
Open daily_learning.py and modify the 	opic variable:
`python
topic = "Python - Object-Oriented Programming (OOP)"
`
*(You can change this to any topic: JavaScript, SQL, Cyber Security, Marketing, English, etc.)*

### 2. Change the Schedule
Open .github/workflows/daily.yml and change the cron schedule:
`yaml
schedule:
  - cron: '0 9 * * *'  # Runs every day at 10:00 AM (UTC+1)
`

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **Google GenAI SDK** (google-genai)
- **Python smtplib & email**
- **GitHub Actions** (CI/CD Scheduled Cron)

---

## 📄 License & Terms of Use
Copyright (c) 2026 Abdellah. All rights reserved.

This is a proprietary commercial product. By purchasing or acquiring this software, you are granted a single-user personal/commercial license to run and customize it for your own use. 

You are **NOT** permitted to resell, redistribute, sub-license, or publicly share this source code. See the LICENSE file for full details.
