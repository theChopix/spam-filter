import os


class Corpus:
    def __init__(self, path):
        self.path = path

    def emails(self):
        filenames = os.listdir(self.path)

        for filename in filenames:
            # files whose name don't start with '_' or '!' are email files
            if filename[0] != "_" and filename[0] != "!":
                with open(self.path + "/" + filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    yield filename.strip('.txt'), content
