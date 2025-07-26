from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.ffmpeg_tools import merge_videos
from bot.utils.metadata import prompt_metadata_edit
from bot.utils.storage import save_task, get_user_tasks
from bot.inline_buttons import get_progress_buttons

from loader import dp, bot

@dp.message_handler(commands=['merge'])
async def merge_command(message: types.Message, state: FSMContext):
    await message.answer("Send me the video files you want to merge. Type /done when you're finished.")
    await state.set_state("waiting_videos")
    await state.update_data(videos=[])

@dp.message_handler(lambda message: message.video and message.video.file_id, state="waiting_videos")
async def collect_videos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    videos = data.get("videos", [])
    videos.append(message.video.file_id)
    await state.update_data(videos=videos)
    await message.answer(f"Added video {len(videos)}. Send more or type /done.")

@dp.message_handler(commands=['done'], state="waiting_videos")
async def done_collecting(message: types.Message, state: FSMContext):
    data = await state.get_data()
    videos = data.get("videos", [])
    if len(videos) < 2:
        return await message.answer("You need to send at least 2 videos to merge.")

    msg = await message.answer("Merging in progress... ⏳")
    merged_path = await merge_videos(videos, message.from_user.id)

    await msg.edit_text("Do you want to edit metadata (title, audio, subtitle)?")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Yes, edit", callback_data="edit_metadata"))
    markup.add(InlineKeyboardButton("No, skip", callback_data="skip_metadata"))

    await state.set_state("post_merge")
    await state.update_data(merged_path=merged_path, msg_id=msg.message_id)
    await bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data in ["edit_metadata", "skip_metadata"], state="post_merge")
async def handle_metadata_choice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    merged_path = data.get("merged_path")

    if callback.data == "edit_metadata":
        await callback.message.edit_text("Editing metadata...")
        await prompt_metadata_edit(callback.message, merged_path, state)
    else:
        await callback.message.edit_text("Uploading final merged video... 🚀")
        video_msg = await bot.send_video(callback.message.chat.id, open(merged_path, 'rb'))
        await save_task(callback.from_user.id, video_msg.message_id, merged_path)

    await state.finish()
