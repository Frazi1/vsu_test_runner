from models.Function import Function
from models.code_snippet import CodeSnippet
from models.function_parameter import FunctionArgument


def clone_code_snippet(code_snippet):
    func_clone = Function(name=code_snippet.function.name,
                          return_type=code_snippet.function.return_type,
                          arguments=[FunctionArgument(type=x.type, name=x.name) for x in
                                     code_snippet.function.arguments])
    snippet_clone = CodeSnippet(language=code_snippet.language,
                                code=code_snippet.code,
                                function=func_clone)

    return snippet_clone
