from logger.logger import ILogger
from models.repositories.generator_repository import GeneratorRepository
from services.code_executer_service import CodeExecuterService
from services.function_service import FunctionService
from services.instance_service import InstanceService
from services.run_service import RunService
from services.template_service import TemplateService
from services.testing_input_service import TestingInputService


class RepoResolver(object):
    def __init__(self,
                 generator_repo: GeneratorRepository
                 ):
        self.generator_repo = generator_repo
