import os
import random
import string
import zipfile
from decorators.singleton import singleton


@singleton
class FileSystem:

    def __init__(self) -> None:
        self.rootPath = os.path.join(os.path.dirname(__file__))
        while "app.py" not in os.listdir(self.rootPath):
            self.rootPath = os.path.dirname(self.rootPath)
        os.makedirs(os.path.join(self.rootPath, "temp"), exist_ok=True)
        self.tempPath = os.path.join(self.rootPath, "temp")

    def allowed_file(self, filename, allowedExtensions):
        return (
            "." in filename and '.'+filename.rsplit(".", 1)[1].lower() in allowedExtensions
        )

    def random_file_name(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def generate_random_directory(self):
        randName = self.random_file_name(10)
        randFilePath = os.path.join(self.tempPath, randName)
        os.mkdir(randFilePath)
        return randName, randFilePath
    
    def extract_zip_file(self,zip_file_path, extract_to_directory):
        if not os.path.exists(extract_to_directory):
            os.makedirs(extract_to_directory)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)

    def traverse_directory(self, root, levels=1):
        if levels == 0:
            return None

        tree = {}

        try:
            for entry in os.scandir(root):
                if entry.is_dir(follow_symlinks=False):
                    tree[entry.name] = self.traverse_directory(entry.path, levels - 1)
                else:
                    tree[entry.name] = None
        except Exception as e:
            print(e)
            return {"error": "Permission denied"}

        return tree

    def generate_files(self, project):
        randName, directory_path = self.generate_random_directory()

        def generate_files_recursive(path, project):
            for name, content in project.items():
                if isinstance(content, dict):
                    os.makedirs(os.path.join(path, name), exist_ok=True)
                    generate_files_recursive(os.path.join(path, name), content)
                else:
                    with open(os.path.join(path, name), "w") as file:
                        file.write(content)

        generate_files_recursive(directory_path, project)

        return randName, directory_path
