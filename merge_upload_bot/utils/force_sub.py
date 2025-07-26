from pyrogram.types import Message
from config.config import FORCE_SUB_CHANNEL
from pyrogram import Client, errors


async def check_force_sub(client: Client, message: Message):
    if not FORCE_SUB_CHANNEL:
        return True  # No channel configured

    try:
        user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
        if user.status in ["member", "creator", "administrator"]:
            return True
        return False
    except errors.UserNotParticipant:
        return False
    except errors.ChatAdminRequired:
        print("Make bot admin in force sub channel")
        return False
    except Exception as e:
        print(f"Force sub check error: {e}")
        return True  # Don't block if error


def get_force_sub_text():
    return ("🚫 **You must join our channel before using this bot!**\n"
            "👉 [Click here to Join](@{FORCE_SUB_CHANNEL})\n"
            "Then click /start again.")
