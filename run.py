from typing import Union

import yaml
import subprocess
import time


class StepResult(object):
    def __init__(self, name: str, code: int, duration: int,
                 stdout: str, stderr: str):
        self.name = name
        self.code = code
        self.duration = duration
        self.stderr = stderr
        self.stdout = stdout

    def __repr__(self) -> str:
        return self.name + " " + str(self.code) + " " + str(self.duration) + " " + self.stdout + " " + self.stderr


class ChallengeResult(object):
    def __init__(self, build_result: StepResult, run_result: StepResult, validate_result: StepResult):
        self.build_result = build_result
        self.run_result = run_result
        self.validate_result = validate_result


class ChallengeError(Exception):
    pass


class ChallengeExecution(object):
    def __init__(self, challenge_name: str, repository: str):
        self.repository = repository
        self.challenge_name = challenge_name

    def run_step(self, script_path: str) -> int:
        code = os.system('''
                export REPOSITORY_URL={}
                export CHALLENGE_NAME={}
                bash {}
                '''.format(self.repository, self.challenge_name, script_path))

        return int(code)


def run_challenge(challenge_execution: ChallengeExecution) -> Union[Result, RunError]:
    print(f"Running challenge ${challenge_execution.challenge_name} from repository ${challenge_execution.repository}",
          flush=True)
    build_code = challenge_execution.run_step('scripts/build.sh')
    run_code = challenge_execution.run_step('scripts/run_in_file_program.sh')
    validate_code = challenge_execution.run_step('scripts/validate.sh')

    print(build_code)
    print(run_code)
    print(validate_code)
    if build_code != 0:
        # TODO: handle error
        return RunError()


if __name__ == '__main__':
    with open('participants.yml') as participants_stream:
        participants = yaml.load(participants_stream, Loader=yaml.FullLoader)

    with open('challenges.yml') as challenges_stream:
        challenges = yaml.load(challenges_stream, Loader=yaml.FullLoader)

    for challenge in challenges:
        for p in participants:
            challenge_execution = ChallengeExecution(challenge['name'], p['repository'])
            result = run_challenge(challenge_execution)
