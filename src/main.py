from core import Simulador
import json

if __name__ == "__main__":
    simulador = Simulador("../data/Teste_01.pdf")
    #simulador = Simulador("../data/Tabela __ Simulador Online - adesão.pdf")

    simulador.get_text()

    print("")

    print(json.dumps(simulador.data, indent=4, ensure_ascii=False))