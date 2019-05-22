import shutil
import os
from typing import Optional

from app_config import Config
from coderunner.csharp.csharp_runner import CSharpRunner
from coderunner.file_run_result import FileRunResult


class CSharpDockerRunner(CSharpRunner):

    def __init__(self, config: Config, docker_client):
        super().__init__(config)
        self.docker_client = docker_client

    def _prepare_docker_file(self, container_folder, executable_name):
        docker_file_path = self.config.DOCKER["Templates"]["ExecutableDockerFileTemplatePath"]
        with open(docker_file_path, "r") as docker_file:
            docker_file_text = docker_file.read()

        docker_file_text = docker_file_text.replace("%EXE_NAME%", executable_name)
        with open(os.path.join(container_folder, self.config.docker_file_name), "x") as prepared_docker_file:
            prepared_docker_file.write(docker_file_text)

    def _build_docker_image(self, container_folder):
        image = self.docker_client.images.build(path=container_folder)
        return image

    def _prepare_for_execution(self, exe_file_path) -> str:
        paths = exe_file_path.split("\\")
        container_folder = "\\".join(paths[:-1])
        exe_file_name = paths[-1]
        self._prepare_docker_file(container_folder, exe_file_name)
        image = self._build_docker_image(container_folder)
        image_id = image[0].id
        return image_id

    def _execute_file(self, image_id: str, input: Optional[str]) -> FileRunResult:
        container = self.docker_client.api.create_container(image_id, stdin_open=True)
        self.docker_client.api.start(container)
        output = self.docker_client.api.attach_socket(container, params={'stdout': 1, 'stream': 1})
        if input is not None:
            sock = self.docker_client.api.attach_socket(container, params={'stdin': 1, 'stream': 1})
            sock.send(input.encode('utf-8'))
            sock.close()

        buf = bytes()
        while True:
            bytes_ = output.recv(bufsize=512)
            buf += bytes_
            if len(bytes_) == 0:
                break

        output.close()
        self.docker_client.api.stop(container)
        self.docker_client.api.wait(container)
        self.docker_client.api.remove_container(container)

        text = buf.decode('utf-8')
        return FileRunResult(input, text, None)
