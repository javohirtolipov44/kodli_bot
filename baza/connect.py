import aiosqlite

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA synchronous=NORMAL;")
        await db.execute("PRAGMA busy_timeout = 30000;")
