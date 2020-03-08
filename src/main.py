from core import Simulador
import os
import itertools
import json
from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

if __name__ == "__main__":
    path = os.path.join(".", "new_samples")
    simulador = Simulador(path)
    pdfs = simulador.get_data()

    simulador.get_text(pdfs)

    for pdf,values in simulador.data.items():
        pdf_name = pdf[:-4]
        file = open(os.path.join(".", "output", pdf_name+".txt"), "w")
        file.write("Modelo: " + pdf_name + "\n\n")        
        for i in range(len(values)):
            for prepared_data in list(itertools.islice(values, i, len(values), int(len(values)/2))):
                if isinstance(prepared_data, tuple):
                    m1, m2, m3, m4 = prepared_data
                if isinstance(prepared_data, dict):
                   for table, subtable in prepared_data.items():
                       m5 = table
                       for subtable_name, table_values in subtable.items():
                            m6 = subtable_name
                            v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = table_values
                            file.write("m1: " + m1 + "\n")
                            file.write("m2: " + m2 + "\n")
                            file.write("m3: " + m3 + "\n")
                            file.write("m4: " + m4 + "\n")
                            file.write("m5: " + m5 + "\n")
                            file.write("m6: " + m6 + "\n")
                            file.write("v1: " + v1 + "\n")
                            file.write("v2: " + v2 + "\n")
                            file.write("v3: " + v3 + "\n")
                            file.write("v4: " + v4 + "\n")
                            file.write("v5: " + v5 + "\n")
                            file.write("v6: " + v6 + "\n")
                            file.write("v7: " + v7 + "\n")
                            file.write("v8: " + v8 + "\n")
                            file.write("v9: " + v9 + "\n")        
                            file.write("v10: " + v10 + "\n\n")
        file.close()
            
