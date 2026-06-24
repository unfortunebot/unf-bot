
import aiosqlite

async def setup():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS players(
            id INTEGER PRIMARY KEY,
            name TEXT,
            ekip TEXT,
            discord_id TEXT
        )
        """)
        await db.commit()

async def add_player(pid,name,ekip,discord_id):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute(
        "INSERT OR REPLACE INTO players VALUES(?,?,?,?)",
        (pid,name,ekip,discord_id))
        await db.commit()

async def get_team(ekip):
    async with aiosqlite.connect("bot.db") as db:
        cur = await db.execute(
        "SELECT * FROM players WHERE ekip=?",(ekip,))
        return await cur.fetchall()

async def get_player(pid):
    async with aiosqlite.connect("bot.db") as db:
        cur = await db.execute(
        "SELECT * FROM players WHERE id=?",(pid,))
        return await cur.fetchone()
