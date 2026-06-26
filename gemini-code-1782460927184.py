# Define the content for the updated bot.py and requirements.txt
requirements_content = """python-telegram-bot==21.6
groq==0.9.0
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.2.2
python-dotenv==1.0.1
"""

bot_py_content = """import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def rewrite_with_groq(raw_content: str) -> dict:
    prompt = f\"\"\"
Bạn là chuyên gia SEO Content Writer người Việt Nam.
Hãy viết lại nội dung dưới đây thành một bài viết blog chuẩn SEO hoàn chỉnh, hấp dẫn, giọng văn tự nhiên.

Nội dung gốc:
{raw_content}

Trả về JSON theo đúng định dạng sau:
{{
  "seo_title": "...",
  "meta_description": "...",
  "focus_keyword": "...",
  "content_html": "...",
  "tags": ["tag1", "tag2"],
  "category_suggestion": "..."
}}
\"\"\"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Bạn là trợ lý SEO chuyên nghiệp. Luôn trả về dữ liệu định dạng JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-70b-versatile",
            response_format={"type": "json_object"},
        )
        
        text = chat_completion.choices[0].message.content
        return json.loads(text)

    except Exception as e:
        logger.error(f"Lỗi Groq AI: {e}")
        raise

# Telegram Bot Handler (Example placeholder)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã sẵn sàng với Groq AI!")

if __name__ == '__main__':
    # Add your telegram token here
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    app.run_polling()
"""

# Create a zip file containing the updated files
import zipfile
import os

os.makedirs("fb-wp-bot-groq", exist_ok=True)
with open("fb-wp-bot-groq/requirements.txt", "w") as f:
    f.write(requirements_content)
with open("fb-wp-bot-groq/bot.py", "w") as f:
    f.write(bot_py_content)

with zipfile.ZipFile("fb-wp-bot-groq.zip", "w") as zipf:
    for root, dirs, files in os.walk("fb-wp-bot-groq"):
        for file in files:
            zipf.write(os.path.join(root, file), arcname=file)