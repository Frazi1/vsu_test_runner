from marshmallow import Schema, post_load
from marshmallow.fields import Integer, String, Nested, List, DateTime

from dtos import TestRunDto, TestRunQuestionAnswerDto
from schemas import CodeSnippetSchema


class TestRunQuestionSchema(Schema):
    id = Integer()
    name = String(required=True)
    description = String(required=True)
    answer_code_snippet = Nested(CodeSnippetSchema,
                                 dump_to='answerCodeSnippet',
                                 load_from='answerCodeSnippet')

    @post_load()
    def create_class(self, value):
        return TestRunQuestionAnswerDto(**value)


class TestRunSchema(Schema):
    id = Integer()
    name = String(required=True)
    started_at = DateTime(dump_to='startedAt',
                          load_from='startedAt')

    ends_at = DateTime(dump_to='endsAt',
                       load_from='endsAt')

    finished_at = DateTime(required=False,
                           allow_none=True,
                           dump_to='finishedAt',
                           load_from='finishedAt')

    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         required=False,
                         allow_none=True)

    question_answers = List(Nested(TestRunQuestionSchema),
                            dump_to='questionAnswers',
                            load_from='questionAnswers')

    @post_load
    def create_class(self, value):
        return TestRunDto(**value)
