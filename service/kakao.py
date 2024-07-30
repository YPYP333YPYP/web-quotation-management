import json
import os

import aiohttp
import dotenv

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException

dotenv.load_dotenv()


class KakaoService:
    def __init__(self):
        self.access_token = os.getenv('KAKAO_ACCESS_TOKEN')

    async def send_quotation_completed_message(self, quotation_id, web_url):
        api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.access_token}"
        }

        template_object = {
            "object_type": "text",
            "text": f"견적서 #{quotation_id}가 완료되었습니다. 확인해 주세요.",
            "link": {
                "web_url": web_url,
                "mobile_web_url": web_url
            },
            "button_title": "견적서 확인"
        }

        data = {
            "template_object": json.dumps(template_object)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, data=data) as response:
                print(response)
                # if response.status == 200:
                #     return await response.json()
                # else:
                #     raise ServiceException(ErrorStatus.KAKAO_MESSAGE_NOT_SENT)
