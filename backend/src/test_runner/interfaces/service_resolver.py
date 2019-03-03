from logger.logger import ILogger
from services.code_executer_service import CodeExecuterService
from services.function_service import FunctionService
from services.instance_service import InstanceService
from services.run_service import RunService
from services.template_service import TemplateService


class ServiceResolver(object):
    def __init__(self,
                 logger,  # type: ILogger
                 code_executer_service,  # type: CodeExecuterService
                 function_service,  # type: FunctionService
                 instance_service,  # type: InstanceService
                 run_service,  # type: RunService
                 template_service  # type: TemplateService
                 ):
        self.code_executer_service = code_executer_service
        self.function_service = function_service
        self.instance_service = instance_service
        self.run_service = run_service
        self.template_service = template_service
        self.logger = logger
