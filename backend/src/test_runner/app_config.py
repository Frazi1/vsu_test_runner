import os
import enum

class ContainerType(enum.Enum):
    Native = 1
    Docker = 2

class Config:
    _tmp_path = "e:\_TMP_"
    _python_default_template_path = ".\coderunner\\templates\python_process_template.py"

    _csharp_compiler_path = "C:\Program Files (x86)\Microsoft Visual " \
                            "Studio\\2017\Community\MSBuild\\15.0\Bin\Roslyn\csc.exe"

    _docker_path = "..\\..\\..\\docker"
    docker_file_name = "DOCKERFILE"
    DOCKER = {
        "Templates": {
            "ExecutableDockerFileTemplatePath": os.path.join(_docker_path, "executable_tpl", docker_file_name)
        }
    }

    CONTAINER_TYPE = ContainerType.Docker

    def __init__(self):
        pass

    @property
    def tmp_folder_path(self):
        # type: ()-> str
        return self._tmp_path

    @property
    def python_default_template_path(self):
        return self._python_default_template_path

    @property
    def csharp_compiler_path(self):
        return self._csharp_compiler_path
