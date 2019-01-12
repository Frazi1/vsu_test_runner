class TestTemplateDto:
    @staticmethod
    def list_of(test_templates):
        return [TestTemplateDto(x) for x in test_templates]

    def __init__(self, test_template):
        self.name = test_template.name
        self.time_limit = test_template.time_limit
        self.questions = [TestQuestionTemplateDto(x) for x in test_template.questions]


class TestQuestionTemplateDto:
    def __init__(self, test_template_question):
        self.name = test_template_question.name
        self.description = test_template_question.description
        self.time_limit = test_template_question.time_limit


class CodeRunResult:
    def __init__(self, language, output, output_type, error=None):
        self.language = language
        self.output = output
        self.output_type = output
        self.error = error
