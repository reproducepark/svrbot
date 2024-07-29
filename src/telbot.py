import logging, os
import asyncio, telegram, ping3, time, pytz
from datetime import datetime, timedelta
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
    print("starting service...")

    timeZone = pytz.timezone('Asia/Seoul')

    now = datetime.now(timeZone)
    target = now.replace(hour=6, minute=0, second=0, microsecond=0)
    
    if now >= target:
        target += timedelta(days=1)
    timeRemaining = target - now
    secondsRemaining = timeRemaining.total_seconds()

    bot = telegram.Bot(token = botToken)
    await send_message(bot)
    
    time.sleep(secondsRemaining)
    while True:
        await send_message(bot)
        time.sleep(43200) # 12시간 대기

if __name__ == "__main__":
    asyncio.run(main())