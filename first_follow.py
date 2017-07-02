from Estado import *

###GLOBAL VARIABLES###
i_line = 1
Estados = []
has_changed = True
pos_estado = None
pos_estado_atual = None
######################

#Print the first sets
def imprime_first():
	global Estados
	print("CONJUNTOS FIRST")
	for estado in Estados:
		print(estado.nome + " -> {", end="")
		for i in range(0, len(estado.first)):
			if i:
				print(", ", end="")
			print(estado.first[i], end="")
		print("}")


#Print the follow sets
def imprime_follow():
	global Estados
	print("CONJUNTOS FOLLOW")
	for estado in Estados:
		print(estado.nome + " -> {", end="")
		for i in range(0, len(estado.follow)):
			if i:
				print(", ", end="")
			print(estado.follow[i], end="")
		print("}")


#Splits a string between '<' and '>' characters to obtain the NonTerminal Symbol
def splitNT(line):
	global i_line
	NT = "" #NonTerminal symbol
	if line[i_line] == '<':
		i_line += 1
	while line[i_line] != '>':
		NT = NT + line[i_line]
		i_line += 1
	return NT


#Verifies if a determinated state exists in the list of states (Estados)
def exists_estado(estado):
	for i in Estados:
		if estado == i.nome:
			return True
	return False


#Search the position of a state in the list (Estados)
def search_pos_estado(estado):
	for i in range(0, len(Estados)):
		if Estados[i].nome == estado:
			return i


#Retorna True se terminou de ler a produção e Falso se precisa continuar lendo
def read_production_first(line):
	global i_line, Estados, has_changed, pos_estado_atual, pos_estado
	if line[i_line] != '<' and line[i_line] != '>':
		#If production's first symbol is Terminal,
		#verifies if it already exists in state's first set.
		if line[i_line] == 'ε':
			Estados[pos_estado_atual].tem_epsilon = True
		if line[i_line] != 'ε' and line[i_line] not in Estados[pos_estado_atual].first:
			Estados[pos_estado_atual].first.append(line[i_line])
			has_changed = True
		i_line += 1
		return True
	else:
		#If production's first symbol is NonTerminal,
		#copy the first set corresponding to it into current state.
		estado = splitNT(line)
		if exists_estado(estado) and estado != Estados[pos_estado_atual].nome:
			pos_estado = search_pos_estado(estado)
			for i in Estados[pos_estado].first:
				if i not in Estados[pos_estado_atual].first:
					Estados[pos_estado_atual].first.append(i)
					has_changed = True
			if not Estados[pos_estado].tem_epsilon:
				return True
		i_line += 1
		return False


#Receives a line from the external file and executes the verification of
#the First Set Algorithm.
def read_line_first(line):
	global i_line, has_changed, Estados, pos_estado, pos_estado_atual
	i_line = 1
	estado = splitNT(line)
	if exists_estado(estado):
		pos_estado_atual = search_pos_estado(estado)
	else:
		Est = Estado()
		Est.nome = estado
		Estados.append(Est)
		pos_estado_atual = len(Estados)-1

	while (line[i_line] == ' ' or line[i_line] == '>' or line[i_line] == ':'
			or line[i_line] == '='):
		i_line += 1

	while line[i_line] != '\n':
		while line[i_line] != ' ' and line[i_line] != '\n':
			if read_production_first(line) == True:
				break

		while line[i_line] != '|':
			if line[i_line] == '\n': return #Current line is over, end function
			i_line += 1
		i_line += 1
		while line[i_line] == ' ':
			i_line += 1


#Everytime flagg is set, it means some first set has changed in last iteration;
#so, the function reopen the file and iterate over it again.
def resolve_first():
	global i_line, Estados, has_changed
	#open file in read mode
	has_changed = False;
	with open("GLC.txt", "r") as File:
		for line in File:
			read_line_first(line)


#Main Function
def main():
	global Estados, has_changed
	has_changed = True
	while has_changed:
		resolve_first()

	imprime_first()
	imprime_follow()

main()
