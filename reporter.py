from typing import Union

from requests import session, Session, Response
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


def is_ok(status_code: int) -> bool:
    if 200 <= status_code <= 299:
        return True
    return False


def raise_error_on_not_ok(response: Response, message: str):
    if not is_ok(response.status_code):
        raise Exception(f'{message}, response: {response.text} status:{response.status_code}')


def report(nickname: str, challenge_name: str, run_id: str, result: Union[ChallengeResult, ChallengeError]):
    request = ReportRequest(nickname, challenge_name, run_id, result)
    request_json = json.dumps(request.__dict__, default=lambda o: o.__dict__, indent=4)
    response = get_session().post(f'{BASE_URL}/scores', data=request_json)
    raise_error_on_not_ok(response, 'Error in reporting')


def start_round(round_id: int, challenge_name: str):
    response = get_session().post(f'{BASE_URL}/challenges/{challenge_name}/rounds',
                                  json={'round_id': round_id, 'challenge_name': challenge_name})
    raise_error_on_not_ok(response, f'Error in starting round {round_id} chalenge {challenge_name}')


def finish_round(round_id: int, challenge_name: str):
    response = get_session().patch(f'{BASE_URL}/challenges/{challenge_name}/rounds{round_id}', json={'status': 'DONE'})
    raise_error_on_not_ok(response, f'Error in finishing round {round_id} challenge {challenge_name}')
