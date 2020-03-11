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

        self.desnecessary = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(https:\/\/.*)|(\d\/\d{1,2})|(Tabela :: Simulador Online)|(\d{2}\/\d{2}\/\d{4})")

        self.last_change = re.compile(r"(Última\sAlteração\W\s\d{2}\/\d{2}\/\d{2,4})")
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
            
            text_splitted = text.decode("utf-8").replace('\xa0', '\n').split("\n")
            text_splitted = [re.sub(pattern=r"\x0c", repl="", string=t) for t in text_splitted]             

            if SYSTEM == "Windows":
                text_splitted = [re.sub(pattern=r"\r", repl="", string=t) for t in text_splitted]             

            for i, desnecessary in enumerate(text_splitted):
                match_desnecesary = self.desnecessary.match(desnecessary)
                if match_desnecesary:
                    exclude_values.add(i)
                if desnecessary == "":
                    exclude_values.add(i)

            exclude_values = list(exclude_values)

            text_splitted = delete(text_splitted, exclude_values).tolist()

            last_index = self.get_last_index_change(text_splitted)
            text_splitted = text_splitted[:last_index]

            key = text_splitted[0].split(" ")[0]

            for i in range(len(text_splitted)):
                if text_splitted[i]=="Taxas":
                    index_initial = i
                if key in text_splitted[i]:
                    index_final = i - 1

            del text_splitted[index_initial:index_final]

            headers = {}
            values = []
            is_table = False
            is_info = True
            n_table = 1
            tables = {}
            tables
            i = 0
            while len(text_splitted) != 0:

                phone_match = self.phone.match(text_splitted[i])
                if phone_match:
                    m1 = " ".join(text_splitted[:i])
                    del text_splitted[:i+1]
                age_range_match = self.age_range.match(text_splitted[i])                
                if age_range_match:
                    if len(text_splitted[:i-1]) == 1:
                        m2 = text_splitted[:i-1]
                        m3, m4 = "", ""
                        del text_splitted[:i-1]

                    elif len(text_splitted[:i-1]) == 2:
                        m2, m3 = text_splitted[:i-1]
                        m4 = ""
                        del text_splitted[:i-1]

                    elif len(text_splitted[:i-1]) == 3:
                        m2, m3, m4 = text_splitted[:i-1]
                        del text_splitted[:i-1]
                    
                    tables[(pdf_name[:-4],m1,m2,m3,m4)] = {}
                    # m5 = text_splitted[0]
                    # del text_splitted[:i-1]
                
                # last_change_match = self.last_change.match(text_splitted[i])
                # if last_change_match:
                #     title_table = self.title_table.match(text_splitted[0])
                #     if title_table:
                #         is_table = True
                #         is_info = False
                #         m5 = text_splitted[0]
                #         del text_splitted[0]
                #         tables[(pdf_name[:-4],m1,m2,m3,m4)][m5] = {}
                first_age_range_match = self.first_age_range.match(text_splitted[i])
                if first_age_range_match:
                    m5 = text_splitted[0]
                    del text_splitted[0]
                    tables[(pdf_name[:-4],m1,m2,m3,m4)][m5] = {}
                    i -= 1
                    for column in text_splitted[:i]:
                        if not self.age_range.match(column):
                            m6 = column
                            tables[(pdf_name[:-4],m1,m2,m3,m4)][m5][m6] = []
                    del text_splitted[:i]
                last_change_match = self.last_change.match(text_splitted[i])
                if last_change_match:
                    for value in text_splitted[:i]:
                        if self.value.match(value):
                            # tables[(pdf_name[:-4],m1,m2,m3,m4)][m5][m6].append(value)
                            values.append(value)
                    del text_splitted[:i]
                print(text_splitted)
                i += 1

            exit()


##############################################################################################################################

            state = 1
            first_page = True

            update_values = True
            for i in range(len(text_splitted)):
                if i == last_index:
                    update_values = False

                last_change = self.last_change.match(text_splitted[i])           

                if first_page: #primeira tabela antes do "Última Alteração: xx/xx/xxxx"                    
                    if state == 1:
                        match_phone = self.phone.match(text_splitted[i])
                        if match_phone:
                            state = 2
                            m2 = text_splitted[i+1]
                            m3 = text_splitted[i+2]
                            m4 = text_splitted[i+3]
                            if self.msg.match(m3):
                                m3 = ""
                            if self.msg.match(m4):
                                m4 = ""                            
                            headers[str(n_2*-1)] = (m1,m2,m3,m4)
                            n_2 += 1
                            #print(str(n*-1), (m1,m2,m3,m4))

                        else:
                            m1 = m1 + text_splitted[i] + " "

                    match_age_range = self.age_range.match(text_splitted[i])

                    if match_age_range:
                        if match_age_range.string == "Faixa Etária":
                            k = 1
                            m = 1
                            while not re.match(r"0.+", text_splitted[i+k]):                            
                                tables[n][text_splitted[i-1]][text_splitted[i+k]] = []
                                # n += 1
                                k += 1
                        if match_age_range.string == "Faixa":
                            while not re.match(r"0.+", text_splitted[i+m]):
                                if text_splitted[i+m] == "Etária":
                                    m += 1
                                    continue
                                tables[n][text_splitted[i-1]][text_splitted[i+m]] = []
                                # n += 1
                                m += 1
                        if m3 == text_splitted[i-1]:
                            m3 = ""                              
                        if m4 == text_splitted[i-1]:
                            m4 = ""
                        
                
                    match_value = self.value.match(text_splitted[i])
                    if match_value:
                        new_value = match_value.string
                        if new_value[:3] != "R$ ":
                            new_value = "R$ " + match_value.string
                        values.append(new_value)

                    if last_change:
                        index = i                    
                        first_page = False
                                       
                else: # tabelas apos a primeira ocorrendia do "Última Alteração: xx/xx/xxxx"
                    last_change = self.last_change.match(text_splitted[index])
                    title_table = self.title_table.match(text_splitted[index])
                    if update_values:                    
                        if last_change:
                            after_last_change = self.title_table.match(text_splitted[index+1])
                            if not after_last_change:
                                m2 = text_splitted[index+1]
                                m3 = text_splitted[index+2]
                                m4 = text_splitted[index+3]
                                #print((m1,m2,m3,m4))
                                headers[str(n_2*-1)] = (m1,m2,m3,m4)
                                n_2 += 1
                        if title_table:
                            # headers[str(n*-1)] = (m1,m2,m3,m4)
                            index_title_table = index + 1

                            match_age_range = self.age_range.match(text_splitted[index_title_table])

                            if match_age_range:
                                if match_age_range.string == "Faixa Etária":
                                    k = 1
                                    while not re.match(r"0.+", text_splitted[index_title_table+k]):
                                        sub_table = text_splitted[index_title_table+k]
                                        tables[n][title_table.string][sub_table] = []
                                        k += 1
                                elif match_age_range.string == "Faixa":
                                    l = 2
                                    while not re.match(r"0.+", text_splitted[index_title_table+l]):                                
                                        if text_splitted[index_title_table+l].split(" ")[-1].upper() == m2.upper():
                                            sub_table = text_splitted[index_title_table+l] + " " + text_splitted[index_title_table+l+1]
                                        elif text_splitted[index_title_table+l+1].split(" ")[0].upper() == m2.upper():
                                            sub_table = text_splitted[index_title_table+l] + " " + text_splitted[index_title_table+l+1] + " " + text_splitted[index_title_table+l+2]
                                        tables[n][title_table.string][sub_table] = []                                                                                         
                                        l += 1
                                    n += 1                         
                    
                    match_value = self.value.match(text_splitted[index])
                    if match_value:
                        new_value = match_value.string
                        if new_value[:3] != "R$ ":
                            new_value = "R$ " + match_value.string
                        values.append(new_value)
                    index += 1
                    
            for n_table in tables: #insercao dos valores nas tabelas
                for class_ in tables[n_table]:
                    n_symbols = len(tables[n_table][class_])
                    len_table = n_symbols * 10
                    
                    values_of_table = values[:len_table].copy()
                    del values[:len_table]

                    for symbol, row in zip(tables[n_table][class_], range(n_symbols)):                        
                        tables[n_table][class_][symbol] = list(itertools.islice(values_of_table, row, len_table, n_symbols))

            print(json.dumps(tables, indent=4, ensure_ascii=False))

            headers.update(tables)

            self.data[pdf] = list(headers.values())

