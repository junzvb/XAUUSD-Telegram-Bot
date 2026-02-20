import logging, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from strategies import get_trade_signal
from daily_mapping import schedule_daily_mapping
from pending_orders import pending_orders

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = ""
CHAT_ID = "t.me/xauusdgoldd_bot"

last_alert_time = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 XAUUSD Real-time Bot Ready!\nUse /signal for latest setup.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_alert_time
    import time
    now = time.time()
    if last_alert_time and now - last_alert_time < 60:
        await update.message.reply_text("⏳ Wait before next alert to avoid spam.")
        return
    signal_data = get_trade_signal()
    if signal_data['type'] != "WAIT":
        pending_orders.add_order(signal_data)
        message = (
            f"💰 Symbol: {signal_data['symbol']}\n"
            f"📈 Type: {signal_data['type']}\n"
            f"🟢 Entry: {signal_data['entry']}\n"
            f"🔴 SL: {signal_data['sl']}\n"
            f"🏹 TP: {signal_data['tp']}\n"
            f"📌 Technique: {signal_data['technique']}"
        )
        keyboard = [
            [InlineKeyboardButton("SL/TP", callback_data="sl_tp"),
             InlineKeyboardButton("Reason/Technique", callback_data="reason")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup)
        last_alert_time = now
    else:
        await update.message.reply_text("No clear setup. Waiting for high-probability zone.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "sl_tp":
        await query.edit_message_text("🔴 SL: Tight\n🏹 TP: Big reward (to the moon style)")
    elif query.data == "reason":
        await query.edit_message_text("📌 Reason: High-probability setup using multiple techniques.")

async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = pending_orders.get_orders()
    if not orders:
        await update.message.reply_text("No pending orders.")
        return
    message = "🕒 Pending Orders:\n"
    for o in orders:
        message += f"{o['type']} {o['symbol']} Entry: {o['entry']} SL: {o['sl']} TP: {o['tp']}\n"
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("pending", pending))
    app.add_handler(CallbackQueryHandler(button_callback))
    schedule_daily_mapping(app)
    print("Bot running with auto zone + pending orders...")
    app.run_polling()
