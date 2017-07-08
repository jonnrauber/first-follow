from Estado import *

###GLOBAL VARIABLES###
i_line = 1
Estados = []
has_changed = True
pos_estado = None
pos_estado_atual = None
######################

################### PRINT FUNCTIONS #######################

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

##############################################################


##################### UTIL FUNCTIONS #########################

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

#################################################################


############### FUNCTIONS TO FIND FIRST SET #####################

#Retorna True se terminou de ler a produção e Falso se precisa continuar lendo
def read_production_first(line):
	global i_line, Estados, has_changed, pos_estado_atual, pos_estado
	if line[i_line] != '<' and line[i_line] != '>':
		#If production's first symbol is Terminal,
		#verifies if it already exists in state's first set.
		if line[i_line] not in Estados[pos_estado_atual].first:
			Estados[pos_estado_atual].first.append(line[i_line])
			#print("First(" + Estados[pos_estado_atual].nome + ") <- " + line[i_line])
			has_changed = True
		i_line += 1
		return True
	else:
		#If production's first symbol is NonTerminal,
		#copy the first set corresponding to it into current state.
		estado = splitNT(line)
		if exists_estado(estado):
			pos_estado = search_pos_estado(estado)
			if estado != Estados[pos_estado_atual].nome:
				for i in Estados[pos_estado].first:
					if i not in Estados[pos_estado_atual].first and i != 'ε':
						Estados[pos_estado_atual].first.append(i)
						#print("First(" + Estados[pos_estado_atual].nome + ") <- " + i)
						has_changed = True
				if 'ε' not in Estados[pos_estado].first:
					return True
			else:
				return True
		else:
			return True
		i_line += 1
		if(line[i_line] == ' ' or line[i_line] == '|' or line[i_line] == '\n'):
			if 'ε' not in Estados[pos_estado_atual].first:
				Estados[pos_estado_atual].first.append('ε')
		return False


#Receives a line from the external file and executes the verification of
#the First Set Algorithm.
def read_line_first(line):
	global i_line, has_changed, Estados, pos_estado, pos_estado_atual, all_have_eps
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


#Everytime has_changed is set, it means some first set has changed in last iteration;
#so, the function reopen the file and iterate over it again.
def resolve_first():
	global i_line, Estados, has_changed
	#open file in read mode
	has_changed = False;
	with open("GLC.txt", "r") as File:
		for line in File:
			read_line_first(line)


################# FUNCTIONS TO FIND FOLLOW SETS ######################

#Receives a line and two indexes a & b.
#Returns the FIRST set of the interval [a,b]
def first_substring(line, a, b):
	FIRST = {}



#Receives a line from the external file and executes the verification of the first part of the Follow Set algorithm.
def read_line_follow(line):
	global i_line, Estados, has_changed
	i_line = 1
	estado = splitNT(line)
	while (line[i_line] == ' ' or line[i_line] == '>' or line[i_line] == ':'
			or line[i_line] == '='):
		i_line += 1
	
	while line[i_line] != '\n':
		while line[i_line] == '|' or line[i_line] == ' ':
			i_line += 1
			
		if line[i_line] == '<':
			i_line += 1
			est = splitNT(line)
			i_line += 1
			
			if line[i_line] == '<':
				i_line += 1
				est2 = splitNT(line)
				for i in Estados:
					if i.nome == est2:
						for j in Estados:
							if j.nome == est:
								for k in i.first:
									if k not in j.follow and k != 'ε':
										j.follow.append(k)
				i_line -= 1
				while line[i_line] != '<':
					i_line -= 1
				i_line -= 1
			else:
				if(line[i_line] != '\n'):
					for i in Estados:
						if i.nome == est:
							if line[i_line] not in i.follow and line[i_line] != 'ε' and line[i_line] != ' ':
								i.follow.append(line[i_line])				
		if line[i_line] != '\n':
			i_line += 1


#Receives a line from the external file and executes the verification of the second part of the Follow Set algorithm.
def read_line_follow2(line):
	global i_line, Estados, has_changed, all_have_eps
	all_have_eps = True
	fim_producao = False
	i_line = 1
	estado = splitNT(line)
	while (line[i_line] == ' ' or line[i_line] == '>' or line[i_line] == ':'
			or line[i_line] == '='):
		i_line += 1
	
	while line[i_line] != '\n':
		while line[i_line] != '|' and line[i_line] != '\n':
			i_line += 1
		while line[i_line] == '\n' or line[i_line] == ' ' or line[i_line] == '|':
			i_line -= 1
		all_have_eps = True
		fim_producao = False
		if line[i_line] == '>':
			while all_have_eps == True and fim_producao == False:
				while line[i_line] != '<':
					if(line[i_line] == '=' or line[i_line] == '|'):
						fim_producao = True
						break
					i_line -= 1
				i_line += 1
				est = splitNT(line)
				for i in Estados:
					if i.nome == estado:
						for j in Estados:
							if j.nome == est:
								if 'ε' in j.first:
									all_have_eps = True
								else:
									all_have_eps = False
								for k in i.follow:
									if k not in j.follow:
										has_changed = True
										j.follow.append(k)
				while line[i_line] != '<':
					i_line -= 1
				i_line -= 1
		while line[i_line] != '\n' and line[i_line] != '|':
			i_line += 1
		if line[i_line] == '|':
			i_line += 1

#the function open the file and iterate over it.
def resolve_follow():
	global i_line, Estados, has_changed
	#open file in read mode
	has_changed = False;
	with open("GLC.txt", "r") as File:
		for line in File:
			read_line_follow(line)


#Everytime has_changed is set, it means some follow set has changed in last iteration;
#so, the function reopen the file and iterate over it again.
def resolve_follow2():
	global i_line, Estados, has_changed
	#open file in read mode
	has_changed = False;
	with open("GLC.txt", "r") as File:
		for line in File:
			read_line_follow2(line)


#Put the "Dollar Sign" ($) in the initial state's follow set.
def put_dollar_sign():
	global Estados
	for e in Estados:
		if e.nome == 'S':
			e.follow.append('$')
			return

######################################################################

#Main Function
def main():
	global Estados, has_changed

	##### FIRST ######
	has_changed = True
	while has_changed:
		resolve_first()
	##################

	##### FOLLOW #####
	put_dollar_sign()
	resolve_follow()
	has_changed = True
	while has_changed:
		resolve_follow2()
	##################

	##### PRINT RESULTS #####
	imprime_first()
	imprime_follow()
	#########################


####### EXECUTE PROGRAM ######
main()
