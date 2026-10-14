"""
database.py - SQLite storage for tracking bot visitors and exporting to CSV.
"""

import sqlite3
import csv
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "bot_users.db")


def get_connection():
    """Returns a SQLite connection with dict-like row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Table 1: Unique users summary
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                first_seen TEXT,
                last_active TEXT,
                interaction_count INTEGER DEFAULT 1,
                last_action TEXT
            )
            """
        )
        # Table 2: Detailed audit log of every query, command, and button click
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                full_name TEXT,
                query_type TEXT,
                query_text TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()

        # Seed existing user actions into user_queries if table is new
        cursor.execute("SELECT COUNT(*) FROM user_queries")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO user_queries (user_id, username, full_name, query_type, query_text, created_at)
                SELECT 
                    user_id, 
                    username, 
                    TRIM(first_name || ' ' || last_name), 
                    CASE WHEN last_action LIKE '/%' THEN 'command' ELSE 'button' END, 
                    last_action, 
                    last_active 
                FROM users
                """
            )
            conn.commit()


def log_user_visit(user, action: str = "interaction", query_type: str = "button"):
    """
    Records or updates user profile AND appends an entry to user_queries audit log.
    - user: telebot User object
    - action: descriptive label of the query/action
    - query_type: 'command', 'button', 'question', or 'message'
    """
    if not user:
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = f"@{user.username}" if user.username else "N/A"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip() or "Anonymous User"

    with get_connection() as conn:
        cursor = conn.cursor()
        # 1. Upsert users summary
        cursor.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name, first_seen, last_active, interaction_count, last_action)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                last_active = excluded.last_active,
                interaction_count = users.interaction_count + 1,
                last_action = excluded.last_action
            """,
            (user.id, username, first_name, last_name, now_str, now_str, action)
        )
        # 2. Insert into user_queries audit log
        cursor.execute(
            """
            INSERT INTO user_queries (user_id, username, full_name, query_type, query_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user.id, username, full_name, query_type, action, now_str)
        )
        conn.commit()


def get_all_queries(limit: int = 200, query_type: str = None, search: str = None) -> list:
    """Retrieves structured query history for the UI dashboard."""
    query = "SELECT * FROM user_queries WHERE 1=1"
    params = []

    if query_type and query_type != "all":
        query += " AND query_type = ?"
        params.append(query_type)

    if search:
        search_pattern = f"%{search}%"
        query += " AND (full_name LIKE ? OR username LIKE ? OR query_text LIKE ? OR CAST(user_id AS TEXT) LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_all_users() -> list:
    """Returns all unique visitors ordered by last active time."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY last_active DESC")
        return [dict(row) for row in cursor.fetchall()]


def get_analytics_summary() -> dict:
    """Returns analytics metrics for dashboard cards."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total_users, SUM(interaction_count) AS total_interactions FROM users")
        row = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS total_queries FROM user_queries")
        q_row = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS custom_questions FROM user_queries WHERE query_type = 'question'")
        quest_row = cursor.fetchone()

        return {
            "total_users": row["total_users"] if row and row["total_users"] else 0,
            "total_interactions": row["total_interactions"] if row and row["total_interactions"] else 0,
            "total_queries": q_row["total_queries"] if q_row and q_row["total_queries"] else 0,
            "custom_questions": quest_row["custom_questions"] if quest_row and quest_row["custom_questions"] else 0,
        }



def export_users_to_csv(csv_path: str = "users_export.csv") -> tuple[int, str]:
    """
    Exports all visitor records to a CSV file.
    Returns (total_rows_exported, absolute_file_path).
    """
    abs_path = os.path.abspath(csv_path)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                user_id,
                username,
                first_name,
                last_name,
                first_seen,
                last_active,
                interaction_count,
                last_action
            FROM users
            ORDER BY last_active DESC
            """
        )
        rows = cursor.fetchall()

    with open(abs_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "User ID",
            "Username",
            "First Name",
            "Last Name",
            "First Visited (Local Time)",
            "Last Active (Local Time)",
            "Total Interactions",
            "Last Action Performed"
        ])
        for row in rows:
            writer.writerow([
                row["user_id"],
                row["username"],
                row["first_name"],
                row["last_name"],
                row["first_seen"],
                row["last_active"],
                row["interaction_count"],
                row["last_action"]
            ])

    return len(rows), abs_path

