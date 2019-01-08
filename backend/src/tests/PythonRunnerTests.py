import unittest

from src.coderunner.PythonRunner import PythonRunner
from src.models.ArgumentType import ArgumentType
from src.models.CodeSnippet import CodeSnippet
from src.models.Function import Function
from src.models.FunctionParameter import FunctionParameter
from src.models.LanguageEnum import LanguageEnum


class PythonRunnerTests(unittest.TestCase):
    runner = PythonRunner()

    def test_param_conversion(self):
        param = FunctionParameter(ArgumentType.STRING, "param1")
        self.assertEquals(self.runner._translate_parameter(param), "param1")

    def test_no_arg_function(self):
        function_ = Function("test_param_conversion", ArgumentType.STRING)
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionParameter(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner._translate_code(function_, snippet)
        expected ="""def test_param_conversion():
    param = FunctionParameter(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_one_arg_function(self):
        param1 = FunctionParameter(ArgumentType.VOID, "self")
        function_ = Function("test_param_conversion", ArgumentType.STRING, [param1])
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionParameter(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner._translate_code(function_, snippet)
        expected ="""def test_param_conversion(self):
    param = FunctionParameter(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_two_arg_function(self):
        param1 = FunctionParameter(ArgumentType.VOID, "self")
        param2 = FunctionParameter(ArgumentType.VOID, "param2")
        function_ = Function("test_param_conversion", ArgumentType.STRING, [param1, param2])
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'param = FunctionParameter(ArgumentType.STRING, "param1")',
            'self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner._translate_code(function_, snippet)
        print res
        expected = """def test_param_conversion(self, param2):
    param = FunctionParameter(ArgumentType.STRING, "param1")
    self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        self.assertEquals(res, expected)

    def test_indented_code(self):
        function_ = Function("test_param_conversion", ArgumentType.STRING)
        snippet = CodeSnippet(LanguageEnum.PYTHON, [
            'if a is b:',
            '    self.assertEquals(self.runner.translate_parameter(param), "param1")'
        ], function_)
        res = self.runner._translate_code(function_, snippet)
        print res
        expected = """def test_param_conversion():
    if a is b:
        self.assertEquals(self.runner.translate_parameter(param), "param1")"""
        print expected
        self.assertEquals(res, expected)