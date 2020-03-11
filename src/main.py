from core import Simulador
import os
import itertools
import json

if __name__ == "__main__":
    path = os.path.join(".", "new_samples")
    path = os.path.join(".", "new_samples", "PF_UnimedRio_RiodeJaneiro.pdf")
    path = os.path.join(".", "new_samples", "Adesao_Sulmareica_Qualicorp_Alagoas.pdf")

    simulador = Simulador(path)
    pdfs = simulador.get_data()

    prepaired_data = simulador.prepare_text(pdfs)

    simulador.extract_info(prepaired_data)
    exit()

    # for pdf,values in simulador.data.items():
    #     state = 1
    #     pdf_name = pdf[:-4]
    #     file = open(os.path.join(".", "output", pdf_name+".txt"), "w")
    #     file.write("Modelo: " + pdf_name + "\n\n")
    #     for i, value in enumerate(values):
    #         print(i)

    for pdf,values in simulador.data.items():
        state = 1
        pdf_name = pdf[:-4]
        file = open(os.path.join(".", "output", pdf_name+".txt"), "w")
        file.write("Modelo: " + pdf_name + "\n\n")

        while len(values) != 0:
            for i, value in enumerate(values):
                if isinstance(value, tuple) and state == 1:
                    print(value)
                    m1, m2, m3, m4 = value
                    values.pop(i)
                    state = 2
                elif isinstance(value, dict) and state == 2:
                    for table, subtable in value.items():
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
                    values.pop(i)
                    state = 1
        file.close()
            
