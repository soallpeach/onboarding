from dataclasses import dataclass
from typing import List, Dict



@dataclass
class CommitInfo(object):
    repository_url: str
    hash: str
    subject: str


@dataclass
class ChallengeStep(object):
    name: str
    runner: str
    script: str
    timeout: int

    @staticmethod
    def from_dict(dict):
        return ChallengeStep(dict['name'], dict['runner'], dict['script'], dict['timeout'])


@dataclass
class Challenge(object):
    name: str
    description: str
    input_model: str
    custom_runner: bool
    steps: List[ChallengeStep]
    parameters: Dict[str, str]

    @staticmethod
    def from_dict(dict):
        challenge_name = dict['name']
        challenge_input_model = dict['input_model']
        custom_runner = dict.get('custom_runner', False)
        parameters = dict.get('parameters', {})
        steps = [ChallengeStep.from_dict(step_dict) for step_dict in dict.get('steps', [])]
        challenge = Challenge(challenge_name, '', challenge_input_model, custom_runner, steps, parameters)
        return challenge


@dataclass
class StepResult(object):
    name: str
    code: int
    duration: int
    stdout: str
    stderr: str


@dataclass
class ChallengeResult(object):
    commit_info: CommitInfo
    validate_result: StepResult
    run_result: StepResult
    build_result: StepResult


class ChallengeResult2(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self) -> str:
        return str(self.__dict__)


@dataclass
class ChallengeError(Exception):
    message: str
    step_result: StepResult

