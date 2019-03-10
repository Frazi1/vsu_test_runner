import unittest

from coderunner.python.python_runner import PythonRunner
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum


class PythonRunnerTests(unittest.TestCase):
    runner = PythonRunner()

    def test_param_conversion(self):
        param = FunctionArgument(ArgumentType.STRING, "param1")
        self.assertEquals(self.runner._translate_parameter(param), "param1")

    def test_no_arg_function(self):
        function_ = Function("test_param_conversion", ArgumentType.STRING)
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionArgument(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner.translate_code(function_, snippet)
        expected ="""def test_param_conversion():
    param = FunctionArgument(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_one_arg_function(self):
        param1 = FunctionArgument(ArgumentType.VOID, "self")
        function_ = Function("test_param_conversion", ArgumentType.STRING, [param1])
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionArgument(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner.translate_code(function_, snippet)
        expected ="""def test_param_conversion(self):
    param = FunctionArgument(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_two_arg_function(self):
        param1 = FunctionArgument(ArgumentType.VOID, "self")
        param2 = FunctionArgument(ArgumentType.VOID, "param2")
        function_ = Function("test_param_conversion", ArgumentType.STRING, [param1, param2])
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionArgument(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner.translate_code(function_, snippet)
        print res
        expected = """def test_param_conversion(self, param2):
    param = FunctionArgument(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_indented_code(self):
        function_ = Function("test_param_conversion", ArgumentType.STRING)
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'if a is b:',
            '    self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner.translate_code(function_, snippet)
        print res
        expected = """def test_param_conversion():
    if a is b:
        self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        print expected
        self.assertEquals(res, expected)