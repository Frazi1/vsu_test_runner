class Config:
    _tmp_path = "e:\_TMP_"
    _python_default_template_path = ".\coderunner\\templates\python_process_template.py"

    def __init__(self):
        pass

    @property
    def tmp_folder_path(self):
        # type: ()-> str
        return self._tmp_path

    @property
    def python_default_template_path(self):
        return self._python_default_template_path
