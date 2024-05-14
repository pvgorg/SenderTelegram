from asyncio import sleep
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler


API_ID = 23403371  # Your API ID
API_HASH = '68d4eed389072a016e929ea086329437'  # Your API HASH
ADMIN_ID = 1502490631  # Your USER ID

client = Client('tanchi', API_ID, API_HASH)
scheduler = AsyncIOScheduler(timezone='Asia/Tehran')
banner = None
banne_time = 10


async def send_banner():
    global banner

    if banner:
        async for chat in client.get_dialogs():
            if chat.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                try:
                    await sleep(4)
                    await client.send_message(chat.chat.id, banner)

                except:
                    continue

with client:
    try:
        client.join_chat('@Roh_bijan')
        client.join_chat('@rav_ani')
    except:
        pass

@client.on_message(filters.user(ADMIN_ID) & filters.text)
async def message_handler(_, message: Message):
    global banner, banne_time

    text = message.text.lower()

    if text == '/ping':
        await message.reply_text('هستم داش خیالت راحت')

    elif text == '/banner on':
        scheduler.add_job(send_banner, 'interval', seconds=int(banne_time))
        await message.reply_text('🟢 حالت ارسال بنر با موفقیت فعال شد !')

    elif text == '/banner off':
        scheduler.remove_all_jobs()
        await message.reply_text('🔴 حالت ارسال بنر با موفقیت غیر فعال شد !')

    elif text == '/setbanner' and message.reply_to_message:
        banner = message.reply_to_message.text

        await message.reply_text('🏞 بنر مورد نظر با موفقیت تنظیم شد !')

    elif text.startswith('/settime'):
        banne_time = int(text.split('/settime')[1])
        await message.reply_text(f'⌛️ زمان بنر مورد نظر با موفقیت به ( `{banne_time}` ) تنظیم شد !')

    elif text == '/help':
        await message.reply_text('''
            `/ping` ⤳ بررسی آنلاین بودن بات
            `/banner on/off` ⤳ فعال سازی/غیرفعال‌سازی حالت بنر
            `/setbanner` reply ⤳ تنظیم بنر
            `/settime` s ⤳ تنظیم زمان ارسال بنر به دقیقه                      
    ''')




scheduler.start()
client.run()
