import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import datetime

# Token của bot
TOKEN = '7392075828:AAEfBjUKzgQnrIT4jIkhUV2YzKGxQOnGXDM'

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hàm start khi người dùng bắt đầu trò chuyện với bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Thứ này được tạo ra để nhắc nhở ae đi ăn, lên ngủ trưa và về đúng giờ')
    while True:
        # if CHAT_ID:
        #     print(CHAT_ID)
        #     await app.bot.send_message(chat_id=CHAT_ID, text='test')
        if datetime.datetime.now().strftime("%I:%M:%S %p") == "11:30:00 AM":
            await update.message.reply_text('Tất cả đi ăn trưa!!!')
        await asyncio.sleep(10) 
        
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('test is ok')
            
def error(update, context):
    logger.warning('Có lỗi: %s', context.error)
        
app =  Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_error_handler(error)
app.run_polling()
