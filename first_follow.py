

class Estado:
	nome = ""
	firsts = []

i_linha = 1
Estados = []
flagg = ""

def splitNT (linha):
	global i_linha
	NT = ""

	while linha[i_linha] != '>':
		NT = NT + linha[i_linha]
		i_linha += 1
	return NT

def Resolvefirst():
	global i_linha, Estados, flagg
	#abre o arquivo em modo de leitura
	with open("entrada.txt", "r") as arquivo:
		for linha in arquivo:
			flag = 0;
			if (linha[len(linha)-1] != '\n'):
				linha = linha + '\n'
			
			estado = splitNT(linha)
			for i in Estados:
				if estado == i.nome:
					flag = 1;
			
			if flag == 0:
				Est = Estado()
				Est.nome = estado
				Estados.append(Est)
			
			while linha[i_linha] != ':':
				i_linha += 1
			i_linha += 3 #pula o simbolo da atribuição ::=
			while linha[i_linha] == ' ':
				i_linha += 1
			
			while linha[i_linha] != '\n':
				if linha[i_linha] != '<':
					flagg = 1
					Estados[len(Estados)-1].firsts.append(linha[i_linha])
					
				else:
					i_linha += 1
					estado = splitNT(linha)
					
					for i in Estados:
						if i.nome == estado:
							for j in i.firsts:
								flagg = 1
								Estados[len(Estados)-1].firsts.append(j)
				while linha[i_linha] != '|':
					if linha[i_linha] == '\n':
						break
					i_linha += 1
					print(linha[i_linha])
				
				if linha[i_linha] == '|':
					print("ola")
					while linha[i_linha] != ' ':
						i_linha += 1			
			i_linha = 1

def main():
	global Estados,flagg
	flagg = 0
	while flagg == 0:	
		Resolvefirst()
main()
