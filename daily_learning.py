import os
import smtplib
from email.mime.text import MIMEText
from google import genai

# Read environment variables mn GitHub Secrets
GEMINI_API_KEY =os.getenv ( "AQ.Ab8RN6KEtW0jUATJppUtkbTWO_6G0pvuS1KqJTdhPwdfU3ei7g")  # Key mn Google AI Studio
SENDER_EMAIL = os.getenv("abdellahbenka05@gmail.com")
SENDER_PASSWORD = os.getenv("gvpu qsra mpml lhgn")   # App Password dyal Gmail (16 caractères)
RECEIVER_EMAIL = os.getenv("abdellahbenka05@gmail.com") 

client = genai.Client(api_key=GEMINI_API_KEY)

# Topic d l-yowm
topic = "Fundamentals - Variables and Data Types in Python"

prompt = f"""
Enseignez-moi la leçon du jour en Python de manière très simple et claire f Darija Marocaine m3a Français.

Sujet: {topic}

Structure du cours:
1. Explication simple du concept.
2. Exemples de Code Python facile.
3. Exercice pratique m3a Solution.
"""

# 1. Générer Dars mn Gemini
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

# 2. Setup Email
msg = MIMEText(response.text, 'plain', 'utf-8')
msg['Subject'] = f"📚 Dars Python: {topic}"
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

# 3. Sift Email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print("✅ Dars t-sift f l-email successfully!")