import json
import logging
import requests
import aiohttp
import asyncio
import logging
logging.basicConfig(filename='logs/api_requests.log', level=logging.NOTSET, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def request(base_url, access_token=None, endpoint=None, query=None):
    """
    Performs GET request with given params.
    :param base_url:
    :param access_token:
    :param endpoint:
    :param query:
    :return:
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        r = requests.get(f"{base_url}{endpoint}{'/'+ query if query else ''}", headers=headers if headers else None)
        return r.json()
    except Exception as e:
        return {"error": e}

