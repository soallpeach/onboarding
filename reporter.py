from typing import Union

from requests import session, Session

import os

from models import ChallengeResult, ChallengeError

BASE_URL = os.getenv('API_URL', 'https://soallpeach-api-soroosh.fandogh.cloud')


def get_session() -> Session:
    session.headers.update({
        'Authorization': 'TOEKN ' + os.getenv('API_SECRET_KEY', 'STRONG_TOKEN')
    })
    return session


def report(result: Union[ChallengeResult, ChallengeError]):
    response = get_session().post(f'{BASE_URL}/scores', json=result)
    print(response)
