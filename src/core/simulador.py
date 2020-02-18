import textract
import platform
import os
import re

SYSTEM = platform.system()
months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]


class Simulador:
    def __init__(self, path):
        self.path = path
        self.file = os.path.isdir(path)
        self.phone = re.compile(r"\(\d\d\)\W\d{4,5}\W\d{4,5}")

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
            m2 = ''
            m5 = ''
            m6 = ''
            v1 = ''
            v2 = ''
            v3 = ''
            v4 = ''
            v5 = ''
            v6 = ''
            v7 = ''
            v8 = ''
            v9 = ''
            v10 = ''

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
                elif state == 2:
                    m2 = text_splitted[i]
                    state = 3
                elif state == 3:
                    m3 = text_splitted[i]
                    for month in months:
                        if month in text_splitted[i]:
                            m3 = ''
                            break
                    state = 4
                elif state == 4:
                    m4 = text_splitted[i]
                    for month in months:
                        if month in text_splitted[i]:
                            m4 = ''
                            break                    
                    state = 5                                       

            print("M1: ",m1)
            print("M2: ",m2)
            print("M3: ",m3)
            print("M4: ",m4)
            print("-"*30)




