from core import Simulador
import json

if __name__ == "__main__":
    simulador = Simulador("../data/")

    simulador.get_text()

    #print(json.dumps(simulador.data, indent=4, ensure_ascii=False))

    with open("data.json","w") as file:
        json.dump(simulador.data, file, indent=4, ensure_ascii=False)