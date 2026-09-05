import os
import time
import schedule
import smtplib
from email.mime.text import MIMEText
from google import genai

# ==========================================
# 1. CONFIGURATION (Bdl had l-ma'loumat)
# ==========================================
GEMINI_API_KEY =os.getenv ( "AQ.Ab8RN6KEtW0jUATJppUtkbTWO_6G0pvuS1KqJTdhPwdfU3ei7g")  # Key mn Google AI Studio
SENDER_EMAIL = os.getenv("abdellahbenka05@gmail.com")
SENDER_PASSWORD = os.getenv("gvpu qsra mpml lhgn")   # App Password dyal Gmail (16 caractères)
RECEIVER_EMAIL = os.getenv("abdellahbenka05@gmail.com") # Email dyalak fash ghadi t-sta3bel dars

# Client Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# 2. PLAN DIAL L-9RAYA (Modules par Jour)
# ==========================================
LEARNING_PLAN = [
    "Jour 1: Fundamentals - Variables, Data Types (int, string, float), print() and input()",
    "Jour 2: Control Flow - If, Else, Elif, and Logical Operators",
    "Jour 3: Loops - For loops, While loops, and range() function",
    "Jour 4: Functions - Defining functions, parameters, and return values",
    "Jour 5: Data Structures - Lists, Tuples, and basic operations",
    "Jour 6: Data Structures - Dictionaries and Sets",
    "Jour 7: Practice Day - Write a mini project combining all 6 days!"
]

# Track d n-nhar l-current
current_day_index = 0

# ==========================================
# 3. FONCTIONS DIAL E-MAIL & GEMINI
# ==========================================
def send_email(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Dars d l-yowm t-sift f l-email successfully!")
    except Exception as e:
        print(f"❌ Khata' f tsfat d e-mail: {e}")

def daily_python_lesson():
    global current_day_index
    
    if current_day_index >= len(LEARNING_PLAN):
        print("🎉 Mabrouk! Saliti l-program dyal l-9raya!")
        return

    topic = LEARNING_PLAN[current_day_index]
    print(f"⏳ Gemini ghadin y-générer l-dars dyal: {topic}")

    prompt = f"""
    Enseignez-moi la leçon du jour en Python de manière très simple et claire f Darija Marocaine m3a Français.
    
    Sujet: {topic}
    
    Structure du cours:
    1. Explication simple du concept (avec exemples de la vie réelle).
    2. Exemples de Code Python facile.
    3. Exercice pratique (Mini-challenge) avec la solution à la fin.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        lesson_content = response.text
        subject = f"📚 Dars Python d l-Yowm ({topic.split(':')[0]})"
        
        # Send Email
        send_email(subject, lesson_content)
        
        # Passage au jour suivant
        current_day_index += 1
    except Exception as e:
        print(f"❌ Khata' f Gemini API: {e}")

# ==========================================
# 4. SCHEDULER (Kulla Sba3 f Sa3a 13:00 PM)
# ==========================================
# T9der t-bdl "13:00" b l-wa9t li bghiti
schedule.every().day.at("13:00").do(daily_python_lesson)

print("🚀 Script khddam! Ghadi y-sift dars kulla sba3 f 13:00 PM...")

# Loop dyal l-wa9t (Keep script alive)
while True:
    schedule.run_pending()
    time.sleep(60)