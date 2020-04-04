from typing import Union

from requests import session, Session
import json

import os

from models import ChallengeResult, ChallengeError

BASE_URL = os.getenv('API_URL', 'https://soallpeach-api-soroosh.fandogh.cloud')

session = Session()


def get_session() -> Session:
    session.headers.update({
        'Authorization': 'TOKEN ' + os.getenv('API_SECRET_KEY', 'STRONG_TOKEN'),
        'Content-Type': 'application/json'
    })
    return session


class ReportRequest(object):
    nickname: str
    challenge_name: str
    run_id: str
    result: Union[ChallengeResult, ChallengeError]
    state: str

    def __init__(self, nickname: str, challenge_name: str, run_id: str, result: Union[ChallengeResult, ChallengeError]):
        self.nickname = nickname
        self.challenge_name = challenge_name
        self.run_id = run_id
        self.result = result
        self.state = 'PASSED' if isinstance(result, ChallengeResult) else 'FAILED'


def report(nickname: str, challenge_name: str, run_id: str, result: Union[ChallengeResult, ChallengeError]):
    request = ReportRequest(nickname, challenge_name, run_id, result)
    request_json = json.dumps(request.__dict__, default=lambda o: o.__dict__, indent=4)
    response = get_session().post(f'{BASE_URL}/scores', data=request_json)
    print(response)
    print(response.text)
