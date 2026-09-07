import os
import smtplib
from email.mime.text import MIMEText
from google import genai

# Load local .env file if it exists (for local running)
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# Read environment variables (supports GitHub Secrets and local .env)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", SENDER_EMAIL)

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1beta'}
)
# Topic d l-yowm
topic = "Fundamentals - Variables and Data Types in Python"

prompt = f"""
Anta ostad kbir f Python. 3tini dars d l-yowm b tariqa tatbiqiya 100% (pratique w hands-on) f Darija Marocaine m3a Français.

Sujet: {topic}

Kteb l-contenu kamel b HTML nqi w design m-style b CSS inline (fond sombre/clair zwin, code blocks mefrouzin, boutons w liens cliquables) fih had l-ajzaa2:
1. 💡 **L-Mafhoum b Khtissar:** Chno howa had l-concept w 3lach kaynfe3 f l-waqi3 (b Darija sahla).
2. 💻 **Code Tatbiqi (Hands-on):** Amthila dyal bseh mchrou7in bl-code.
3. 🛠️ **Tamrin / Challenge Tatbiqi:** Exercice b Darija bach n-tbe9 biya w f l-lekher l-7ell dialo m3a l-chere7.
4. 🎥 **A7san Vidéos Ta3limiya (Masadir I7tirafiya):**
   - 3tini a7san vidéos li y-choufhüm f had l-mawdo3 (b7al FreeCodeCamp, Corey Schafer, Bro Code, wlla chanat b Darija).
   - Dir bouton wlla lien direct cliquable l YouTube search:
     <p style="margin-top: 15px;">
       <a href="https://www.youtube.com/results?search_query=python+{topic.replace(' ', '+')}+tutorial" 
          style="background-color: #FF0000; color: white; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
          ▶️ Tferrej f a7san vidéos f YouTube 3la had Dars
       </a>
     </p>

Mat-zidch doctype w html/head tags, 3tini ghir div stylé b CSS inline li y-ban zwin f Gmail.
"""

# 1. Générer Dars mn Gemini
response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=prompt
)

# N9i l-HTML mn backticks ila kano
email_html = response.text.strip()
if email_html.startswith("```html"):
    email_html = email_html[7:]
elif email_html.startswith("```"):
    email_html = email_html[3:]
if email_html.endswith("```"):
    email_html = email_html[:-3]
email_html = email_html.strip()

# 2. Setup Email b format HTML
msg = MIMEText(email_html, 'html', 'utf-8')
msg['Subject'] = f"📚 Dars Python Tatbiqi: {topic}"
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

# 3. Sift Email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD.replace(" ", ""))
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print("[OK] Dars t-sift f l-email successfully!")