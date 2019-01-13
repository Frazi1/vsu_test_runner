from marshmallow import Schema, fields, post_load

from src.models.TestQuestionTemplate import TestQuestionTemplate
from src.models.TestTemplate import TestTemplate


class TestQuestionTemplateSchema(Schema):
    name = fields.String()
    description = fields.Str()
    time_limit = fields.Integer(data_key='timeLimit', attribute='time_limit')

    @post_load
    def load(self, value):
        return TestQuestionTemplate(**value)


class TestTemplateSchema(Schema):
    id = fields.Integer(required=False, allow_none=True)
    name = fields.String()
    time_limit = fields.Integer(data_key='timeLimit', attribute='time_limit')
    questions = fields.Nested(TestQuestionTemplateSchema, data_key='questionTemplates', many=True, required=False, allow_none=True)

    @post_load
    def fuck_my_fucking_life_bitches(self, value):
        print "DESERIALIZATION!!!"
        print value
        return TestTemplate(**value)
