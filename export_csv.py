"""
export_csv.py - Standalone command-line script to export user visitors to CSV.
Run anytime with: python export_csv.py
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from database import init_db, get_analytics_summary, export_users_to_csv

def main():
    init_db()
    stats = get_analytics_summary()
    total_users = stats["total_users"]
    total_interactions = stats["total_interactions"]

    print("=" * 55)
    print("📊 Py12 Course Bot - Visitor Analytics")
    print("=" * 55)
    print(f"👥 Total Unique Users:       {total_users}")
    print(f"⚡ Total User Interactions:  {total_interactions}")
    print("-" * 55)

    if total_users == 0:
        print("ℹ️ No visitors have interacted with the bot yet.")
        print("Start the bot with 'python bot.py' and send /start on Telegram!")
        print("=" * 55)
        return

    count, path = export_users_to_csv("users.csv")
    print(f"✅ Successfully exported {count} user records to:")
    print(f"📁 {path}")
    print("=" * 55)

if __name__ == "__main__":
    main()

