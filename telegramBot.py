import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import datetime
import multiprocessing
import threading
from time import sleep
import pytz

# Token của bot
TOKEN = '7392075828:AAEfBjUKzgQnrIT4jIkhUV2YzKGxQOnGXDM'

vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Hẹn giờ
timers = [
    {
        'time': '11:25:00 AM',
        'message': 'Sắp đến giờ ăn!!! Anh em chuẩn bị 😑.'
    },
    {
        'time': '11:30:00 AM',
        'message': 'Toàn thể anh em chú ý. Đã đến giờ đi ăn!!! 😃😃😃'
    },
    {
        'time': '5:00:00 PM',
        'message': 'Gần đến giờ về!!! Anh em chuẩn bị!'
    },
    {
        'time': '12:00:00 AM',
        'message': 'Ăn xong rồi! Lên thôi anh em 😊.'
    },
    {
        'time': '10:00:00 AM',
        'message': 'Test ok'
    },
]

timeThreads = []
stopAllThreads = False

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hàm start khi người dùng bắt đầu trò chuyện với bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global timers, timeThreads, stopAllThreads
    await update.message.reply_text('Thứ này được tạo ra để nhắc nhở ae đi ăn, lên ngủ trưa và về đúng giờ!!!')
    # try:
    # if len(timeThreads):
    #     await update.message.reply_text('Đang hủy bộ hẹn giờ cũ!!!')
    #     stopAllThreads = True
    #     for timeThread in timeThreads:
    #         timeThread.join(timeout=0)
    #     timeThreads = []
    # except Exception as e:
    #     await update.message.reply_text('Lỗi khi hủy bộ hẹn giờ cũ:' + e)
    # try:
    # stopAllThreads = False
    for timer in timers:
        # tạo hàm để chạy bộ hẹn giờ
        async def timerDef(timer):
            time = datetime.datetime.strptime(timer['time'], "%I:%M:%S %p").time()
            while True:
                now = datetime.datetime.now(vietnam_tz).time()
                await asyncio.sleep(1)
                if(time.hour == now.hour and time.minute == now.minute and time.second == now.second):
                    await update.message.reply_text(timer['message'])
        # tạo hàm để chạy trong thread
        def run_coroutine():
            asyncio.run(timerDef(timer))
        # tạo thread
        # timeThread = multiprocessing.Process(target=run_coroutine)
        timeThread = threading.Thread(target=run_coroutine)
        timeThread.start()
        print('thread start with time', timer['time'])
        timeThreads.append(timeThread)
    await update.message.reply_text('Đã kích hoạt bộ hẹn giờ mới!!!')
    await update.message.reply_text('Bộ hẹn giờ bao gồm')
    for timer in timers:
        await update.message.reply_text('Thời gian: ' + timer['time'] + '. Thông báo: ' + timer['message'])
    # except Exception as e:
    #     await update.message.reply_text('Lỗi khi kích hoạt bộ hẹn giờ:' + e)
        
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('test...')
    async def test1():
        while True:
            await asyncio.sleep(5)
            print('test is ok')
            await update.message.reply_text('test is ok')
    def test2():
        asyncio.run(test1())
    timeThread = threading.Thread(target=test2)
    timeThread.start()

    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Help cái gì mà help -.-')
            
def error(update, context):
    logger.warning('Có lỗi: %s :(((', context.error)
        
app =  Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("test", test))
app.add_handler(CommandHandler("help", help))
app.add_error_handler(error)
app.run_polling()
