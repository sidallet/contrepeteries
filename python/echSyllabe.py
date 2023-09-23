from arbin import *
import json
import itertools
import sys
from commun import *
from utilitaires import *
import threading
import time

sys.stdout.reconfigure(encoding='utf-8')

###############################################################################
"""
Pour deux mots, teste toutes les combinaisons d'échanges possible entre ces deux mots
Renvoie une liste de type : (nouveauMot1,nouveauMot2,[i,j] du mot1,[i,j] du mot2)
"""

def mixSyllablesWord1(Word1, Word2, phrase, mode, dicoDico, barChargement, avancement):
	listeWord = []
	tmp = []
	i = 0
	j = 0
	while(i < len(Word1)):

		[tmp, allResults] = mixSyllablesWord2(Word1[i:j], Word2, phrase, mode, barChargement, avancement)
		if(dicoDico['config']['MotCoupe'] == "Oui"):
			for x in allResults :
				listemot1 = mixSyllabeCoupe(Word1[:i] + x[1] + Word1[j:], mode,barChargement, avancement)
				listemot2 = mixSyllabeCoupe(x[0], mode,barChargement, avancement)

				for l in listemot1 :
					for k in listemot2 :
						listeWord.append([l,k,[i,j],x[2]])


		for k in tmp:
			# test si retour de Word_to_Phon est une chaîne de caractère,
			# Si oui, alors le mélange est un mot existant
			if isInDico(mode, Word1[:i] + k[1] + Word1[j:]):
				listeWord.append([Word1[:i]+k[1]+Word1[j:], k[0], [i, j], k[2]])

		j += 1
		if (j > len(Word1)):
			i += 1
			j = i+1
	return listeWord

###############################################################################
"""
Créer un nouveau mot à partir de word2 en changeant ses lettres par la syllabe sy
Retourne une liste de résultat de type : (nouveauMot,ancienneSyllabe, le couple[i,j])
"""
def mixSyllablesWord2(sy, Word2, phrase, mode, barChargement,avancement):
	i = 0
	j = 0
	liste = []
	allResults = []

	while(i < len(Word2)):
		# test si retour de Word_to_Phon est une chaîne de caractère
		# et si le Word trouvé n'est pas déjà dans la phrase d'origine.
		#if isInDico(mode, Word2[:i]+sy+Word2[j:]) and Word2[:i]+sy+Word2[j:] not in phrase: #le nouveau mot qu'on forme existe et n'est pas dans la phrase
		if isInDico(mode, Word2[:i]+sy+Word2[j:]):
			liste.append([Word2[:i]+sy+Word2[j:], Word2[i:j], [i, j]])
		# gestion de l'intervalle [i:j] section du Word2
		allResults.append([Word2[:i]+sy+Word2[j:], Word2[i:j], [i, j]])
		j += 1
		if j > len(Word2):
			i += 1
			j = i+1
		barChargement.update(avancement)
		avancement = avancement+1

	return liste, list(allResults)
###############################################################################
"""
prend en entrée la phrase de l'utilisateur,et le mode
soit 'phon' ou 'word' (même mode que pour isInDico)

retourne une liste de tuples de la forme :
(nvllePhrase,index1,index2)
index1 est un tuple contenant les coordonées dans la phrase
du premier mot que l'on échange
index2 est un tuple contenant les coordonées dans la phrase
du deuxième mot que l'on échange
"""

def mainMixSyllables(phrase, mode,dicoDico):

	phrase = phrase.split()
	WordsContreP = []
	#print(phrase)
	Lphrases = [[phrase]] #phrase se contient elle même
	i = 0

	print(f"Recherche des résultats en cours...")
	barChargement = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
	avancement=0
	# Pour chaque mot dans la phrase
	for i in range(len(phrase)):
		# Pour chaque autre mot que tmp dans la phrase on permutra
		#for m in range(i,len(phrase)) :
		
		for j in range(i+1, len(phrase)) :
			WordsContreP = mixSyllablesWord1(phrase[i], phrase[j], phrase, mode,dicoDico, barChargement, avancement)
			Lphrases.extend(createLPhrase1(WordsContreP,phrase, i, j))
			if j != i+1 and i < len(phrase)-1:
				if j < len(phrase)-1 :
					WordsContreP = mixSyllablesWord1(phrase[i]+phrase[i+1],phrase[j]+phrase[j+1],phrase, mode,dicoDico,barChargement, avancement)
					Lphrases.extend(createLPhrase2(WordsContreP,phrase, i, j))		
				else :
					WordsContreP = mixSyllablesWord1(phrase[i]+phrase[i+1],phrase[j],phrase,mode,dicoDico,barChargement, avancement)
					Lphrases.extend(createLPhrase3(WordsContreP,phrase, i, j))	
			else :
				if j < len(phrase)-1 :
					WordsContreP = mixSyllablesWord1(phrase[i],phrase[j]+phrase[j+1],phrase, mode,dicoDico,barChargement, avancement)
					Lphrases.extend(createLPhrase4(WordsContreP,phrase, i, j))
			# remplace les contreP trouvees dans la phrase
	return Lphrases

#------------------------------------------------------------------------------
"""
mixSyllabeCoupe
ajoute des espaces au mot échangé dans mixSyllablesWord1
"""


def mixSyllabeCoupe (word1, mode, barChargement, avancement) :
	liste = []
	if isInDico(mode,word1) :
		liste.append(word1)
	if len(word1) <= 1 :
		return liste
	for i in range(1,len(word1)) :
		moitié1 = mixSyllabeCoupe(word1[0:i], mode,barChargement, avancement)
		moitié2 = mixSyllabeCoupe(word1[i:len(word1)], mode,barChargement, avancement)
		for j in moitié1 :
			for k in moitié2 :
				liste.append(j+' '+k)
				barChargement.update(avancement)
				avancement = avancement+1
	return liste


"""
création liste phrase
"""

def createLPhrase1 (WordsContreP, phrase, i, j) : 
	Lphrases = []
	tmp = []
	for k in WordsContreP:
		tmp = []
		tmp.extend(phrase)
		 #tous les éléments de phrase
		#ajoute les nouveaux mots au même endroit que les anciensdd
		tmp[i] = k[0]
		tmp[j] = k[1]
		test = True
		"""
		for l in Lphrases:
			if l[0] == tmp:
				test = False
        """
		if test:
			L1 = (i, k[2][0], k[2][1])
			L2 = (j, k[3][0], k[3][1])
			Lphrases.append((tmp, L1, L2))
	return Lphrases

def createLPhrase2 (WordsContreP, phrase, i, j) : 
	Lphrases = []
	tmp = []
	for k in WordsContreP:
		tmp = []
		tmp.extend(phrase)
		a = j
		#tous les éléments de phrase
		#ajoute les nouveaux mots au même endroit que les anciensdd
		
		tmp.pop(i+1)
		a = a - 1
		tmp[i] = k[0]
		
		tmp.pop(a+1)
		tmp[a] = k[1]

		# pour chaque nouvelles combinaisons trouvées,
		# on vérifie que la nouvelles n'a pas déjà été trouvée
		
		test = True
		"""
		for l in Lphrases:
			if l[0] == tmp:
				test = False
		"""
		if test:
			L1 = (i, k[2][0], k[2][1])
			L2 = (a, k[3][0], k[3][1])
			Lphrases.append((tmp, L1, L2))
	return Lphrases

def createLPhrase3 (WordsContreP, phrase, i, j) : 
	Lphrases = []
	for k in WordsContreP:
		a = j
		tmp = []
		tmp.extend(phrase)
		#tous les éléments de phrase
		#ajoute les nouveaux mots au même endroit que les anciensdd
		tmp.pop(i+1)
		a = a - 1
		tmp[i] = k[0]
		

		tmp[a] = k[1]

		# pour chaque nouvelles combinaisons trouvées,
		# on vérifie que la nouvelles n'a pas déjà été trouvée
		test = True
		"""
		for l in Lphrases:
			if l[0] == tmp:
				test = False
		"""
		if test:
			L1 = (i, k[2][0], k[2][1])
			L2 = (a, k[3][0], k[3][1])
			Lphrases.append((tmp, L1, L2))
	return Lphrases

def createLPhrase4 (WordsContreP, phrase, i, j) : 
	Lphrases = []
	tmp = []
	for k in WordsContreP:
		tmp = []
		tmp.extend(phrase)
		#tous les éléments de phrase
		#ajoute les nouveaux mots au même endroit que les anciensdd
		

		tmp[i] = k[0]
		
		tmp.pop(j+1)
		tmp[j] = k[1]

		# pour chaque nouvelles combinaisons trouvées,
		# on vérifie que la nouvelles n'a pas déjà été trouvée
		test = True
		"""
		for l in Lphrases:
			if l[0] == tmp:
				test = False
		"""
		if test:
			L1 = (i, k[2][0], k[2][1])
			L2 = (j, k[3][0], k[3][1])
			Lphrases.append((tmp, L1, L2))
	return Lphrases



###############################################################################
"""
Retourne liste de phonème de la phrase :
'la poule qui mu' -> 'la pul ki my
"""
def Phrase_to_Phon(phrase):
	string = ''
	for mot in phrase.split():
		b=Mot_to_Phon_Only(arbre_mot, mot)
		if b != False:
			string += b + ' '
		else:
			print('\nLe mot', mot, '''de la phrase n\'est pas dans notre dictonnaire.
			Veuillez essayer avec une autre orthographe.''')
			return False
			break
	return string

################################################################################
'''
Prend en argument une phrase en phonétique en string
retourne les combinaisons possibles de phrases en orthographe
classique en string
phraseOrigine est la liste des mots de la phrase d'origine,
on l'utilise pour filtrer les resultats des combinaisons
selon un % de mots recurrent entre la nvlle et l'ancienne phrase
'''

def Phon_to_Phrase(PhrasePhoneme, phraseOrigine, pos1, pos2,langue,dicoPhon):

	listeretour = []
	listePhon = PhrasePhoneme.split()
	# PhrasePhoneme(str)
	#print(dicoPhon["e"])

# Extraction du dico de phonème les mots possible a partir des phonèmes en entrée
	for i in range(len(listePhon)):
		listePhon[i] = dicoPhon[listePhon[i]] #Pour chaque phonème de la phrase, on récupère tous les mots qui s'écrivent pareil

		#string = string+" "+listePhon[i][0]


	listeretour.append(listePhon)

# Produit de toutes les combinaisons possibles des mots
# qui ont changer par rapport à la phrase d'origine
	return listeretour



"""
Applique les filtres et affiche les résultats en fonctions de la config
donnée par l'utilisateur
"""
def affiRechFiltre(nvDico,mode,isAllContrepeterie, noPage, nbPage, taille):

	with open('data/config.json') as diconfig_:
		diconfig = json.load(diconfig_)

	if mode == 'phon':
		count1 = 0
		count2 = 0
		for key in nvDico:
			count1 += len(nvDico[key])

		if(count1 == 0):
			print("Pas de résultats pour la recherche avec les phonèmes.")
			input("appuyer sur n'importe quelle touche puis entrée pour retourner au menu")
			return 0
		StockPourkey = ""
		compteur = 1
		dicores = []
		print("\nVoici les résultats possibles en échangeant les phonèmes. \nUn exemple d'orthographe pour chaque phrase vous ai donné.\n")
		for key in nvDico:
			for j in nvDico[key]:
				#j = ' '.join(j) #Joint chaque élément par "" de nvDico[key]
				if j[0] == " ":
					j = j[1:] #Si la phrase commence par un espace, on l'enlève
				for k in range(len(j[0])) :
					"""j[0][k] = """
					j[0][k].capitalize() #Met la première en majuscule et toutes les autres en minuscules
				if StockPourkey != key :#and len(language_tool_python.LanguageToolPublicAPI('fr').check(j)) == 0:
					print(compteur, " -->", end=" ")
					for k in range(len(j)) :
						print(j[k][0], end = ' ')
					StockPourkey = key
					dicores.append(key)
					print()
					compteur+=1
		print(f"\npage {noPage}/{nbPage}")
		print('\nNombre de résultats pour les échanges avec les phonèmes : ', taille)
		choixutilisateur = 1
		while True:
			try:
				if(isAllContrepeterie):
					choixutilisateur = input("\nz - Quitter la recherche\ne - page précédente\nr - page suivante\nou saisissez un des index pour obtenir toutes les ortographes : ")
				else:
					choixutilisateur = input(
				"\na - quitter l'application\nz - revenir au menu principal\ne - page précédente\nr - page suivante\nou saisissez un des index pour obtenir toutes les ortographes : ")
			except:
				print("\nVous n'avez pas saisi un chiffre")
				continue
			if inputInt(choixutilisateur):
				choixutilisateur =  int(choixutilisateur)
				if (choixutilisateur) < compteur and choixutilisateur > -1:
					print("\nAffichage des différentes orthographes. Une orthographe de chaque mot vous est proposée : ")
					for j in nvDico[dicores[choixutilisateur-1]]: #pour chaque orthographe de la phrase
						maxlen = 0
						phrase = []	
						for k in range(len(j)) :
							phrase.append(j[k])
							if len(j[k]) > maxlen :
								maxlen = len(j[k])
							for l in range(len(phrase[0])) :
								phrase[0][l] = phrase[0][l].capitalize()
						#if diconfig["FiltreGrammatical"] == "Oui":
								#matches = language_tool_python.LanguageToolPublicAPI('fr').check(j)
								#if len(matches) == 0:
						for m in range(maxlen) :
							for n in range(len(phrase)) :
								if len(phrase[n]) > m :
									print(phrase[n][m], end=" ")
								else :
									print(phrase[n][0], end=" ")
							print()


							#else:
							#	print(j)

			elif choixutilisateur == "a":
				return 0
			elif choixutilisateur == "z":
				return 1
			elif choixutilisateur == "e":
				return 2
			elif choixutilisateur == "r":
				return 3

	if mode == 'word':
		#attention, ici nvDico est une liste de tuple, plus un dico
		#filtrage par grammaire de la phrase
		nvListe = [nvDico[0]]

		tmpListe = []
		tmpListe =  nvDico[:]
		#filtrage par mot vulgaires
		for contrepet in tmpListe[1:]:
			nvListe.append(" ".join(contrepet[0]))
		if(isAllContrepeterie):
			return nvListe
		else:
			affichagePhraseLettre(nvListe)


"""
Objectif : Affiche le résultats de la recherche de contrepèteries par échange de lettres dans une phrase
Paramètres :
    -Entrée :
        listeRes : liste des réponses
    -Sortie :
        aucun
"""
def affichagePhraseLettre(listeRes):
	if(len(listeRes) == 0):
		print("Pas de résultats pour l'échange avec les lettres")
		return
	print("Voici les résultats en échangeant les lettres.")
	count=1
	for contrepet in listeRes[1:]:
		print(f"{count} --> {contrepet}")
		count += 1
	print('\nNombre de résultats pour les échanges avec les lettres : ', count)
	input("Tapez sur entrée pour revenir au menu")