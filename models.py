class Challenge(object):
    def __init__(self, name: str, description: str, input_model: str, custom_runner: bool):
        self.name = name
        self.description = description
        self.input_model = input_model
        self.custom_runner = custom_runner


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
    validate_result: StepResult
    run_result: StepResult
    build_result: StepResult

    def __init__(self, build_result: StepResult, run_result: StepResult, validate_result: StepResult):
        self.build_result = build_result
        self.run_result = run_result
        self.validate_result = validate_result

    def __str__(self) -> str:
        return str(self.__dict__)


class ChallengeError(Exception):
    def __init__(self, message: str, step_result: StepResult):
        self.message = message
        self.step_result = step_result
