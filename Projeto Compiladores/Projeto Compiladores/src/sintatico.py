import sys
from collections import defaultdict
from lex import *
from ap import Pilha
from src.lexico import *


def a_sintatica(Fita, TabelaSimbolos):

    return False


class styxAlg:

	def __init__(self,grammar,source):
		self.dfa = {}
		self.la = {}
		self.terminals = {}
		self.nonterminals = {}
		self.slr = defaultdict(list)
		self.dfa_t = defaultdict(list)
		self.rules = []
		self.readGOLDParserFile(grammar)
		self.p = lexAlg(self.dfa_t,self.dfa)
		self.lexicalFlag = 0
		if(self.p.lexicalAnalysis(source)==0):
			self.lexicalFlag = 1

	def readGOLDParserFile(self,arq):
		lalrFlag = 0
		slrFlag = 0
		l = open(arq)

		while(1):

			f = l.readline()
			if(f == ''): break
			elif("Terminals" in f ):
				st = f.strip()
				st = st.split()
				stage = 0
				self.slr[-1] = [[],[]]
				counter = 0
			elif((("Terminals" in st[0]) and stage==0)and counter < int(st[1])):
				f = f.strip()
				f = f.split()
				self.slr[-1][0].append(f[1])
				self.terminals[int(f[0])] = f[1]
				counter = counter + 1
			elif(("Nonterminals") in f ):
				st = f.strip()
				st = st.split()
				stage = 1
				counter	 = 0
				#slr[-1].append(['']*st[1])
			elif((("Nonterminals" in st[0]) and stage==1)and counter < int(st[1])):
				f = f.strip()
				f = f.split()
				self.slr[-1][1].append(f[1])
				self.nonterminals[int(f[0])] = f[1]
				counter = counter + 1
			elif("Rules" in f):

				st = f.strip()
				st = st.split()
				stage = 2
				counter= 0
			elif((("Rules" in st[0]) and stage==2)and counter < int(st[1])):
				f = f.strip()
				f = f.split()

				temp = f[1]
				self.rules.append([f[0],temp,' '.join(f[3:])])

				counter = counter + 1
			elif("DFA" in f):
				st = f.strip()
				st = st.split()
				stage = 3
				counter  =0
				#state = 0
			elif((("DFA" in st[0]) and stage==3)and counter < int(st[2])):

				f = f.strip()
				f = f.split()
				if("State" in f):
					state = int(f[1])
					self.dfa_t[state] = []
					#counter= counter + 1
					#print(state)
					#continue

				if("Accept" in f):
					self.dfa[state] = f[1]

				elif("Goto" in f):
					string = f[2] + ":" +f[1]
					#print(string + str(f[1]))
					#print(str(counter))
					self.dfa_t[state].append(str(string))
				counter = counter + 1
			elif("LALR States" in f):

				st = f.strip()
				st = st.split()
				stage = 4
				counter= 0

			elif((("LALR" in st[0]) and stage==4)and counter < int(st[2])+1):

				f = f.strip()
				f = f.split()

				if("State" in f):
					state = int(f[1])
					counter = counter + 1
					lalrFlag = 0
					slrFlag = 0
				if("tb" in f):
					slrFlag = 1
					lalrFlag = 0
					#print("sim")
					continue
				if("la" in f):
					lalrFlag = 1
					slrFlag = 0
					continue

				if(lalrFlag == 1):
					#print(f)
					#print(la.keys())
					if(state not in self.la.keys()):
						self.la[state] = []

					self.la[state].append([' '.join(f)])

				if(slrFlag == 1):
					#state = int(f[1])
					letIn = 0
					if(state not in self.slr.keys()):
						self.slr[state] = [['']*len(self.slr[-1][0]),['']*len(self.slr[-1][1])]
					if("<" == f[0][1] and len(f[0])==3):
						letIn = 1
					if("<" not in f[0] or letIn == 1):
						indice = self.slr[-1][0].index(f[0])
						if(len(f)==2):
							self.slr[state][0][indice] = str(f[1])
						else:self.slr[state][0][indice] = str(f[1]+f[2])
					else:
						indice = self.slr[-1][1].index(f[0])
						self.slr[state][1][indice] = str(f[2])





	def getError(self,source,target):
		indx = [ i[0] for i in enumerate(self.slr[source][0]) if i[1]!='']

		rt = [self.slr[-1][0][i] for i in indx]
		#print(rt)
		rt = " , ".join(rt)
		ft = [i[1][0] for i in enumerate(self.p.ts) if i[0] < target]
		ft = ' '.join(ft)
		ft = ft + ' >#<'

		return rt,ft
	def syntaxAnalysis(self,debug = False):

		if(self.lexicalFlag==1):
			pilha = Pilha()
			pilha.empilha(["",0])

			#prox = p.f[0]
			#p#rox = prox.split(":")
			#pilha.append([
			pos = 1
			pos_fita = 0
			while(1):
				#Percorre a fita token a token
				if(pos_fita >= len(self.p.ts)):
					ind = 0
				else:
					prox = self.p.ts[pos_fita]
					ps = self.dfa[prox[1]]
					ind = self.slr[-1][0].index(ps)


				#Verifica na tabela lalr o mapeamento para o token
				rs = self.slr[pilha.topo()[1]][0][ind]
				if(debug):
					print("Pilha: " + str(pilha.dados))
				if("r" in rs):
					reduce = int(rs[1:])
					tam = len(self.rules[reduce][2].split())
					#pos_fita = pos_fita - tam
					pilha.desempilha(tam)

					index_nonterminals = self.slr[-1][1].index(self.rules[reduce][1])
					#rule = nonterminals.keys()[nonterminals.values().index(rules[reduce][1])]

					next = self.slr[pilha.topo()[1]][1][index_nonterminals]

					pilha.empilha([self.rules[reduce][1],int(next)])
					#pos_fita = pos_fita + 1


				elif("s" in rs):
					pilha.empilha([prox[0],int(rs[1:])])
					pos_fita = pos_fita + 1
					pos = pos +1
				elif("a" in rs):
					print("\nCódigo Sintaticamente Correto!")
					break
				else:
					rt = self.getError(pilha.topo()[1],pos_fita)
					print("Erro sintatico:")
					print("Esperava algum desses tokens:" + str(rt[0]) +" na Linha:" +str(self.p.ts[pos_fita][2]))
					print(" Após: "+ str(rt[1]))

					break
				#if(pilha.tam == 2 and pilha.topo[0]==nonterminals[1] and pos >= len(p.ts)):
				#	print("Sintaticamente correto")
				#	break




test = styxAlg("table.txt","codigo.txt")
test.syntaxAnalysis(False)
#syntaxAnalysis(True)
