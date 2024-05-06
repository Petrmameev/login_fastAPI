import os
import sqlite3
from datetime import datetime, timezone

import bcrypt

from config import *


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def add_user(cur, username, salary, date_next_raise_salary, password):
    try:
        cur.execute(
            """
        INSERT INTO users (username, hashed_password, salary, date_next_raise_salary) VALUES (?, ?, ?, ?)
        """,
            (username, hash_password(password), salary, date_next_raise_salary),
        )
    except sqlite3.IntegrityError:
        print(f"Error: Cannot add user '{username}'. Username already exists.")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if os.path.exists(DATABASE_FILENAME):
        try:
            os.remove(DATABASE_FILENAME)
        except OSError as e:
            print(f"Error: {e.strerror}. Could not delete {DATABASE_FILENAME}.")
            return
    try:
        conn = sqlite3.connect("users.db")
    except sqlite3.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               hashed_password TEXT NOT NULL,
               salary REAL NOT NULL,
               date_next_raise_salary TEXT NOT NULL
           )"""
        )
    except sqlite3.DatabaseError as e:
        print(f"Error creating table: {e}")
        conn.close()
        return

    add_user(
        cur,
        "petr",
        60000.0,
        datetime(2026, 9, 1, tzinfo=timezone.utc).isoformat(),
        "mameev",
    )
    add_user(
        cur,
        "anatoly",
        100000.0,
        datetime(2025, 1, 1, tzinfo=timezone.utc).isoformat(),
        "12345",
    )
    try:
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error committing changes: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
