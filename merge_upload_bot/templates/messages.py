# templates/messages.py
# All user-facing messages
def get_start_message():
    return (
        "👋 Welcome to Merge Upload Bot!\n\n"
        "📄 Upload your docs/videos (.mkv, .mp4, etc.)\n"
        "🎞️ Merge subtitles\n"
        "🔊 Support multiple audio tracks\n"
        "✏️ Edit metadata\n"
        "🚀 Get final file back with progress updates!"
    )

def get_help_message():
    return (
        "📚 *How to use this bot:*\n\n"
        "1. Upload your video or document files\n"
        "2. Optionally upload subtitle files (SRT/ASS)\n"
        "3. Choose merge/edit settings (metadata, audio, etc.)\n"
        "4. Bot will process & send you the final file with progress updates!"
    )

def get_error_message(error: str):
    return f"❌ Error occurred: {error}"

def get_success_message(filename: str):
    return f"✅ Successfully processed and uploaded `{filename}`!"

def get_processing_message():
    return "⏳ Processing your file... this might take a few minutes."

def get_progress_template():
    return "🚧 Progress: {percent}% | {current}/{total}"

def get_settings_message():
    return (
        "⚙️ *Current Settings:*\n"
        "• Merge subtitles: {sub_merge}\n"
        "• Include all audio tracks: {multi_audio}\n"
        "• Ask before editing metadata: {meta_edit}\n"
        "\nUse buttons below to toggle."
    )

def get_admin_message():
    return "👑 You are accessing the admin panel."

def get_not_admin_message():
    return "🚫 This command is for admins only."

def get_cancelled_message():
    return "❌ Task cancelled by user."

def get_metadata_prompt():
    return "📝 Enter new metadata in format: `title | artist | genre | year` or send /skip."

def get_file_received_message():
    return "📥 File received. What would you like to do next?"

def get_unknown_command_message():
    return "❓ Unknown command. Use /help to see available commands."

def get_task_page_title(index: int, total: int):
    return f"📄 Task {index+1} of {total}"

def get_task_controls():
    return ["⏮ Prev", "🔁 Restart", "⏭ Next"]
