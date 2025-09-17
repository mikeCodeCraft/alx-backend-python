import asyncio
import aiosqlite
from datetime import datetime

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Fetched {len(rows)} users")
            return rows
        
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            rows = await cursor.fetchall()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Fetched {len(rows)} older users")
            return rows
        
async def fetch_concurrently():
    # Run both fetch operations concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# -------- Run the concurrent fetch --------
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())