"""
Singleton for httpx stuff
"""
import httpx, json, asyncio

from ..globals import return_client, return_b_token


    url = BASE_URL+url_add

    if n_headers == None:
        headers={
            "Authorization": f"Bearer {return_b_token()}",
            "Content-Type": "application/json; charset=utf-8"
        }
    else:
        headers=n_headers
    data = n_data

    client = return_client()
    resp = await client.post(
            url,
            json=data,
            headers=headers
    )
    
    return resp.json()
