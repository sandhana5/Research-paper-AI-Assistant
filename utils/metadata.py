import json
import hashlib
import os


class MetadataManager:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        self.file = "data/indexed_files.json"

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump({}, f)

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def get_file_hash(self, pdf_path):

        with open(pdf_path, "rb") as f:

            file_bytes = f.read()

        return hashlib.md5(file_bytes).hexdigest()

    def already_indexed(self, pdf_path):

        data = self.load()

        file_hash = self.get_file_hash(pdf_path)

        return file_hash in data

    def add_file(self, pdf_path):

        data = self.load()

        file_hash = self.get_file_hash(pdf_path)

        data[file_hash] = {

            "filename": os.path.basename(pdf_path)

        }

        self.save(data)