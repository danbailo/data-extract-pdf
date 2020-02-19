import textract
import platform
import os
import re
from collections import defaultdict

SYSTEM = platform.system()
months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]


class Simulador:
    def __init__(self, path):
        self.path = path
        self.file = os.path.isdir(path)
        self.phone = re.compile(r"\(\d\d\)\W\d{4,5}\W\d{4,5}")
        self.years = re.compile(r"anos")
        self.age_range = re.compile(r"(Faixa Etária)|(Faixa)")
        self.age = re.compile(r"(anos)")
        self.value = re.compile(r"R\$\s(.+\d$)|((\d+.\d+\.\d+.+)|(\d+\.\d+.+)|(\d+\,\d+))")
        

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
            
            m1 = ''
            table = []
            tables = defaultdict(lambda: defaultdict(list))
            n = 0
            indexes = []
            symbols = []

            if need_path:
                text = textract.process(os.path.join(self.path, pdf))
            else:
                text = textract.process(pdf)
            
            text_splitted = text.decode("utf-8").replace('\xa0', '\n').split("\n")

            if SYSTEM == "Windows":
                text_splitted = [re.sub(pattern=r"\r", repl="", string=t) for t in text_splitted]             

            for empty in text_splitted:
                if empty == '': text_splitted.remove(empty)
            
            text_splitted = text_splitted[2:]

            state = 1

            for i in range(len(text_splitted)):
                if state == 1:
                    match_phone = self.phone.match(text_splitted[i])
                    if match_phone:
                        state = 2
                    else:
                        m1 = m1 + text_splitted[i] + " "
                
                match_age_range = self.age_range.match(text_splitted[i])

                if match_age_range:
                    if match_age_range.string == "Faixa Etária":
                        k = 1
                        m = 1
                        while not re.match(r"0.+", text_splitted[i+k]):
                            print(text_splitted[i+k])
                            k += 1
                        print()
                    if match_age_range.string == "Faixa":
                        while not re.match(r"0.+", text_splitted[i+m]):
                            if text_splitted[i+m] == "Etária":
                                m += 1
                                continue
                            print(text_splitted[i+m])
                            m += 1                     

#                    tables[text_splitted[i-1]][].append()
                
                match_value = self.value.match(text_splitted[i])
                if match_value:
                    pass
                    #print(re.sub(r"R\$ ", "", match_value.string))

            print("M1: ",m1)
            print("tables: ",tables)

            # print("M4: ",m4)
            # print("M5: ",m5)
            # print("M6: ",m6)
            print("-"*30)




