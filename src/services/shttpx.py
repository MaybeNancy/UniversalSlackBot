"""
Singleton for httpx stuff
"""
import httpx, asyncio

from ..globals import return_client

async def spost(url,headers,data):
    client = return_client()
    return await client.post(
            url,
            json=data,
            headers=headers
    )
