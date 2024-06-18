import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import datetime
import multiprocessing
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
        'time': '8:51:00 AM',
        'message': 'Test ok'
    },
    {
        'time': '8:52:00 AM',
        'message': 'Test ok'
    },
    {
        'time': '8:53:00 AM',
        'message': 'Test ok'
    },
    {
        'time': '8:27:00 AM',
        'message': 'Test ok'
    },
    {
        'time': '8:28:00 AM',
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
    if len(timeThreads):
        await update.message.reply_text('Đang hủy bộ hẹn giờ cũ!!!')
        stopAllThreads = True
        for timeThread in timeThreads:
            timeThread.join(timeout=0)
        timeThreads = []
    # except Exception as e:
    #     await update.message.reply_text('Lỗi khi hủy bộ hẹn giờ cũ:' + e)
    # try:
    await update.message.reply_text('Đã kích hoạt bộ hẹn giờ mới!!!')
    await update.message.reply_text('Bộ hẹn giờ bao gồm')

    stopAllThreads = False
    for timer in timers:
        # tạo hàm để chạy bộ hẹn giờ
        async def timerDef():
            while True:
                now = datetime.datetime.now()
                today = now.today()
                time = datetime.datetime.strptime(timer['time'], "%I:%M:%S %p").time()
                time = datetime.datetime.combine(today, time)
                if time < now:
                    time += datetime.timedelta(days=1)
                timeSleep = (time - now).total_seconds()
                print('Count time in', timeSleep, 's to message', timer['message'])
                await update.message.reply_text(f"Thời gian: {timer['time']}. Thông báo: {timer['message']}. Thời gian còn: {timeSleep}")
                # await update.message.reply_text('Đã kích hoạt bộ hẹn giờ mới!!!')        
                # await asyncio.sleep(timeSleep)
                while time > datetime.datetime.now():
                    sleep(10)
                    if stopAllThreads:
                        break
                if stopAllThreads:
                    break
                await update.message.reply_text(timer['message'])
        # tạo thread
        # timeThread = multiprocessing.Process(target=run_coroutine)
        timeThread = threading.Thread(target=timerDef)
        timeThread.start()
        print('thread start with time', timer['time'])
        timeThreads.append(timeThread)
    # for timer in timers:
    #     await update.message.reply_text(f'Thời gian: {timer['time']}. Thông báo: {timer['message']}. Thời gian còn: {}')
    # except Exception as e:
    #     await update.message.reply_text('Lỗi khi kích hoạt bộ hẹn giờ:' + e)
        
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('test...')
    async def test1():
        while True:
            sleep(5)
            print('test is ok')
            await update.message.reply_text('test is ok')
    timeThread = threading.Thread(target=test1)
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
