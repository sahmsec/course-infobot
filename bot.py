"""
bot.py - Professional Telegram Bot for Course Catalog, Modules, Duration, and Pricing.
Built with pyTelegramBotAPI (telebot).
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Ensure safe UTF-8 terminal output on Windows
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import telebot
from telebot import apihelper
from telebot.types import BotCommand, CallbackQuery, Message
from telebot.apihelper import ApiTelegramException
from datetime import datetime

from courses_data import COURSES
import keyboards
import messages
import database
import dashboard

# Configure logging
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("CourseBot")

# Initialize database
database.init_db()

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
    logger.error("❌ BOT_TOKEN is not set in .env! Please add your token from @BotFather to .env file.")
    print("\n" + "=" * 65)
    print("🚨 CONFIGURATION NEEDED: TELEGRAM BOT TOKEN")
    print("=" * 65)
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot and follow instructions to get your API Token")
    print("3. Open the '.env' file in this project directory")
    print("4. Paste your token: BOT_TOKEN=your_token_here")
    print("5. Run this bot again with: python bot.py")
    print("=" * 65 + "\n")
    sys.exit(1)

# Enable middleware before TeleBot initialization
apihelper.ENABLE_MIDDLEWARE = True

# Initialize bot instance with HTML default parse mode
bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode="HTML")


@bot.middleware_handler(update_types=["message"])
def track_message_visitor(bot_instance, message: Message):
    """Automatically records every visitor message/command with category."""
    if message and message.from_user:
        text = message.text or "[Media/Non-text]"
        if text.startswith("/"):
            q_type = "command"
        elif text in ["📚 Browse Courses", "💰 Pricing Overview", "📞 Contact Support", "❓ Help & FAQ"]:
            q_type = "menu"
        else:
            q_type = "question"
        database.log_user_visit(message.from_user, action=text, query_type=q_type)


@bot.middleware_handler(update_types=["callback_query"])
def track_callback_visitor(bot_instance, call: CallbackQuery):
    """Automatically records every button click."""
    if call and call.from_user:
        database.log_user_visit(call.from_user, action=f"button:{call.data}", query_type="button")


def setup_bot_commands():
    """Sets up the Telegram command menu in the bottom-left corner of the chat."""
    try:
        commands = [
            BotCommand("start", "Welcome message & main menu"),
            BotCommand("courses", "Browse available courses"),
            BotCommand("prices", "Check tuition fees & plans"),
            BotCommand("contact", "Contact admissions counselor"),
            BotCommand("about", "Learn about our academy"),
            BotCommand("stats", "View visitor counts"),
            BotCommand("export", "Download visitor list as CSV"),
            BotCommand("help", "Help & navigation guide"),
        ]
        bot.set_my_commands(commands)
        logger.info("Bot commands successfully registered with Telegram.")
    except Exception as e:
        logger.warning(f"Could not register bot commands: {e}")


# ==========================================================
# COMMAND HANDLERS (/start, /courses, /prices, etc.)
# ==========================================================

@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    """Greeting message on /start with persistent menu and interactive buttons."""
    user_name = message.from_user.first_name if message.from_user else "there"
    welcome_text = messages.get_welcome_message(user_name)
    
    # Send welcome text with inline buttons and persistent keyboard
    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        reply_markup=keyboards.get_main_inline_keyboard()
    )
    # Also attach the persistent reply keyboard for quick access
    bot.send_message(
        chat_id=message.chat.id,
        text="👇 <i>Use the inline buttons above or the quick menu below:</i>",
        reply_markup=keyboards.get_persistent_reply_keyboard()
    )


@bot.message_handler(commands=["courses"])
def handle_courses(message: Message):
    """Displays course catalog."""
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.get_courses_overview_message(),
        reply_markup=keyboards.get_courses_keyboard()
    )


@bot.message_handler(commands=["prices"])
def handle_prices(message: Message):
    """Displays pricing comparison overview."""
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.get_pricing_overview_message(),
        reply_markup=keyboards.get_courses_keyboard()
    )


@bot.message_handler(commands=["contact"])
def handle_contact(message: Message):
    """Displays contact details and admissions support."""
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.get_contact_message(),
        reply_markup=keyboards.get_contact_keyboard()
    )


@bot.message_handler(commands=["about"])
def handle_about(message: Message):
    """Displays about information."""
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.get_about_message(),
        reply_markup=keyboards.get_contact_keyboard()
    )


@bot.message_handler(commands=["help"])
def handle_help(message: Message):
    """Displays help information."""
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.get_help_message(),
        reply_markup=keyboards.get_main_inline_keyboard()
    )


@bot.message_handler(commands=["stats"])
def handle_stats(message: Message):
    """Displays real-time visitor count and interaction metrics."""
    stats = database.get_analytics_summary()
    text = (
        "📊 <b>Bot Visitor Analytics</b>\n\n"
        f"👥 <b>Total Unique Visitors:</b> <code>{stats['total_users']}</code>\n"
        f"⚡ <b>Total User Interactions:</b> <code>{stats['total_interactions']}</code>\n\n"
        "💡 <i>Tip: Send /export to receive the complete user list as a CSV file.</i>"
    )
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(commands=["export", "csv"])
def handle_export_csv(message: Message):
    """Exports all visitors to a CSV file and uploads it to the Telegram chat."""
    stats = database.get_analytics_summary()
    if stats["total_users"] == 0:
        bot.send_message(
            chat_id=message.chat.id,
            text="ℹ️ <i>No visitor records yet. Once users send a message or click buttons, they will be tracked.</i>"
        )
        return

    count, file_path = database.export_users_to_csv("users.csv")
    try:
        with open(file_path, "rb") as f:
            bot.send_document(
                chat_id=message.chat.id,
                document=f,
                caption=(
                    f"📊 <b>Visitor Report ({count} unique users)</b>\n"
                    f"Generated at: <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"
                )
            )
    except Exception as e:
        logger.error(f"Error sending CSV file: {e}")
        bot.send_message(chat_id=message.chat.id, text=f"⚠️ Failed to send CSV file: {e}")



# ==========================================================
# PERSISTENT REPLY KEYBOARD TEXT HANDLERS
# ==========================================================

@bot.message_handler(func=lambda msg: msg.text == "📚 Browse Courses")
def reply_browse_courses(message: Message):
    handle_courses(message)


@bot.message_handler(func=lambda msg: msg.text == "💰 Pricing Overview")
def reply_pricing(message: Message):
    handle_prices(message)


@bot.message_handler(func=lambda msg: msg.text == "📞 Contact Support")
def reply_contact(message: Message):
    handle_contact(message)


@bot.message_handler(func=lambda msg: msg.text == "❓ Help & FAQ")
def reply_help(message: Message):
    handle_help(message)


@bot.message_handler(func=lambda msg: True, content_types=["text"])
def handle_custom_inquiry(message: Message):
    """Handles any free-text query or question sent by a user."""
    from html import escape
    first_name = message.from_user.first_name if message.from_user else "there"
    text = (
        f"📩 <b>Thank you for your message, {escape(first_name)}!</b>\n\n"
        f"We've logged your query:\n"
        f"<i>\"{escape(message.text)}\"</i>\n\n"
        f"An admissions counselor will review this shortly. In the meantime, you can explore our course details or chat with our team directly:"
    )
    bot.reply_to(message, text, reply_markup=keyboards.get_contact_keyboard())


# ==========================================================
# INLINE KEYBOARD CALLBACK QUERY HANDLERS
# ==========================================================

def safe_edit_message(call: CallbackQuery, text: str, reply_markup):
    """Safely edits message in-place and ignores 'message is not modified' error."""
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=reply_markup
        )
    except ApiTelegramException as e:
        if "message is not modified" not in str(e).lower():
            logger.error(f"Error editing message: {e}")


@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call: CallbackQuery):
    """Central router for all inline button clicks."""
    # Immediately acknowledge callback to stop user's loading spinner
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    data = call.data

    # Main menu navigation
    if data == "main_menu":
        user_name = call.from_user.first_name if call.from_user else "there"
        safe_edit_message(
            call,
            messages.get_welcome_message(user_name),
            keyboards.get_main_inline_keyboard()
        )
        return

    # Courses List
    if data == "view_courses":
        safe_edit_message(
            call,
            messages.get_courses_overview_message(),
            keyboards.get_courses_keyboard()
        )
        return

    # Pricing Overview
    if data == "view_pricing_overview":
        safe_edit_message(
            call,
            messages.get_pricing_overview_message(),
            keyboards.get_courses_keyboard()
        )
        return

    # Contact Admissions
    if data == "view_contact":
        safe_edit_message(
            call,
            messages.get_contact_message(),
            keyboards.get_contact_keyboard()
        )
        return

    # About Academy
    if data == "view_about":
        safe_edit_message(
            call,
            messages.get_about_message(),
            keyboards.get_contact_keyboard()
        )
        return

    # Specific Course Overview
    if data.startswith("course_"):
        course_id = data.replace("course_", "")
        course = COURSES.get(course_id)
        if not course:
            bot.answer_callback_query(call.id, text="⚠️ Course not found.", show_alert=True)
            return

        safe_edit_message(
            call,
            messages.get_course_detail_message(course),
            keyboards.get_course_detail_keyboard(course_id)
        )
        return

    # Course Modules / Syllabus
    if data.startswith("modules_"):
        course_id = data.replace("modules_", "")
        course = COURSES.get(course_id)
        if not course:
            return

        safe_edit_message(
            call,
            messages.get_course_modules_message(course),
            keyboards.get_course_subview_keyboard(course_id, current_view="modules")
        )
        return

    # Course Duration & Schedule
    if data.startswith("duration_"):
        course_id = data.replace("duration_", "")
        course = COURSES.get(course_id)
        if not course:
            return

        safe_edit_message(
            call,
            messages.get_course_duration_message(course),
            keyboards.get_course_subview_keyboard(course_id, current_view="duration")
        )
        return

    # Course Price & Installments
    if data.startswith("price_"):
        course_id = data.replace("price_", "")
        course = COURSES.get(course_id)
        if not course:
            return

        safe_edit_message(
            call,
            messages.get_course_price_message(course),
            keyboards.get_course_subview_keyboard(course_id, current_view="price")
        )
        return

    # Course Enrollment / Register Interest
    if data.startswith("enroll_"):
        course_id = data.replace("enroll_", "")
        course = COURSES.get(course_id)
        if not course:
            return

        safe_edit_message(
            call,
            messages.get_course_enroll_message(course),
            keyboards.get_enroll_keyboard(course_id)
        )
        return


# ==========================================================
# BOT ENTRYPOINT
# ==========================================================

def main():
    logger.info("Initializing bot commands...")
    setup_bot_commands()
    
    # Automatically start Web Dashboard UI in the background
    dashboard.start_dashboard_in_background(port=5000)
    
    logger.info("🚀 Course Bot is online and listening for messages...")
    
    # Start polling
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
