from collections import defaultdict
import itertools
import textract
import platform
import json
import os
import re
from numpy import delete

SYSTEM = platform.system()

class Simulador:
    def __init__(self, path):
        self.path = path
        self.file = os.path.isdir(path)

        #patterns
        self.phone = re.compile(r"\(\d\d\)\W\d{4,5}\W\d{4,5}")
        self.years = re.compile(r"anos")
        self.age_range = re.compile(r"(Faixa Etária)|(Faixa)")
        self.first_age_range = re.compile(r"(0\sa\s18).+")
        self.age = re.compile(r"(anos)")
        self.value = re.compile(r"R\$\s(.+\d$)|((\d+.\d+\.\d+.+)|(\d+\.\d+.+)|(\d+\,\d+))")

        self.msg = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)")
        self.link = re.compile(r"(https:\/\/.*)")

        # self.desnecessary = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(https:\/\/.*)|(\d\/\d{1,2})|(Tabela :: Simulador Online)|(\d{2}\/\d{2}\/\d{4})|\(\d\d\)\W\d{4,5}\W\d{4,5}")
        self.desnecessary = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(https:\/\/.*)|(\d\/\d{1,2})|(Tabela :: Simulador Online)|(\d{2}\/\d{2}\/\d{4})")

        self.last_change = re.compile(r"(Última\sAlteração\W\s\d{2}\/\d{2}\/\d{2,4})")
        self.last_change_lb = re.compile(r"(Última Alteração: \d{2}\/\d{2}\/\d{2,4}\\n)")
        self.title_table = re.compile(r"(\w+\s\W\w+\W)")

        self.data = {}
        

    def get_data(self):
        if self.file:
            pdfs = [pdf for pdf in os.listdir(self.path) if pdf[-4:] == ".pdf"]
            return pdfs
        return [self.path]

    def get_last_index_change(self, text_splitted):
        for i in range(len(text_splitted)-1, 0, -1):
            if self.last_change.match(text_splitted[i]):
                return i


    def get_text(self, pdfs):
        pdfs = self.get_data()
        need_path = True

        if len(pdfs) == 1 and self.file is False:
            need_path = False            

        for pdf in pdfs:
            if not need_path:
                pdf_name = pdf.split("/")[-1]

            exclude_values = set()

            if need_path:
                text = textract.process(os.path.join(self.path, pdf))
            else:
                text = textract.process(pdf)
            
            text = text.decode("utf-8").replace('\xa0', '\n')
            text = text.replace('\x0c', '\n')
            
            text_splitted = re.split(r"(Última\sAlteração\W\s\d{2}\/\d{2}\/\d{2,4})", text)


            for t in text_splitted:
                if self.last_change.match(t):
                    text_splitted.remove(t)

            new_text = []
            for i in range(len(text_splitted)):
                new_text.append(text_splitted[i].split("\n"))

            final_text = []
            for i in range(len(new_text)):
                prepaired_text = []
                for j in range(len(new_text[i])):
                    if self.desnecessary.match(new_text[i][j]):
                        new_text[i][j] = ""
                    if new_text[i][j]!="":
                        prepaired_text.append(new_text[i][j])
                final_text.append(prepaired_text)

            print(final_text)

            exit()
