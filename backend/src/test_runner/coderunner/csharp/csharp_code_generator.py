import os
import re

from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.scaffolding_type import ScaffoldingType
from models.argument_type import ArgumentType
from models.function import Function
from models.function_parameter import FunctionArgument


class CSharpCodeGenerator(BaseCodeGenerator):
    SINGLE_LINE_COMMENT_START = "//"
    TARGET_FUNCTION_MARKER = [
        SINGLE_LINE_COMMENT_START + "TargetFunction",
        SINGLE_LINE_COMMENT_START + "EndTargetFunction"
    ]

    SOLUTION_MARKER = [
        SINGLE_LINE_COMMENT_START + "SolutionStart",
        SINGLE_LINE_COMMENT_START + "SolutionEnd"
    ]

    PROGRAM_TEMPLATE = """
using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace TestRunner
{{
    internal class Program
    {{
        public static void Main(string[] args)
        {{
             {return_type} res = {target_function_call};
             Console.WriteLine(res);
        }}

        //TargetFunction
        {target_function_declaration}
        //EndTargetFunction

    }}
}}"""

    def __init__(self):
        self.target_function_regex = re.compile(r'{start_target_function}{line_sep}?(.*?){end_target_function}'
                                                .format(line_sep="\n",
                                                        start_target_function=self.TARGET_FUNCTION_MARKER[0],
                                                        end_target_function=self.TARGET_FUNCTION_MARKER[1]),
                                                re.RegexFlag.MULTILINE | re.RegexFlag.DOTALL)
        self.solution_marker_regex = re.compile(r'{solution_start}{line_sep}?(.*?){solution_end}'
                                                .format(line_sep="\n",
                                                        solution_start=self.SOLUTION_MARKER[0],
                                                        solution_end=self.SOLUTION_MARKER[1]),
                                                re.RegexFlag.MULTILINE | re.RegexFlag.DOTALL)

    def _get_csharp_type_name(self, argument_type: ArgumentType):
        if argument_type == ArgumentType.STRING:
            return "string"
        elif argument_type == ArgumentType.INTEGER:
            return "int"
        elif argument_type == ArgumentType.ARRAY_STRING:
            return "string[]"
        elif argument_type == ArgumentType.ARRAY_INTEGER:
            return "int[]"
        else:
            raise ValueError("{} is not supported!".format(argument_type))

    def scaffold_function_declaration_argument_text(self, parameter: FunctionArgument):
        type_name = self._get_csharp_type_name(parameter.type)
        return "{} {}".format(type_name, parameter.name)

    def scaffold_code(self, function_: Function, scaffolding_type: ScaffoldingType) -> str:
        function_declaration = self.scaffold_function_declaration(function_)
        if scaffolding_type == ScaffoldingType.FUNCTION_ONLY:
            return function_declaration
        elif scaffolding_type == ScaffoldingType.FULL_TEMPLATE:
            return self.scaffold_program_template(function_declaration, function_)

        raise NotImplementedError("{} scaffolding type is not implemented yet!".format(scaffolding_type))

    def scaffold_function_declaration(self, function_):
        arguments_ = [self.scaffold_function_declaration_argument_text(arg) for arg in function_.arguments]
        res = "public static {return_type} {name}({parameters})\n{{\n    {comment_start}Write code here\n}}".format(
            return_type=self._get_csharp_type_name(function_.return_type),
            name=function_.name,
            comment_start=self.SINGLE_LINE_COMMENT_START,
            parameters=", ".join(arguments_))
        return res

    def scaffold_function_call(self, function: Function) -> str:
        res = "{name}()".format(name=function.name)
        return res

    def scaffold_program_template(self, function_declaration_code: str, function: Function):
        template = self.PROGRAM_TEMPLATE.format(return_type=self._get_csharp_type_name(function.return_type),
                                                target_function_call=self.scaffold_function_call(function),
                                                target_function_declaration=function_declaration_code)
        return template

    def prepare_execution_code_from_function_declaration(self, function_declaration: str, function: Function):
        full_code_template: str = function.code_snippets[0].code
        template_function_code = self.target_function_regex.findall(full_code_template)[0]
        result = full_code_template.replace(template_function_code, os.linesep + function_declaration + os.linesep)
        return result

    def remove_solution_part_from_code(self, solution_code: str):
        return self.solution_marker_regex.sub("{} write code here".format(
            self.SINGLE_LINE_COMMENT_START), solution_code)
