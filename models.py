from dataclasses import dataclass


@dataclass
class Challenge(object):
    name: str
    description: str
    input_model: str
    custom_runner: bool


@dataclass
class StepResult(object):
    name: str
    code: int
    duration: int
    stdout: str
    stderr: str


@dataclass
class ChallengeResult(object):
    validate_result: StepResult
    run_result: StepResult
    build_result: StepResult


@dataclass
class ChallengeError(Exception):
    message: str
    step_result: StepResult
