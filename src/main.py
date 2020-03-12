from core import Simulador
import os
import itertools
import json

if __name__ == "__main__":

    path = os.path.join(".", "new_samples")
    path = os.path.join(".", "samples")
    
    simulador = Simulador(path)
    pdfs = simulador.get_data()

    prepaired_data = simulador.prepare_text(pdfs)

    data = simulador.extract_info(prepaired_data)

    for pdf, all_values in data.items():
        file = open(os.path.join(".", "output", pdf+".txt"), "w")
        file.write("Modelo: " + pdf + "\n\n")  
        print(pdf)      
        for value in all_values.values():
            for key, tables in value.items():
                m1, m2, m3, m4 = key
                for table_name, table_values in tables.items():
                    m5 = table_name
                    for header, final_values in table_values.items():
                        m6 = header
                        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = final_values
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