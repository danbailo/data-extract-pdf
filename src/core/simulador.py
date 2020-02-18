import textract
import platform
import os
import re

SYSTEM = platform.system()

class Simulador:
    def __init__(self, path):
        self.path = path
        self.file = os.path.isdir(path)

    def get_data(self):
        if self.file:
            pdfs = [pdf for pdf in os.listdir(self.path) if pdf[-4:] == ".pdf"]
            return pdfs
        return [self.path]

    def get_text(self):
        pdfs = self.get_data()
        need_path = False
        if len(pdfs) != 1:
            need_path = True

        for pdf in pdfs:
            if need_path:
                text = textract.process(os.path.join(self.path, pdf))
            else:
                text = textract.process(pdf)
            
            text_splitted = text.decode("utf-8").replace('\xa0', '\n').split("\n")

            if SYSTEM == "Windows":
                text_splitted = [re.sub(pattern=r"\r", repl="", string=t) for t in text_splitted]             

            for empty in text_splitted:
                if empty == '': text_splitted.remove(empty)
            
            print(text_splitted)



