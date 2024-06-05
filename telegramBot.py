import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import datetime
import threading
from time import sleep

# Token của bot
TOKEN = '7392075828:AAEfBjUKzgQnrIT4jIkhUV2YzKGxQOnGXDM'

# Hẹn giờ
timers = [
    {
        'time': '11:30:00 AM',
        'message': 'Đã đến giờ đi ăn!!!'
    },
    {
        'time': '5:00:00 PM',
        'message': 'Đã đến giờ về!!!'
    },
    {
        'time': '12:00:00 AM',
        'message': 'Ăn xong rồi!!!'
    },
    {
        'time': '4:50:00 PM',
        'message': '10 phút đếm ngược cho đến giờ về!!!'
    },
    {
        'time': '4:55:00 PM',
        'message': '5 phút đếm ngược cho đến giờ về!!!'
    },
    {
        'time': '4:59:00 PM',
        'message': '1 phút đếm ngược cho đến giờ về!!!'
    },
    {
        'time': '3:46:00 PM',
        'message': 'Test ok'
    },
]

timeThreads = []

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hàm start khi người dùng bắt đầu trò chuyện với bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global timers, timeThreads
    await update.message.reply_text('Thứ này được tạo ra để nhắc nhở ae đi ăn, lên ngủ trưa và về đúng giờ!!!')
    for timer in timers:
        # tạo hàm để chạy bộ hẹn giờ
        async def timerDef(timer):
            while True:
                now = datetime.datetime.now()
                today = now.today()
                time = datetime.datetime.strptime(timer['time'], "%I:%M:%S %p").time()
                time = datetime.datetime.combine(today, time)
                if time < now:
                    time += datetime.timedelta(days=1)
                timeSleep = (time - now).total_seconds()
                print('Count time in', timeSleep, 's to message', timer['message'])         
                await asyncio.sleep(timeSleep)
                await update.message.reply_text(timer['message'])
        # tạo hàm để chạy trong thread
        def run_coroutine():
            asyncio.run(timerDef(timer))
        # tạo thread
        timeThread = threading.Thread(target=run_coroutine)
        timeThread.start()
        print('thread start with time', timer['time'])
        timeThreads.append(timeThread)
        
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('test is ok')
            
def error(update, context):
    logger.warning('Có lỗi: %s', context.error)
        
app =  Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_error_handler(error)
app.run_polling()
