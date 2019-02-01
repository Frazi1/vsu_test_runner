from marshmallow import Schema, post_load
from marshmallow.fields import *

from models.question_instance import QuestionInstance
from models.test_instance import TestInstance


class TestQuestionSchema(Schema):
    id = Integer(required=False, allow_none=True)
    name = String(required=True)

    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         required=False,
                         allow_none=True)

    tests = Nested('TestInstanceSchema',
                   required=False,
                   allow_none=True,
                   many=True,
                   load_from='tests',
                   dump_to='tests')

    @post_load()
    def create_class(self, value):
        return QuestionInstance(**value)


class TestInstanceSchema(Schema):
    id = Integer(required=False, allow_none=True)
    name = String(required=True)
    created_at = DateTime(required=True,
                          load_from='createdAt',
                          dump_to='createdAt')

    available_after = DateTime(required=False,
                               allow_none=True,
                               load_from='availableAfter',
                               dump_to='availableAfter')

    disabled_after = DateTime(required=False,
                              allow_none=True,
                              load_from='disabledAfter',
                              dump_to='disabledAfter')

    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         required=False,
                         allow_none=True)

    questions = Nested(TestQuestionSchema(exclude=('tests',)),
                       required=False,
                       allow_none=True,
                       many=True,
                       load_from='questions',
                       dump_to='questions')

    @post_load()
    def create_class(self, value):
        return TestInstance(**value)
