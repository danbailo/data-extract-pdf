from collections import defaultdict
import itertools
import textract
import platform
import json
import os
import re

SYSTEM = platform.system()

class Simulador:
    def __init__(self, path):
        self.path = path
        self.file = os.path.isdir(path)

        #patterns
        self.phone = re.compile(r"\(\d\d\)\W\d{4,5}\W\d{4,5}")
        self.years = re.compile(r"anos")
        self.age_range = re.compile(r"(Faixa Etária)|(Faixa)")
        self.age = re.compile(r"(anos)")
        self.value = re.compile(r"R\$\s(.+\d$)|((\d+.\d+\.\d+.+)|(\d+\.\d+.+)|(\d+\,\d+))")
        self.msg = re.compile(r"(Tabela\sde\s\d+\sà\s\d+\svidas\/beneficiários)|(Faixa Etária)")

        self.last_change = re.compile(r"(Última\sAlteração\W\s\d{2}\/\d{2}\/\d{2,4})")
        self.title_table = re.compile(r"(\w+\s\W\w+\W)")

        self.data = {}
        

    def get_data(self):
        if self.file:
            pdfs = [pdf for pdf in os.listdir(self.path) if pdf[-4:] == ".pdf"]
            return pdfs
        return [self.path]

    def get_text(self):
        pdfs = self.get_data()
        need_path = True

        if len(pdfs) == 1 and self.file is False:
            need_path = False

        for pdf in pdfs:
            
            m1 = ''
            tables = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
            n = 1
            n_other_pages = 1
            values = []

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
            first_page = True
            for i in range(len(text_splitted)):

                #title_table = self.title_table.match(text_splitted[i])
                last_change = self.last_change.match(text_splitted[i])

                if first_page: #primeira tabela antes do "Última Alteração: xx/xx/xxxx"                    
                    if state == 1:
                        match_phone = self.phone.match(text_splitted[i])
                        if match_phone:
                            state = 2
                            m2 = text_splitted[i+1]
                            #print("aqui:",m2)
                            m3 = text_splitted[i+2]
                            m4 = text_splitted[i+3]
                            if self.msg.match(m3):
                                m3 = ""
                            if self.msg.match(m4):
                                m4 = ""                            
                        else:
                            m1 = m1 + text_splitted[i] + " "

                    match_age_range = self.age_range.match(text_splitted[i])

                    if match_age_range:
                        if match_age_range.string == "Faixa Etária":
                            k = 1
                            m = 1
                            while not re.match(r"0.+", text_splitted[i+k]):                            
                                tables[n][text_splitted[i-1]][text_splitted[i+k]] = []
                                k += 1
                        if match_age_range.string == "Faixa":
                            while not re.match(r"0.+", text_splitted[i+m]):
                                if text_splitted[i+m] == "Etária":
                                    m += 1
                                    continue
                                tables[n][text_splitted[i-1]][text_splitted[i+m]] = []
                                m += 1
                        if m3 == text_splitted[i-1]:
                            m3 = ""                              
                        if m4 == text_splitted[i-1]:
                            m4 = ""
                        n += 1
                
                    match_value = self.value.match(text_splitted[i])
                    if match_value:
                        new_value = match_value.string
                        if new_value[:3] != "R$ ":
                            new_value = "R$ " + match_value.string
                        values.append(new_value)

                    if last_change:
                        index = i
                        first_page = False
                                       
                else:
                    #print(index)
                    last_change = self.last_change.match(text_splitted[index])
                    title_table = self.title_table.match(text_splitted[index])
                    if last_change:
                        if not self.title_table.match(text_splitted[index+1]):
                            m2 = text_splitted[index+1]
                            m3 = text_splitted[index+2]
                            m4 = text_splitted[index+3]
                    if title_table:
                        index_title_table = index + 1
                        n_other_pages += 1
                        #tables[n][title_table.string]["sub_tabela"] = []

                        match_age_range = self.age_range.match(text_splitted[index_title_table])

                        if match_age_range.group(1) == "Faixa Etária":
                            k = 1
                            while not re.match(r"0.+", text_splitted[index_title_table+k]):                                
                                # if text_splitted[index_title_table+k].split(" ")[-1].upper() == m2.upper():
                                    # sub_table = text_splitted[index_title_table+k] + " " + text_splitted[index_title_table+k+1]
                                    #print(sub_table)
                                    # tables[n_other_pages][title_table.string][sub_table] = []
                                # elif text_splitted[index_title_table+k+1].split(" ")[0].upper() == m2.upper():
                                    # sub_table = text_splitted[index_title_table+k] + " " + text_splitted[index_title_table+k+1] + " " + text_splitted[index_title_table+k+2]
                                    #print(sub_table)
                                    # tables[n_other_pages][title_table.string][sub_table] = []
                                print(text_splitted[index_title_table+k])                                                                                                
                                k += 1
                        elif match_age_range.group(2) == "Faixa":
                            l = 2
                            while not re.match(r"0.+", text_splitted[index_title_table+l]):                                
                                if text_splitted[index_title_table+l].split(" ")[-1].upper() == m2.upper():
                                    sub_table = text_splitted[index_title_table+l] + " " + text_splitted[index_title_table+l+1]
                                    print(sub_table)
                                    # tables[n_other_pages][title_table.string][sub_table] = []
                                elif text_splitted[index_title_table+l+1].split(" ")[0].upper() == m2.upper():
                                    sub_table = text_splitted[index_title_table+l] + " " + text_splitted[index_title_table+l+1] + " " + text_splitted[index_title_table+l+2]
                                    print(sub_table)
                                    # tables[n_other_pages][title_table.string][sub_table] = []
                                else:
                                    pass
                                    #print(text_splitted[index_title_table+l])                                                                                                
                                l += 1                            

                    match_age_range = self.age_range.match(text_splitted[index])

                    match_value = self.value.match(text_splitted[index])
                    if match_value:
                        new_value = match_value.string
                        if new_value[:3] != "R$ ":
                            new_value = "R$ " + match_value.string
                        values.append(new_value)
                    
                    index += 1
                    
            #print(values)
            print(json.dumps(tables, indent=4, ensure_ascii=False))

            for n_table in tables:
                for class_ in tables[n_table]:
                    n_symbols = len(tables[n_table][class_])
                    len_table = n_symbols * 10
                    
                    values_of_table = values[:len_table].copy()
                    del values[:len_table]

                    for symbol, row in zip(tables[n_table][class_], range(n_symbols)):                        
                        tables[n_table][class_][symbol] = list(itertools.islice(values_of_table, row, len_table, n_symbols))

            #tables[0] = (re.sub(r"\s$", "", m1), m2, m3, m4)

            data = {}
            for dict_keys in sorted(tables):
                data[dict_keys] = tables[dict_keys]

            #print(json.dumps(data, indent=4, ensure_ascii=False))

            if not need_path:
                pdf = pdf.split("/")[-1]

            self.data[pdf] = list(data.values())

