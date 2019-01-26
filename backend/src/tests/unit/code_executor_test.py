import unittest

from coderunner.python_runner import PythonRunner
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from services.code_executer_service import Executer


class CodeExecutorTest(unittest.TestCase):
    executer = Executer()
    executer.register_runner(PythonRunner())

    def test_run_hello_world_code(self):
        res = self.executer.execute_code(LanguageEnum.PYTHON, ArgumentType.STRING, "print 'HELLO WORLD'")
        print len(res.output)
        self.assertEqual('HELLO WORLD', res.output)