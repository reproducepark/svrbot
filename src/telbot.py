import logging, os
import asyncio, telegram, ping3, time
from dotenv import load_dotenv

load_dotenv()
botToken = os.environ.get('token')
chatId = os.environ.get('main_chat_id')

def GetPingRes(servers):
    result = []
    for svr in servers:
        res = ping3.ping(svr)
        if res is None or res is False:
            result.append(-1)
        else:
            result.append(res)

    return result

async def send_message(bot):
    msg = ""
    servers = ["main", "sub1", "sub2"]
    xCnt = 0
    pingRes = GetPingRes(servers)
    for svr, res in zip(servers, pingRes):
        if res > 0:
            sent = f"{svr} ✅ {res:.4f}s\n"
            logging.info(sent)
            msg += sent
        else:
            xCnt += 1
            msg += f"{svr} ❌\n"
    if xCnt > 0:
        sent = f"{xCnt}/4 not working!"
        logging.warning(sent)
        msg += sent
    await bot.send_message(chatId,msg)

async def main():
    bot = telegram.Bot(token = botToken)
    await send_message(bot)
    time.sleep(35640)
    while True:
        await send_message(bot)
        time.sleep(43200) # 12시간 대기

if __name__ == "__main__":
    asyncio.run(main())