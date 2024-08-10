import os

import dotenv
import jwt
from jwt import InvalidTokenError

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException

dotenv.load_dotenv()


def list_to_string(lst):
    return ','.join(map(str, lst))


def string_to_list(string):
    return [int(item) for item in string.split(',') if item]


def get_user_id_from_token(token):
    if not token:
        return None

    try:
        secret_key = os.environ.get("SECRET_KEY")
        algorithm = os.environ.get("ALGORITHM")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get('user_id')

        return user_id
    except InvalidTokenError:
        raise GeneralException(ErrorStatus.INVALID_TOKEN)


def load_blacklist(file_path: str = "blacklist.txt"):
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]