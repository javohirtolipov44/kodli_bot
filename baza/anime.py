import aiosqlite
from baza.connect import DB_NAME

async def get_anime_by_hesh(hesh: str):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT k_id, message_id FROM anime WHERE hesh = ?",
            (hesh,)
        )
        return await cursor.fetchone()

async def add_anime(chanel_id, m_id, title, hesh):
    qism = 0
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO anime (k_id, message_id, hashtag, qism, hesh) VALUES (?, ?, ?, ?, ?)",
            (chanel_id, m_id, title, qism, hesh)
        )
        await db.commit()