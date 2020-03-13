import sys

def get_path():
	if len(sys.argv) > 1:
		return sys.argv[1]

	while True:
		try:
			path = input("\nEntre com o caminho do PDF ou do diretório que contém o(s) PDF(s): ")
			option = input('\nGostaria de entrar com o caminho novamente? [n]ão/Enter ou [s]im: ')
		except KeyboardInterrupt:
			print("\n\nPrograma finalizado!")
			exit()
		if option=="": break
		elif option[0].lower() == "n":
			break
	return path		
