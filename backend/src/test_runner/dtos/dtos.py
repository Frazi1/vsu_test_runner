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


class TestRunQuestionAnswerDto:
    def __init__(self, id, name, description, answer_code_snippet):
        self.id = id
        self.name = name
        self.description = description
        self.answer_code_snippet = answer_code_snippet

    @classmethod
    def map_from(cls, question_answer):
        cls_ = cls(id=question_answer.id,
                   name=question_answer.question_instance.name,
                   description=question_answer.question_instance.description,
                   answer_code_snippet=question_answer.code_snippet)
        return cls_


class TestRunDto:
    def __init__(self, id, started_at, ends_at, finished_at, question_answers):
        self.id = id
        self.started_at = started_at
        self.ends_at = ends_at
        self.finished_at = finished_at
        self.question_answers = question_answers

    @classmethod
    def map_from(cls, test_run):
        cls_ = cls(id=test_run.id,
                   started_at=test_run.started_at,
                   ends_at=test_run.ends_at,
                   finished_at=test_run.finished_at,
                   question_answers=[TestRunQuestionAnswerDto.map_from(x) for x in test_run.question_answers])
        return cls_
    
    
class TestInstanceUpdate:
    def __init__(self, available_after, disabled_after, time_limit):
        self.available_after = available_after
        self.disabled_after = disabled_after
        self.time_limit = time_limit
