import os
import threading
import google.generativeai as genai
import telebot
from flask import Flask

TELEGRAM_TOKEN = "8779960615:AAEyUq4t6HESTGtaIUWncRtedI01J6kxd7A"
GEMINI_API_KEY = "AQ.Ab8RN6LjxiA6AoeHYq7NQfxzoTsdZWR_FONYay4q-9NadiYqBg"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running 24/7!"


@bot.message_handler(commands=["start"])
def start_freelance(message):
  bot.reply_to(
      message,
      "Welcome to **FreelancePitch Bot**! 🚀\n\nStruggling to win clients on"
      " Upwork or Fiverr? Send me a short description of the project you want"
      " to apply for, and I will generate a high-converting, professional"
      " proposal for you in seconds.",
      parse_mode="Markdown",
  )


@bot.message_handler(func=lambda message: True)
def generate_proposal(message):
  project_desc = message.text
  waiting_msg = bot.reply_to(
      message, "⏳ Crafting your professional proposal... Please wait."
  )
  try:
    prompt = (
        "Act as an expert freelance copywriter. Write a professional,"
        " high-converting, and persuasive freelance proposal/cover letter"
        " in English for the following project description. Keep it concise,"
        " engaging, and results-oriented:\n\n"
        f"Project: {project_desc}"
    )
    response = model.generate_content(prompt)
    proposal_text = response.text
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=waiting_msg.message_id,
        text=(
            "🎯 **Generated Professional Proposal:**\n\n"
            f"{proposal_text}\n\n"
            "💡 *Tip: Copy it, tweak any specifics, and win that client!*"
        ),
        parse_mode="Markdown",
    )
  except Exception as e:
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=waiting_msg.message_id,
        text=(
            "❌ Sorry, an error occurred while generating the proposal."
            " Please try again later."
        ),
    )


def run_bot():
  bot.infinity_polling()


if __name__ == "__main__":
  t = threading.Thread(target=run_bot)
  t.start()
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)

