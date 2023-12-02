from typing import Annotated

from fastapi import Depends

from utils.app_token import AppToken


def get_token():
    return AppToken()


BookingToken = Annotated[AppToken, Depends(get_token)]
