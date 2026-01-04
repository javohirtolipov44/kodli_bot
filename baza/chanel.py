import aiosqlite
from baza.connect import DB_NAME

# Jadval yaratish
async def create_chanels_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chanel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chanel_id TEXT,
                title TEXT
            )
        """)
        await db.commit()


# Kanal olish
async def get_chanel(chanel_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM chanel WHERE chanel_id = ?",
            (chanel_id,)
        )
        return await cursor.fetchone()


# Kanal qo‘shish
async def add_chanel(chanel_id, title):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO chanel (chanel_id, title) VALUES (?, ?)",
            (chanel_id, title)
        )
        await db.commit()

# Kanalni o'chirish
async def del_chanel(chanel_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "DELETE FROM chanel WHERE chanel_id = ?",
            (chanel_id,)
        )
        await db.commit()
        return cursor.rowcount > 0

# Barcha kanallarni olish
async def get_all_chanels():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM chanel") as cursor:
            return await cursor.fetchall()