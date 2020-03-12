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
        self.first_age_range = re.compile(r"(0\sa\s18)")
        self.age = re.compile(r"(anos)")
        self.value = re.compile(r"R\$\s(.+\d$)|((\d+.\d+\.\d+.+)|(\d+\.\d+.+)|(\d+\,\d+))")

        self.msg = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)")
        self.link = re.compile(r"(https:\/\/.*)")

        # self.desnecessary = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(https:\/\/.*)|(\d\/\d{1,2})|(Tabela :: Simulador Online)|(\d{2}\/\d{2}\/\d{4})|\(\d\d\)\W\d{4,5}\W\d{4,5}")
        self.desnecessary = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(https:\/\/.*)|(\d\/\d{1,2})|(Tabela :: Simulador Online)|(\d{2}\/\d{2}\/\d{4})")

        self.last_change = re.compile(r"(Última\sAlteração\W\s\d{2}\/\d{2}\/\d{2,4})")
        self.last_change_lb = re.compile(r"(Última Alteração: \d{2}\/\d{2}\/\d{2,4}\\n)")
        self.title_table = re.compile(r"(\w+\s\W\w+\W)")

    def get_data(self):
        if self.file:
            pdfs = [pdf for pdf in os.listdir(self.path) if pdf[-4:] == ".pdf"]
            return pdfs
        return [self.path]

    def get_last_index_change(self, text_splitted):
        for i in range(len(text_splitted)-1, 0, -1):
            if self.last_change.match(text_splitted[i]):
                return i

    def prepare_text(self, pdfs):
        prepaired_data = {}
        pdfs = self.get_data()
        need_path = True

        if len(pdfs) == 1 and self.file is False:
            need_path = False            

        for pdf in pdfs:
            if not need_path:
                pdf_name = pdf.split("/")[-1][:-4]
            else:
                pdf_name = pdf[:-4]
            
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

            all_text = []
            for i in range(len(new_text)):
                prepaired_text = []
                for j in range(len(new_text[i])):
                    if self.desnecessary.match(new_text[i][j]):
                        new_text[i][j] = ""
                    if new_text[i][j]!="":
                        prepaired_text.append(new_text[i][j])
                all_text.append(prepaired_text)

            final_text = []
            key = all_text[0][0][:-4]
            for i in range(len(all_text)):
                if all_text[i][0] == "Taxas" or "Elegibilidade" in all_text[i][0]:
                    for j in range(len(all_text[i])):
                        if key in all_text[i][j]:
                            final_text.append(all_text[i][j:])
                if all_text[i][1] == "Título" or all_text[i][1] == "Tipo" or all_text[i][0] == "Carência":
                    continue
                else:
                    final_text.append(all_text[i])
            prepaired_data[pdf_name] = final_text
        return prepaired_data

    def extract_info(self, prepaired_text):
        print(prepaired_text)
        exit()
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))))
        for pdf, text in prepaired_text.items():
            print(pdf)
            i = 0
            while i < len(text):
                j = 0
                while j < len(text[i]):
                    if self.phone.match(text[i][j]):
                       m1 = " ".join(text[i][:j])
                       del text[i][:j+1]
                    if self.title_table.match(text[i][j]): #formando as tabelas
                        if len(text[i][:j]) > 0: #contem informacao antes da tabela
                            if len(text[i][:j]) == 1:
                                m2 = text[i][:j][0]
                                m3 = ""
                                m4 = ""
                                del text[i][:j]                        
                            elif len(text[i][:j]) == 2:
                                m2 = text[i][:j][0]
                                m3 = text[i][:j][1]
                                m4 = ""
                                del text[i][:j]
                            elif len(text[i][:j]) == 3:
                                m2 = text[i][:j][0]
                                m3 = text[i][:j][1]
                                m4 = text[i][:j][2]
                                del text[i][:j]
                            elif len(text[i][:j]) == 4:
                                m2 = text[i][:j][0]
                                m3 = text[i][:j][1]
                                m4 = text[i][:j][2]
                                del text[i][:j]
                            m5 = text[i][0]
                            del text[i][0]
                            j = j-2
                        else:
                            m5 = text[i][j]
                            del text[i][j]
                        
                        try:
                            match_age_range = self.age_range.match(text[i][:j+1][0])
                        except IndexError:
                            break
                        
                        if match_age_range:
                            if match_age_range.string == "Faixa Etária":                        
                                while not self.first_age_range.match(text[i][j]):
                                    j += 1
                                m6 = text[i][1:j]
                                del text[i][1:j]
                            elif match_age_range.string == "Faixa":                            
                                while not self.first_age_range.match(text[i][j]):
                                    j += 1
                                m6 = text[i][2:j]
                                del text[i][2:j]
                        # del text[i][:j]
                        columns = []
                        state = 1
                        
                        if len(m6) == 1:
                            columns.append(m6[0])

                        elif len(m6) > 1:
                            if state == 1:
                                for k in range(len(m6)):
                                    if m2.upper() in m6[k].upper():
                                        state = 2
                                        break
                                    columns.append(m6[k])
                            if state == 2:
                                for k in range(len(m6)):
                                    splited = m6[k].split(" ")
                                    if len(splited) > 1:
                                        if m6[k].split(" ")[1].upper() == m2.upper():
                                            columns.append(m6[k] + " " + m6[k+1])                                
                                        elif m6[k].split(" ")[0].upper() == m2.upper():
                                            joined_text = m6[k-1] + " " + m6[k] + " " + m6[k+1]
                                            columns.append(joined_text)
                        values = []                                           
                        for value in text[i][1:]:
                            match_value = self.value.match(value)
                            if match_value:
                                # v = "R$ " + match_value[1]
                                values.append(v)
                        for n in range(len(columns)):
                            data[pdf][i][(m1, m2, m3, m4)][m5][columns[n]] = list(itertools.islice(values, n, len(values), len(columns)))
                    j += 1
                i += 1
        return data
            