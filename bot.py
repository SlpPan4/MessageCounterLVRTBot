import os
from telebot import TeleBot
from dotenv import load_dotenv
import database as db

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = TeleBot(TOKEN, parse_mode="HTML")


# --- Start ---
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Bot is counting messages now")
    db.init_db()

# --- /stats_day ---
@bot.message_handler(commands=["stats_day"])
def stats_today(message):
    stats = db.get_stats_today(message.chat.id)
    if not stats:
        bot.reply_to(message, "Сегодня пока нет сообщений.\n There were no messages today")
        return
    text = "\n".join(f"{user}: {count}" for user, count in stats)
    bot.reply_to(message, f"📊 Сообщения за сегодня/Messages today:\n{text}")

# --- /stats_month ---
@bot.message_handler(commands=["stats_month"])
def stats_month(message):
    stats1 = db.get_stats_month(message.chat.id)
    if not stats1:
        bot.reply_to(message, "No messages were sent this month\nНичего не было отправлено в этом месяце")
        return
    text = "\n".join(f"{user}: {count}" for user, count in stats1)
    bot.reply_to(message, f"📊 Сообщения за месяц/Messages this month:\n{text}")

# --- /stats_week ---
@bot.message_handler(commands=["stats_week"])
def stats_week(message):
    stats1 = db.get_stats_week(message.chat.id)
    if not stats1:
        bot.reply_to(message, "No messages were sent this week\nНичего не было отправлено на этой неделе")
        return
    text = "\n".join(f"{user}: {count}" for user, count in stats1)
    bot.reply_to(message, f"📊 Сообщения за неделю/Messages this week:\n{text}")

# --- /info ---
@bot.message_handler(commands=["info"])
def showing_info(message):
    bot.reply_to(message, "Author/Автор: " + "[SlpPan4](https://github.com/SlpPan4)\n" +
                "Bot was custom-made for my friend\n" + "If you notice some bugs/errors, please contact me on Github", parse_mode ="Markdown")

# --- collect all messages in the group ---
@bot.message_handler(content_types=[
    "text","photo","sticker","animation","video","voice","document","audio","video_note"
])
def count_message(message):
    try:
        # counts only in groups or supergroups
        if message.chat.type not in ("group", "supergroup"):
            return

        # if message is empty - skip
        if not message.from_user:
            return

        # getting the text or the caption of the message
        text = message.text or message.caption or ""

        # not counting if the message is a command
        if text and text.strip().startswith("/"):
            return

        #
        username = message.from_user.username or message.from_user.full_name
        db.add_message(
            user_id=message.from_user.id,
            username=username,
            chat_id=message.chat.id
        )
        print(f"COUNTED: {username} in chat {message.chat.id} type={message.content_type}")
    except Exception as e:
        # log
        print("count_message exception:", e)


print("Bot is running...")
bot.infinity_polling()
