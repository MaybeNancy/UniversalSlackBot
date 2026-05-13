"""
Singleton for httpx stuff
"""
import httpx, asyncio

from ..globals import return_client, return_b_token

async def post(url,headers,data):
    client = return_client()
    return await client.post(
            url,
            json=data,
            headers=headers
    )
