class Config:
    _tmp_path = "e:\_TMP_"

    def __init__(self):
        pass

    @property
    def tmp_folder_path(self):
        # type: ()-> str
        return self._tmp_path
