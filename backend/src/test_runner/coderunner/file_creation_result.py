class FileCreationResult(object):
    def __init__(self, file_name, file_ext, created_file_abs_path, created_folder_abs_path):
        self.file_name = file_name
        self.file_ext = file_ext
        self.created_file_abs_path = created_file_abs_path
        self.created_folder_abs_path = created_folder_abs_path

    @property
    def file_name_and_ext(self):
        return self.file_name + self.file_ext
