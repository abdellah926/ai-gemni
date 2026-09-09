import os
import smtplib
from datetime import date, datetime
from email.mime.text import MIMEText

from google import genai
from dotenv import load_dotenv

load_dotenv()

def load_local_env():
    """Load a local .env file without overwriting GitHub Actions secrets."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


COURSE_STAGES = [
    "Foundation: essential concepts and vocabulary",
    "Setup and tools: professional environment and workflow",
    "Core skills: the most important concepts and techniques",
    "Intermediate practice: solve realistic problems",
    "Building: create useful small projects",
    "Quality: testing, debugging, documentation, and best practices",
    "Integration: tools, APIs, data, and collaboration where relevant",
    "Security and performance: safe, reliable, efficient work",
    "Production: deployment, maintenance, and professional workflow",
    "Expert practice: portfolio projects and advanced real-world cases",
]


def get_today_lesson():
    course_start = os.environ.get("COURSE_START_DATE", "2026-09-08")
    try:
        start_date = datetime.strptime(course_start, "%Y-%m-%d").date()
    except ValueError as error:
        raise RuntimeError("COURSE_START_DATE must use YYYY-MM-DD format.") from error

    elapsed_days = (date.today() - start_date).days
    if elapsed_days < 0:
        raise RuntimeError("COURSE_START_DATE cannot be in the future.")

    course_day = elapsed_days + 1
    stage_index = min((course_day - 1) // 7, len(COURSE_STAGES) - 1)
    return course_day, stage_index, COURSE_STAGES[stage_index]


def get_required_settings():
    settings = {
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
        "SENDER_EMAIL": os.environ.get("SENDER_EMAIL"),
        "SENDER_PASSWORD": os.environ.get("SENDER_PASSWORD"),
        "RECEIVER_EMAIL": os.environ.get("RECEIVER_EMAIL"),
        "COURSE_SUBJECT": os.environ.get("COURSE_SUBJECT", "Python"),
    }
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required settings: {', '.join(missing)}")
    return settings


def main():
    load_local_env()
    settings = get_required_settings()
    course_day, stage_index, stage = get_today_lesson()
    subject = settings["COURSE_SUBJECT"]
    progress = f"Dars {course_day} | Mar7ala {stage_index + 1}/{len(COURSE_STAGES)}"

    prompt = f"""
You are an expert teacher. Create today's professional, practical lesson in Moroccan Darija with simple French where useful.

This is {progress} of an ordered roadmap for the subject below. The current stage is: {stage}

Subject: {subject}

Choose exactly one new, concrete lesson that belongs to this stage and is useful for becoming professional in this subject. Build on earlier days. Never repeat a previous lesson. State the selected lesson title clearly at the top of the email.

Return only a clean HTML div with inline CSS that works in Gmail. Do not include markdown fences, doctype, html, or head tags. Use a clean, readable, professional design.

Include these sections:
1. Lesson title and roadmap progress.
2. A concise explanation in easy Darija: what it is, why it matters, and when professionals use it.
3. A hands-on code example with a clear line-by-line explanation.
4. A realistic practice challenge in Darija, followed by a separate complete solution and explanation.
5. Common mistakes and professional tips.
6. A clickable YouTube search link for a high-quality tutorial about this exact topic.

The lesson must be self-contained, accurate, and suitable for someone progressing toward professional-level work in this subject.
"""

    client = genai.Client(
        api_key=settings["GEMINI_API_KEY"],
        http_options={"api_version": "v1beta"},
    )
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    email_html = response.text.strip()
    if email_html.startswith("```html"):
        email_html = email_html[7:]
    elif email_html.startswith("```"):
        email_html = email_html[3:]
    if email_html.endswith("```"):
        email_html = email_html[:-3]

    message = MIMEText(email_html.strip(), "html", "utf-8")
    message["Subject"] = f"{subject} | {progress}"
    message["From"] = settings["SENDER_EMAIL"]
    message["To"] = settings["RECEIVER_EMAIL"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings["SENDER_EMAIL"], settings["SENDER_PASSWORD"].replace(" ", ""))
        server.sendmail(settings["SENDER_EMAIL"], settings["RECEIVER_EMAIL"], message.as_string())

    print(f"[OK] {progress} sent for {subject} ({stage})")


if __name__ == "__main__":
    main()
