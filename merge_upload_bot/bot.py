import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from bot.handlers import start, settings, merge, status, admin
from bot.inline_buttons import main_menu_buttons
from config.secrets import BOT_TOKEN, ADMINS

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register Handlers
def register_all_handlers():
    start.register(dp)
    settings.register(dp)
    merge.register(dp)
    status.register(dp)
    admin.register(dp)

# Startup message
async def on_startup(dispatcher):
    logger.info("Bot started")
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "🤖 Bot started and ready!")
        except Exception as e:
            logger.error(f"Can't send message to admin {admin}: {e}")

# Shutdown cleanup
async def on_shutdown(dispatcher):
    logger.info("Bot stopped")
    await bot.session.close()

if __name__ == '__main__':
    register_all_handlers()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
