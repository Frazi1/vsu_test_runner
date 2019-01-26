class TestTemplateDto:
    @staticmethod
    def list_of(test_templates):
        return [TestTemplateDto.from_test(x) for x in test_templates]

    @classmethod
    def from_test(cls, test_template):
        res = cls()
        res.id = test_template.id
        res.name = test_template.name
        res.time_limit = test_template.time_limit
        res.questions = [TestQuestionTemplateDto.from_test(x) for x in test_template.questions]
        return res

class TestQuestionTemplateDto:
    @classmethod
    def from_test(cls, test_template_question):
        res = cls()
        res.id = test_template_question.id
        res.name = test_template_question.name
        res.description = test_template_question.description
        res.time_limit = test_template_question.time_limit
        return res


class CodeRunResult:
    def __init__(self, language, output, output_type, error=None):
        self.language = language
        self.output = output
        self.output_type = output
        self.error = error
