import uuid


class BaseRunner:
    __file_ext__ = None

    def __init__(self):
        pass

    def _translate_parameter(self, function_parameter):
        raise NotImplemented

    def _translate_code(self, function_signature, code_snippet):
        raise NotImplemented

    def execute(self, function_signature, code_snippet):
        raise NotImplemented

    def write_code(self, code):
        file_name = uuid.uuid4().get_hex()
        with open(file_name + self.__file_ext__, "w") as file_:
            file_.write(code)
        return file_name