from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.storage import get_user_tasks

@Client.on_message(filters.command("status"))
async def status_handler(client, message):
    user_id = str(message.from_user.id)
    tasks = get_user_tasks(user_id)

    if not tasks:
        await message.reply("🚫 No active or recent tasks found.")
        return

    text = "📝 **Your Tasks:**\n\n"
    for idx, task in enumerate(tasks[-5:], 1):
        text += f"`{idx}.` **{task['filename']}**\nStatus: `{task['status']}`\n"

    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_status")]
        ])
    )

@Client.on_callback_query(filters.regex("refresh_status"))
async def refresh_status_callback(client, callback_query):
    user_id = str(callback_query.from_user.id)
    tasks = get_user_tasks(user_id)

    if not tasks:
        await callback_query.message.edit("🚫 No active or recent tasks found.")
        return

    text = "📝 **Your Tasks:**\n\n"
    for idx, task in enumerate(tasks[-5:], 1):
        text += f"`{idx}.` **{task['filename']}**\nStatus: `{task['status']}`\n"

    await callback_query.message.edit(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_status")]
        ])
    )
