from src.shared.ValueConverter import ValueConverter


class ValueRepresentation:
    def __init__(self, type_, parsed_value):
        self.type = type_
        self.parsed_value = parsed_value
        self.raw_value = ValueConverter.to_string(type_, parsed_value)

    @classmethod
    def from_dict(cls, dict_):
        type_ = dict_.type
        raw_value = dict_.value

        cls_ = cls(type_, ValueConverter.from_string(type_, raw_value))
        cls.raw_value = raw_value
        return cls_

    @classmethod
    def from_raw(cls, type_, raw_value):
        cls_ = cls(type_, ValueConverter.from_string(type_, raw_value))
        cls_.raw_value = raw_value
        return cls_

    def __repr__(self):
        return "<ValueRepresentation - type:{} parsed_value:{} raw_value:{}".format(self.type,
                                                                                    self.parsed_value,
                                                                                    self.raw_value)