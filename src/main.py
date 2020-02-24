from core import Simulador
import os

if __name__ == "__main__":
    simulador = Simulador("../samples/")
    simulador.get_text()

    for pdf,values in simulador.data.items():
        pdf_name = pdf[:-4]
        state = 1
        file = open(os.path.join("..", "output", pdf_name+".txt"), "w")
        file.write("Modelo: " + pdf_name + "\n\n")
        for tables in values:
            if state == 1:
                m1, m2, m3, m4 = tables
                state = 2
            elif state == 2:
                for table_name, column in tables.items():
                    m5 = table_name
                    for column_name, column_values in column.items():
                        m6 = column_name
                        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = column_values

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
        
            
