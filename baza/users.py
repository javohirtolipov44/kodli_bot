import aiosqlite
from baza.connect import DB_NAME

# Jadval yaratish
async def create_users_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE
            )
        """)
        await db.commit()


# User olish
async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()


# User qo‘shish (LOCK-SAFE)
async def add_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        await db.commit()

# 🔹 Jami userlar sonini olish
async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        result = await cursor.fetchone()
        return result[0] if result else 0