"""
messages.py - Professional HTML formatted response templates for the bot.
"""

from html import escape
from courses_data import COURSES, CONTACT_INFO


def get_welcome_message(first_name: str) -> str:
    safe_name = escape(first_name) if first_name else "there"
    return (
        f"👋 <b>Welcome, {safe_name}!</b>\n\n"
        f"Welcome to <b>{escape(CONTACT_INFO['organization'])}</b> — where future tech leaders build "
        f"in-demand software engineering, AI, and cloud skills.\n\n"
        f"⚡ <b>What would you like to explore today?</b>\n"
        f"• <b>Browse our live bootcamps & syllabi</b>\n"
        f"• <b>Inspect course durations & schedules</b>\n"
        f"• <b>Review tuition fees & payment plans</b>\n"
        f"• <b>Get in touch with an admissions counselor</b>\n\n"
        f"<i>Select an option below or use the quick navigation menu to get started:</i>"
    )


def get_about_message() -> str:
    return (
        f"🏢 <b>About {escape(CONTACT_INFO['organization'])}</b>\n\n"
        f"We are an elite practical tech training institute dedicated to helping beginners "
        f"and career switchers land high-paying roles in tech.\n\n"
        f"🌟 <b>Why Learn With Us?</b>\n"
        f"✅ <b>Live Interactive Classes</b> with seasoned industry engineers\n"
        f"✅ <b>Real-world Production Projects</b> for your portfolio\n"
        f"✅ <b>1-on-1 Mentorship</b> and dedicated code reviews\n"
        f"✅ <b>Career Guidance:</b> CV reviews, mock technical interviews & referrals\n\n"
        f"🌐 <b>Website:</b> <a href=\"{CONTACT_INFO['website']}\">{CONTACT_INFO['website']}</a>\n"
        f"📍 <b>Headquarters:</b> {escape(CONTACT_INFO['address'])}"
    )


def get_courses_overview_message() -> str:
    return (
        "📚 <b>Our Featured Training Programs</b>\n\n"
        "Click on any course below to view its <b>complete syllabus</b>, "
        "<b>duration/schedule</b>, and <b>tuition fees</b>:\n"
    )


def get_course_detail_message(course: dict) -> str:
    return (
        f"🎓 <b>{escape(course['title'])}</b>\n"
        f"<i>{escape(course.get('badge', ''))}</i>\n\n"
        f"📊 <b>Level:</b> {escape(course['level'])}\n"
        f"⏳ <b>Duration:</b> {escape(course['duration'])}\n"
        f"💵 <b>Tuition:</b> {escape(course['pricing']['discounted'])} <s>{escape(course['pricing']['regular'])}</s>\n\n"
        f"📝 <b>Overview:</b>\n{escape(course['overview'])}\n\n"
        f"🎯 <b>Prerequisites:</b> {escape(course['prerequisites'])}\n"
        f"🏆 <b>Certification:</b> {escape(course['certification'])}\n\n"
        f"👇 <i>Explore specific details using the buttons below:</i>"
    )


def get_course_modules_message(course: dict) -> str:
    modules_text = "\n".join([f"• <b>{escape(m)}</b>" for m in course["modules"]])
    return (
        f"📖 <b>Curriculum & Modules</b>\n"
        f"Course: <b>{escape(course['title'])}</b>\n\n"
        f"{modules_text}\n\n"
        f"💡 <i>Each module includes live coding sessions, assignments, and guided project work.</i>"
    )


def get_course_duration_message(course: dict) -> str:
    return (
        f"⏳ <b>Duration & Schedule</b>\n"
        f"Course: <b>{escape(course['title'])}</b>\n\n"
        f"📅 <b>Total Duration:</b> {escape(course['duration'])}\n"
        f"🕒 <b>Class Schedule:</b> {escape(course['schedule'])}\n"
        f"🎥 <b>Format:</b> Live via Zoom with instant cloud recordings provided\n"
        f"👥 <b>Mentorship:</b> 24/7 Discord community support + weekly office hours"
    )


def get_course_price_message(course: dict) -> str:
    p = course["pricing"]
    return (
        f"💵 <b>Tuition & Payment Plans</b>\n"
        f"Course: <b>{escape(course['title'])}</b>\n\n"
        f"🏷️ <b>One-time Payment:</b> <b>{escape(p['discounted'])}</b> (Regular: <s>{escape(p['regular'])}</s>)\n"
        f"💳 <b>Flexible Installments:</b> {escape(p['installments'])}\n"
        f"🎁 <b>Special Offer:</b> {escape(p.get('offer', 'Standard rate'))}\n\n"
        f"🛡️ <i>Includes 7-day money-back guarantee if you are not 100% satisfied.</i>"
    )


def get_course_enroll_message(course: dict) -> str:
    return (
        f"📝 <b>Enrollment & Consultation</b>\n"
        f"Course: <b>{escape(course['title'])}</b>\n\n"
        f"Seats are strictly limited to <b>25 students per cohort</b> to guarantee personalized mentorship.\n\n"
        f"📌 <b>Next Steps:</b>\n"
        f"1. Click the button below to message our Admissions Counselor directly on Telegram.\n"
        f"2. Or call us at <code>{escape(CONTACT_INFO['phone'])}</code>.\n"
        f"3. You'll receive course access details and pre-course preparation material."
    )


def get_pricing_overview_message() -> str:
    lines = ["💰 <b>Course Pricing Summary</b>\n"]
    for c in COURSES.values():
        lines.append(
            f"• <b>{escape(c['title'])}</b>\n"
            f"   Price: <b>{escape(c['pricing']['discounted'])}</b> (<s>{escape(c['pricing']['regular'])}</s>)\n"
            f"   Duration: {escape(c['duration'])}\n"
            f"   Plan: {escape(c['pricing']['installments'])}\n"
        )
    lines.append("<i>All enrollments include access to recorded sessions, learning portal, and verified certificate.</i>")
    return "\n".join(lines)


def get_contact_message() -> str:
    return (
        f"📞 <b>Contact {escape(CONTACT_INFO['organization'])} Admissions</b>\n\n"
        f"Have questions about prerequisites, schedules, or scholarships? Our admissions team is here to help!\n\n"
        f"💬 <b>Telegram Support:</b> {escape(CONTACT_INFO['telegram_support'])}\n"
        f"📧 <b>Email:</b> <code>{escape(CONTACT_INFO['email'])}</code>\n"
        f"📞 <b>Phone / WhatsApp:</b> <code>{escape(CONTACT_INFO['phone'])}</code>\n"
        f"🕒 <b>Admissions Hours:</b> {escape(CONTACT_INFO['hours'])}\n"
        f"📍 <b>Location:</b> {escape(CONTACT_INFO['address'])}\n\n"
        f"<i>Tap below to start a chat with our counselor or visit the official site.</i>"
    )


def get_help_message() -> str:
    return (
        "❓ <b>Bot Help & Command Navigation</b>\n\n"
        "You can easily navigate using the buttons on your screen, or use these commands anytime:\n\n"
        "🔹 /start - Restart bot and return to main menu\n"
        "🔹 /courses - Browse all courses and curriculums\n"
        "🔹 /prices - View all tuition rates and installment options\n"
        "🔹 /contact - Speak with our admissions counselors\n"
        "🔹 /about - Learn more about our academy\n"
        "🔹 /help - Display this help guide\n\n"
        "💡 <i>Tip: You can also tap any of the buttons below each message for instant answers without typing!</i>"
    )

