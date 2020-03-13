.PHONY: help prepare-dev run
PYTHON=/usr/bin/python3

.DEFAULT: help
help:
	@echo "\nmake prepare-dev"
	@echo "       Prepara ambiente de desenvolvimento, use apenas uma vez.\n"	
	@echo "make run"
	@echo "       Executa o programa principal\n"
	@echo "make run path=CAMINHO_DA_PASTA/ARQUIVO"
	@echo "       Executa o programa principal passando o caminho da pasta/arquivo conténdo os PDFs.\n"	

prepare-dev:
	sudo apt update
	sudo apt full-upgrade -y
	sudo apt install python3 python3-pip -y 
	${PYTHON} -m pip install -U pip --user
	${PYTHON} -m pip install -r requirements.txt --user

run: src
	${PYTHON} src/main.py $(path)
