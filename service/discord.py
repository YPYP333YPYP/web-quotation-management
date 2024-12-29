import json
import os
from datetime import datetime

import aiohttp

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException


async def send_discord_alert(webhook_url: str, message: str):
    async with aiohttp.ClientSession() as session:
        webhook_data = {
            "content": message,
            "username": "MINIFOOD SERVER BOT"
        }
        async with session.post(webhook_url, data=json.dumps(webhook_data),
                                headers={"Content-Type": "application/json"}) as response:
            if response.status != 204:
                raise GeneralException(ErrorStatus.DISCORD_MESSAGE_NOT_SENT)


async def send_discord_startup_message():
    webhook_url = os.getenv("DISCORD_WEB_HOOK")
    message = f"서버가 시작되었습니다. {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
    await send_discord_alert(webhook_url, message)


async def send_discord_shutdown_message():
    webhook_url = os.getenv("DISCORD_WEB_HOOK")
    message = f"서버가 종료되었습니다. {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
    await send_discord_alert(webhook_url, message)