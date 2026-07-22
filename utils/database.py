import aiosqlite
import config

DB_PATH = config.DATABASE


async def setup_database():
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings(
            user_id INTEGER PRIMARY KEY,
            warnings INTEGER NOT NULL DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS tracked_users(
            user_id INTEGER PRIMARY KEY
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS protected_roles(
            role_id INTEGER PRIMARY KEY
        )
        """)

        await db.commit()


# ------------------------
# Warning Functions
# ------------------------

async def get_warning(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT warnings FROM warnings WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0


async def add_warning(user_id: int):
    current = await get_warning(user_id)
    current += 1

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT OR REPLACE INTO warnings(user_id,warnings)
        VALUES (?,?)
        """, (user_id, current))

        await db.commit()

    return current


async def reset_warning(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM warnings WHERE user_id=?",
            (user_id,)
        )
        await db.commit()


async def reset_all():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM warnings")
        await db.commit()


# ------------------------
# Tracked Users
# ------------------------

async def add_tracked(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO tracked_users VALUES(?)",
            (user_id,)
        )
        await db.commit()


async def remove_tracked(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM tracked_users WHERE user_id=?",
            (user_id,)
        )
        await db.commit()


async def is_tracked(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM tracked_users WHERE user_id=?",
            (user_id,)
        )

        return await cursor.fetchone() is not None


# ------------------------
# Protected Roles
# ------------------------

async def add_role(role_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO protected_roles VALUES(?)",
            (role_id,)
        )
        await db.commit()


async def remove_role(role_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM protected_roles WHERE role_id=?",
            (role_id,)
        )
        await db.commit()


async def get_roles():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT role_id FROM protected_roles"
        )

        rows = await cursor.fetchall()

        return [x[0] for x in rows]
