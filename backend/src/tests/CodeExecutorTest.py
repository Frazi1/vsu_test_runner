import unittest

from src.coderunner.PythonRunner import PythonRunner
from src.models.ArgumentType import ArgumentType
from src.models.LanguageEnum import LanguageEnum
from src.services.CodeExecuterService import Executer


class PythonRunnerTests(unittest.TestCase):
    executer = Executer()
    executer.register_runner(PythonRunner())

    def test_run_hello_world_code(self):
        res = self.executer.execute_code(LanguageEnum.PYTHON, ArgumentType.STRING, "print 'HELLO WORLD'")
        print len(res.output)
        self.assertEqual('HELLO WORLD', res.output)