import schedule, pytz, datetime, asyncio, threading

async def send_daily_mapping(app):
    chat_id = "YOUR_TELEGRAM_CHAT_ID"
    tz = pytz.timezone("Asia/Kuala_Lumpur")
    now = datetime.datetime.now(tz)
    message = f"📊 Daily Mapping {now.strftime('%Y-%m-%d %H:%M')} MYT: Check XAUUSD zones!"
    await app.bot.send_message(chat_id=chat_id, text=message)

def schedule_daily_mapping(app):
    def job():
        asyncio.run(send_daily_mapping(app))
    schedule.every().day.at("09:00").do(job)
    threading.Thread(target=lambda: [schedule.run_pending() for _ in iter(int,1)]).start()
