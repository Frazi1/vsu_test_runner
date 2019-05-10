from utils.business_error import BusinessException


def is_not_none(value, param_name):
    if value is None:
        raise BusinessException("{} should not be None!".format(param_name))
