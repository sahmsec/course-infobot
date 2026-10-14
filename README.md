# 🎓 Professional Telegram Course & Admissions Bot

A production-ready Telegram bot built with **Python 3.14+** and **pyTelegramBotAPI (`telebot`)**. Designed for tech institutes, online bootcamps, and digital course academies.

---

## 🌟 Included Features

- **Personalized Start Greeting**: Warm welcome addressed directly to the user's Telegram first name with academy mission and highlights.
- **Interactive Course Catalog**:
  - Full course list presented with clean inline buttons and persistent quick menus.
  - In-place message updates (`edit_message_text`) preventing chat history spam.
- **Modular Sub-Views for Each Course**:
  - 📖 **Course Modules / Detailed Syllabus**: Comprehensive module-by-module breakdown.
  - ⏳ **Duration & Schedule**: Exact weeks, lecture hours, weekly schedule, and replay policies.
  - 💵 **Pricing & Payment Plans**: Upfront rates, monthly installment breakdowns, and discounts.
  - 📝 **Enrollment / Inquiry**: Direct hotline to admissions counselors.
- **Dedicated Subcommands & Quick Commands**:
  - `/start` - Launch bot & main menu
  - `/courses` - View course list
  - `/prices` - Full tuition fee matrix comparison
  - `/contact` - Direct contact details (email, phone, Telegram handle, website)
  - `/about` - About the academy and student outcomes
  - `/stats` - Real-time visitor counts and interaction totals
  - `/export` (or `/csv`) - Instant CSV download sent directly in chat
  - `/help` - Bot command and navigation reference
- **Automatic Visitor Tracking & CSV Export**:
  - Lightweight SQLite database (`bot_users.db`) automatically logs every visitor.
  - Tracks user ID, username, first & last name, first visited date/time, last active date/time, total interactions, and last action.
  - Export anytime via `/export` on Telegram or by running `python export_csv.py` on your computer.
- **Dual Navigation UI**:
  - **Inline Keyboards**: Sleek buttons directly below messages.
  - **Reply Keyboard (Bottom Menu)**: Always accessible quick-action buttons.
- **Robust Error & Windows Handling**:
  - UTF-8 terminal encoding protection.
  - Safe callback error suppression (prevents crashes when users spam buttons).
  - Friendly startup validator guiding you if `BOT_TOKEN` is missing.

---

## 📂 Project Architecture

```
py12/
├── bot.py             # Main bot application, commands, callbacks & tracking
├── database.py        # SQLite storage engine & CSV export logic
├── export_csv.py      # Standalone terminal script to export users.csv
├── courses_data.py    # Centralized course data, curriculum & contact information
├── keyboards.py       # Inline & Reply keyboard markup builders
├── messages.py        # Clean, beautifully formatted HTML message templates
├── run.bat            # 1-click launcher for Windows
├── .env               # Your secret Telegram Bot token (ignored by Git)
├── .env.example       # Example configuration template
├── requirements.txt   # Python package dependencies
└── README.md          # Documentation & roadmap
```

---

## 🚀 Quick Setup & Run

### 1. Get your Telegram Bot Token
1. Open the Telegram app and search for [`@BotFather`](https://t.me/BotFather).
2. Send `/newbot`.
3. Give your bot a **Name** (e.g., `CodeCraft Academy Bot`) and a **Username** ending in `bot` (e.g., `codecraft_academy_bot`).
4. Copy the HTTP API token provided by BotFather.

### 2. Configure Environment
Open the `.env` file in the project folder and paste your token:
```ini
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Activate Virtual Environment & Run
In PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
python bot.py
```

---

## 💡 Recommended Features for Future Expansion

Here are high-value features commonly found in top-tier educational bots:

### 1. In-Bot Lead Capture & Free Consultation Form (FSM)
- Collect student details step-by-step using `bot.register_next_step_handler`:
  1. *Full Name*
  2. *Email Address*
  3. *Phone / WhatsApp Number*
  4. *Selected Course & Background*
- Store incoming leads in **Google Sheets**, **Notion**, or a **PostgreSQL/SQLite** database.

### 2. Downloadable Course Syllabus PDF
- Let users tap **"📥 Download Syllabus PDF"** to receive the official PDF curriculum brochure directly in Telegram via `bot.send_document()`.

### 3. Payment Gateway / Telegram Native Payments
- Accept payments directly via **Telegram Stars**, **Stripe**, **Razorpay**, or local gateways (e.g. SSLCommerz / bKash).
- Instantly issue automated receipt and enrollment confirmation tokens.

### 4. Course Recommendation Quiz ("Which Course Is Right for Me?")
- A 3-question diagnostic quiz:
  - *What is your current background?* (Non-tech / Junior / CS student)
  - *What is your primary goal?* (Web Dev / AI & Data / Cloud)
  - *How much time can you commit weekly?*
- The bot evaluates their answers and automatically recommends the perfect course.

### 5. Promo Code & Discount Engine
- Users type `/promo SUMMER25` or enter a discount code to receive an instant coupon calculation on their course fee.

### 6. Admin Broadcast & Batch Alerts
- Admin command (`/broadcast <message>`) to notify all active prospective students about upcoming batch deadlines, free masterclasses, or discounts.

### 7. Student Reviews & Alumni Testimonials
- Interactive carousel displaying real quotes, student portfolio GitHub links, and company placement outcomes (e.g. "Placed at Google, Meta, local startups").

---

## 🛠️ Customizing the Bot

All course data and contact information are separated into [courses_data.py](file:///d:/Projects/py12/courses_data.py).
To add, edit, or remove courses, simply update the `COURSES` dictionary in that file without having to touch any bot logic!

