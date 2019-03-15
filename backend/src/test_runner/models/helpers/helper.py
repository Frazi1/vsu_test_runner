from models.code_snippet import CodeSnippet
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput
from models.function_parameter import FunctionArgument
from utils.business_error import BusinessException


def clone_code_snippet(code_snippet: CodeSnippet) -> CodeSnippet:

    if isinstance(code_snippet.function.testing_input, DeclarativeFunctionInput):
        testing_input_clone = DeclarativeFunctionInput(items=code_snippet.function.testing_input.items)
    else:
        raise BusinessException("Only DeclarativeFunctionInput is supported")

    func_clone = Function(id=None, name=code_snippet.function.name,
                          return_type=code_snippet.function.return_type,
                          arguments=[FunctionArgument(type=x.type, name=x.name) for x in
                                     code_snippet.function.arguments],
                          testing_input=testing_input_clone)
    snippet_clone = CodeSnippet(language=code_snippet.language,
                                code=code_snippet.code,
                                function=func_clone)

    return snippet_clone
