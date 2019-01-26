from marshmallow import Schema, fields, post_load
from marshmallow.fields import Nested, String, Integer

from models.test_question_template import TestQuestionTemplate
from models.test_template import TestTemplate


class TestQuestionTemplateSchema(Schema):
    id = String(required=False, allow_none=True)
    name = String(required=False)
    description = String(required=False)
    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         required=False,
                         allow_none=True)

    @post_load
    def create_class(self, value):
        return TestQuestionTemplate(**value)


class TestTemplateSchema(Schema):
    id = fields.Integer(required=False, allow_none=True)
    name = fields.String()
    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         allow_none=True)
    # many = False, required = False, allow_none = True
    questions = Nested(TestQuestionTemplateSchema,
                       load_from='questionTemplates',
                       dump_to='questionTemplates',
                       attribute='questions',
                       many=True)

    @post_load
    def create_class(self, value):
        return TestTemplate(**value)
