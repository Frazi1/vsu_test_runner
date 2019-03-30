class FileRunResult(object):
    def __init__(self, input: str, output: str, error: str):
        self.input = input
        self.output = output
        self.error = error
