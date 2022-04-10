import aiohttp
import random
import string
import time
import json
import re

from SAGIRIBOT.basics.get_config import get_config
from SAGIRIBOT.basics.aio_mysql_excute import execute_sql
from SAGIRIBOT.basics.tools import get_tx_sign


async def get_chat_session(group_id: int, sender: int) -> str:
    sql = "select `session` from chatSession where groupId=%d and memberId=%d" % (group_id, sender)
    data = await execute_sql(sql)
    print(data)
    data = data[0]
    if data is not None:
        session = data[0]
        print("智能闲聊 sender:%s,session:%s" % (sender, session))
        return str(session)
    else:
        sql = "select MAX(`session`) from chatSession"
        data = await execute_sql(sql)
        data = data[0]
        print(data)
        if data is None:
            session = 1
        else:
            session = int(data) + 1
        sql = "INSERT INTO chatSession (groupId,memberId,`session`) VALUES (%d,%d,%d)" % (group_id, sender, session)
        await execute_sql(sql)
        print("智能闲聊 sender:%s,session:%s" % (sender, session))
        return str(session)


async def get_chat_reply(group_id: int, sender: int, text: str):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    temp_list = re.findall("@.* ", text, re.S)
    if temp_list is not None:
        text = text.replace(temp_list[0], "")

    app_id = await get_config("txAppId")
    t = time.time()
    time_stamp = str(int(t))
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))

    params = {
        'app_id': app_id,
        'question': text,
        'time_stamp': time_stamp,
        'nonce_str': nonce_str,
        'session': await get_chat_session(group_id, sender)
    }
    sign = await get_tx_sign(params)
    params["sign"] = sign

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            res = await resp.json()
    return res["data"]["answer"]
