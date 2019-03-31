from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.scaffolding_type import ScaffoldingType
from models.argument_type import ArgumentType
from models.function import Function
from models.function_parameter import FunctionArgument


class CSharpCodeGenerator(BaseCodeGenerator):
    SINGLE_LINE_COMMENT_START = "//"

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

    def scaffold_function_declaration_text(self, function_: Function, scaffolding_type: ScaffoldingType) -> str:
        if scaffolding_type == ScaffoldingType.FUNCTION_ONLY:
            arguments_ = [self.scaffold_function_declaration_argument_text(arg) for arg in function_.arguments]
            res = "public static {return_type} {name}({parameters})\n{{\n    {comment_start}Write code here\n}}".format(
                return_type=self._get_csharp_type_name(function_.return_type),
                name=function_.name,
                comment_start=self.SINGLE_LINE_COMMENT_START,
                parameters=", ".join(arguments_))
            return res

        raise NotImplementedError("{} scaffolding type is not implemented yet!".format(scaffolding_type))
