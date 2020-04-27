from typing import Union

import os
import yaml
import subprocess
import reporter
import time
import shutil

from models import StepResult, ChallengeResult, ChallengeError, Challenge, ChallengeResult2


class ChallengeExecution(object):
    def __init__(self, challenge: Challenge, repository: str):
        self.challenge = challenge
        self.repository = repository

    def prepare_workspace(self):
        shutil.rmtree('./workspace', ignore_errors=True)
        shutil.copytree(f'./challenges/{self.challenge.name}', './workspace/')

    def run_step(self, cmd: str, name: str, script_path: str, timeout: int = 10 * 60,
                 get_durtion_from_stdout: bool = False, parameters={}) -> StepResult:
        start = time.time()
        script_envs = {**os.environ, **parameters,
                       'CHALLENGE_NAME': self.challenge.name, 'REPOSITORY_URL': self.repository}

        p = subprocess.Popen(f'{cmd} {script_path}',
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=script_envs
                             )

        try:
            p.wait(timeout)
        except subprocess.TimeoutExpired as e:
            stdout_lines = p.stdout.readlines() if p.stdout else ''
            stderr_lines = p.stderr.readlines() if p.stderr else ''
            stdout = ''.join([line.decode("utf-8") for line in stdout_lines])
            stderr = ''.join([line.decode("utf-8") for line in stderr_lines])

            print(stderr)
            print(stdout)
            try:
                p.kill()
            except Exception as e:
                print(e)
            return StepResult(name, 9999, timeout, stdout, stderr + '\nTimeout')

        stdout_lines = p.stdout.readlines() if p.stdout else ''
        stderr_lines = p.stderr.readlines() if p.stderr else ''

        stdout = ''.join([line.decode("utf-8") for line in stdout_lines])
        stderr = ''.join([line.decode("utf-8") for line in stderr_lines])

        print(stderr)
        print(stdout)

        elapsed = time.time()
        returned_code = int(p.poll())
        duration = round(elapsed - start, 3)
        if returned_code == 0:
            if get_durtion_from_stdout:
                try:
                    duration_line = list(filter(lambda line: line.startswith(b'::::DURATION='), stdout_lines))[0][13:]
                    duration = float(duration_line)
                except Exception as e:
                    print(e)
                    duration = round(elapsed - start, 3)

        return StepResult(name, int(p.poll()), duration, stdout, stderr)


run_scripts = {
    'file': 'run_in_file_program.sh',
    'http': 'run_in_http_program.sh'
}


def run_challenge(challenge_execution: ChallengeExecution) -> Union[ChallengeResult, ChallengeResult2, ChallengeError]:
    print(f"Running challenge {challenge_execution.challenge.name} from repository {challenge_execution.repository}",
          flush=True)

    challenge_execution.prepare_workspace()
    build_result = challenge_execution.run_step('bash', 'build', 'scripts/build.sh', timeout=300)
    if build_result.code != 0:
        return ChallengeResult2(build=build_result)

    get_duration_from_stdout = True if challenge_execution.challenge.input_model == 'file' else False
    step_results = {build_result.name: build_result}
    if challenge_execution.challenge.custom_runner:
        for step in challenge_execution.challenge.steps:
            step_result = challenge_execution.run_step(step.runner, step.name, step.script, step.timeout,
                                                       parameters=challenge_execution.challenge.parameters)
            step_results[step_result.name] = step_result
            if step_result.code != 0:
                break

        return ChallengeResult2(**step_results)

    else:
        run_script = run_scripts.get(challenge_execution.challenge.input_model)
        run_result = challenge_execution.run_step('bash', 'run', f'scripts/{run_script}', timeout=10,
                                                  get_durtion_from_stdout=get_duration_from_stdout)
        if run_result.code != 0:
            return ChallengeError('Error in running the code', run_result)
        validate_result = challenge_execution.run_step('bash', 'validate', 'scripts/validate.sh', timeout=10)

        if validate_result.code != 0:
            return ChallengeError('Error in validating the result', validate_result)

        challenge_execution.run_step('bash', 'cleanup', 'scripts/cleanup.sh')
        return ChallengeResult(build_result, run_result, validate_result)


if __name__ == '__main__':
    with open('participants.yml') as participants_stream:
        participants = yaml.load(participants_stream, Loader=yaml.FullLoader)

    with open('challenges.yml') as challenges_stream:
        challenges = yaml.load(challenges_stream, Loader=yaml.FullLoader)

    for challenge_dict in challenges:
        challenge = Challenge.from_dict(challenge_dict)
        round_id = int(time.time())
        reporter.start_round(round_id, challenge.name)
        for p in participants:
            repository = p['repository']
            nickname = p['nickname']
            ce = ChallengeExecution(challenge, p['repository'])
            result = run_challenge(ce)
            reporter.report(nickname, challenge.name, round_id, result)
            print(result)
        reporter.finish_round(round_id, challenge.name)
