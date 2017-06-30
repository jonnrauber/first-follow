T = {}
E = []

def main():

	for i in range(1,10):
		#abre o arquivo em modo de leitura
		with open("GLC.txt", "r") as arquivo:
			for linha in arquivo:
				if (linha[len(linha)-1] != '\n'):
					linha = linha + '\n'
				if not T:
					T['S'] = {}
					E.append('S')
				print(linha, end = "")


main()