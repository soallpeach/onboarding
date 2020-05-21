from typing import Union
from models import ChallengeResult, ChallengeError, ChallengeResult2


class ReportRequest(object):
    nickname: str
    challenge_name: str
    run_id: str
    result: Union[ChallengeResult, ChallengeError]
    state: str

    def __init__(self, nickname: str, challenge_name: str, round_id: str,
                 result: Union[ChallengeResult, ChallengeError]):
        self.nickname = nickname
        self.challenge_name = challenge_name
        self.round = round_id
        self.result = result
        self.state = 'PASSED' if isinstance(result, ChallengeResult2) else 'FAILED'


def report(nickname: str, challenge_name: str, run_id: str, result: Union[ChallengeResult, ChallengeError]):
    pass


def start_round(round_id: int, challenge_name: str):
    pass


def finish_round(round_id: int, challenge_name: str):
    pass
