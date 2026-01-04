import aiosqlite
from baza.connect import DB_NAME



# Jadval yaratish
async def create_homiy_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS homiy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chanel_id TEXT,
                link TEXT
            )
        """)
        await db.commit()


# Barcha homiy kanallarni olish
async def get_all_homiy():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM homiy") as cursor:
            return await cursor.fetchall()

# Homiy kanal qo‘shish
async def add_homiy(chanel_id, link):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO homiy (chanel_id, link) VALUES (?, ?)",
            (chanel_id, link)
        )
        await db.commit()

# homiy kanalni o'chirish
async def del_homiy(chanel_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "DELETE FROM homiy WHERE chanel_id = ?",
            (chanel_id,)
        )
        await db.commit()
        return cursor.rowcount > 0
