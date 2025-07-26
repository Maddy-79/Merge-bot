from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot, user_settings


@bot.on_message(filters.command("settings"))
async def settings_handler(client, message: Message):
    user_id = str(message.from_user.id)
    settings = user_settings.get(user_id, {
        "notify": True,
        "ask_metadata": True,
        "video_codec": "libx264",
        "audio_codec": "aac"
    })

    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"🔔 Notifications: {'ON' if settings['notify'] else 'OFF'}",
                callback_data="toggle_notify"
            )
        ],
        [
            InlineKeyboardButton(
                f"📽️ Ask Metadata: {'ON' if settings['ask_metadata'] else 'OFF'}",
                callback_data="toggle_metadata"
            )
        ],
        [
            InlineKeyboardButton("🎞️ Video Codec", callback_data="set_video_codec"),
            InlineKeyboardButton("🔊 Audio Codec", callback_data="set_audio_codec")
        ]
    ])

    await message.reply("🛠️ Your Settings:", reply_markup=markup)


@bot.on_callback_query(filters.regex("^toggle_notify$"))
async def toggle_notify_cb(client, callback_query):
    user_id = str(callback_query.from_user.id)
    settings = user_settings.setdefault(user_id, {})
    settings["notify"] = not settings.get("notify", True)
    await callback_query.answer(f"Notifications {'enabled' if settings['notify'] else 'disabled'} ✅")
    await settings_handler(client, callback_query.message)


@bot.on_callback_query(filters.regex("^toggle_metadata$"))
async def toggle_metadata_cb(client, callback_query):
    user_id = str(callback_query.from_user.id)
    settings = user_settings.setdefault(user_id, {})
    settings["ask_metadata"] = not settings.get("ask_metadata", True)
    await callback_query.answer(f"Metadata prompt {'enabled' if settings['ask_metadata'] else 'disabled'} 📝")
    await settings_handler(client, callback_query.message)
