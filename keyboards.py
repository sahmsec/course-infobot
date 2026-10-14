"""
keyboards.py - Inline and Reply keyboard builders for Telegram Bot.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from courses_data import COURSES, CONTACT_INFO


def get_persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    """Bottom persistent menu for quick navigation."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton("📚 Browse Courses"), KeyboardButton("💰 Pricing Overview"))
    markup.row(KeyboardButton("📞 Contact Support"), KeyboardButton("❓ Help & FAQ"))
    return markup


def get_main_inline_keyboard() -> InlineKeyboardMarkup:
    """Main menu inline keyboard displayed on /start."""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📚 Browse Courses", callback_data="view_courses"),
        InlineKeyboardButton("💰 Pricing Overview", callback_data="view_pricing_overview"),
    )
    markup.add(
        InlineKeyboardButton("📞 Contact Admissions", callback_data="view_contact"),
        InlineKeyboardButton("ℹ️ About Academy", callback_data="view_about"),
    )
    return markup


def get_courses_keyboard() -> InlineKeyboardMarkup:
    """Generates buttons for each available course."""
    markup = InlineKeyboardMarkup(row_width=1)
    
    course_icons = {
        "python_fullstack": "🐍",
        "data_science_ai": "📊",
        "frontend_react": "⚛️",
        "devops_cloud": "☁️",
    }
    
    for course_id, data in COURSES.items():
        icon = course_icons.get(course_id, "🎓")
        btn_text = f"{icon} {data['title']}"
        markup.add(InlineKeyboardButton(btn_text, callback_data=f"course_{course_id}"))
    
    markup.add(InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu"))
    return markup


def get_course_detail_keyboard(course_id: str) -> InlineKeyboardMarkup:
    """Menu inside a specific course with sub-options (modules, duration, price, enroll)."""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📖 Modules & Syllabus", callback_data=f"modules_{course_id}"),
        InlineKeyboardButton("⏳ Duration & Schedule", callback_data=f"duration_{course_id}"),
    )
    markup.add(
        InlineKeyboardButton("💵 Fees & Installments", callback_data=f"price_{course_id}"),
        InlineKeyboardButton("📝 Register Interest", callback_data=f"enroll_{course_id}"),
    )
    markup.add(InlineKeyboardButton("⬅️ Back to Courses List", callback_data="view_courses"))
    return markup


def get_course_subview_keyboard(course_id: str, current_view: str) -> InlineKeyboardMarkup:
    """
    Sub-view keyboard allowing quick switching between modules, duration, and price,
    plus going back to the course overview.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    
    if current_view != "modules":
        buttons.append(InlineKeyboardButton("📖 Modules", callback_data=f"modules_{course_id}"))
    if current_view != "duration":
        buttons.append(InlineKeyboardButton("⏳ Duration", callback_data=f"duration_{course_id}"))
    if current_view != "price":
        buttons.append(InlineKeyboardButton("💵 Fees", callback_data=f"price_{course_id}"))
        
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton("📝 Register Interest", callback_data=f"enroll_{course_id}"),
        InlineKeyboardButton("↩️ Course Overview", callback_data=f"course_{course_id}"),
    )
    markup.add(InlineKeyboardButton("⬅️ Back to All Courses", callback_data="view_courses"))
    return markup


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """Buttons displayed under contact information."""
    markup = InlineKeyboardMarkup(row_width=2)
    clean_username = CONTACT_INFO["telegram_support"].lstrip("@")
    markup.add(
        InlineKeyboardButton("💬 Chat on Telegram", url=f"https://t.me/{clean_username}"),
        InlineKeyboardButton("🌐 Visit Website", url=CONTACT_INFO["website"]),
    )
    markup.add(InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu"))
    return markup


def get_enroll_keyboard(course_id: str) -> InlineKeyboardMarkup:
    """Enrollment / registration buttons."""
    markup = InlineKeyboardMarkup(row_width=1)
    clean_username = CONTACT_INFO["telegram_support"].lstrip("@")
    markup.add(
        InlineKeyboardButton("💬 Speak with Counselor", url=f"https://t.me/{clean_username}"),
        InlineKeyboardButton("↩️ Back to Course", callback_data=f"course_{course_id}"),
        InlineKeyboardButton("⬅️ All Courses", callback_data="view_courses"),
    )
    return markup

