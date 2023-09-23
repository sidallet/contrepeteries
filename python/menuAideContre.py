import sys
import json
import os
from filtre import *
from arbin import *
from fonc_aide_son import *
from fonc_aide_lettre import *
from commun import *
from utilitaires import *

sys.stdout.reconfigure(encoding='utf-8')

"""
Objectif : Gère le mode aide à la contrepèterie
Paramètres :
	-Entrée :
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
		-historique : historique des 5 derniers mots entrés par l'utilisateur
	-Sortie : 
		-historique : un tableau
"""
def aideContrepetrie(dicoDico,historique):
	with open('data/config.json','r') as diconfig_:
		dicoConfig = json.load(diconfig_)
		langue=dicoConfig['langue'] #on récupère la langue entrée par l'utilisateur
		dicoDico['config']=dicoConfig
	# boucle "tant que" pour le recommencer aide avec un autre mot.
	continuer = 1
	while continuer == 1:
		clear()
		mot=choixMot(historique) #choix du mot
		mot = mot.lower()
		#On update l'historique
		if mot in historique :
			historique.remove(mot)
		historique.insert(0,mot)
		if len(historique) == 6:
			historique.pop(-1)

		#Pour la recherche rapide entre deux mots de la forme : mot1/mot2
		if "/" in mot :
			quadruplRapide(mot)
			continue #Recommence au début du while


		listeDeMotCop = [] #contient les contrepétries du mot entré
		choix=choixMode() #sélection du mode

		clear()
		if(choix == "r" ):
			continuer=0
			continue

		elif choix == "a": #recherche personnalisée pour les lettres
			continuer=modePersonnalisé("word",mot,langue,dicoDico)

		elif choix == "z": #recherche personnalisée pour les sons
			continuer=modePersonnalisé("phon",mot,langue,dicoDico)

		elif choix == "e": #'nimporte quel nombre de lettre
			continuer=recherchePlusieurs(mot,langue,dicoDico)
	return historique


"""
Objectif : Gère le choix du mot de l'utilisateur
Paramètres :
	-Entrée :
		-historique : historique des 5 derniers mots entrés par l'utilisateur
	-Sortie : 
		le mot entré par l'utilisateur
"""
def choixMot(historique):
	if historique != [] : #si l'historique n'est pas vide, on l'affiche
		print("historique : \n")
		for i in range(len(historique)):
			print(i+1," : ",historique[i],"\n")
		print("Pour utiliser l'historique, veuillez entrer le numéro du mot.")
	print("Pour effectuer une recherche rapide entre deux mots, séparez les avec un '/' (code/groupe => gode/croupe).")
	while(True):
		Linput = input("Mot : ")
		if historique != []: #si l'historique n'est pas vide
			if Linput in ["1","2","3","4","5"] and int(Linput) <= len(historique): #on vérifie si le choix est dans l'historique
				mot =  historique[int(Linput)-1]
				return mot
		if "/" in Linput: #on vérifie s'il souhaite effectuer la recherche rapide
			mot=Linput.split('/')
			if(isInDico("word", mot[0]) and isInDico("word", mot[1])): #on vérifie si les deux mots existent
				return Linput
			else:
				print("\nCes mots n'existent pas")
		else:
			if(isInDico("word", Linput)): #on vérifie si le mot existe
				return Linput
			else :
				print("\nL'entrée n'est pas valide ou ce mot n'existe pas")

"""
Objectif : Gère le choix du mode de l'utilisateur
Paramètres :
	-Entrée :
		-tabChoix : tableau contenant les différents choix possibles
	-Sortie : 
		le mode choisi
"""
def choixMode():
	print("\nSélectionner le type de recherche : ")
	print("\ta - recherche par lettre (moule <=> poule)")
	print("\tz - recherche par phonèmes (chute <=> chatte)")
	print("\te - recherche complète (lettres + phonèmes)")
	print("\tr - Retour au menu")
	while(True):
		selection=input("Choix du mode : ")
		if selection in ["a","z","e","r"]: #si le mode choisi est bien dans le tableau
			return selection
		else:
			print("\nL'entrée n'est pas valide, réessayez")
		

"""
Objectif : Gère la sélection de la longueur des syllabes par l'utilisateur
Paramètres :
	-Entrée :
		-message : message à afficher lors de la sélection
	-Sortie : 
		la longueur selectionnée
"""
def longueurSyllabe(message):
	x = True
	while x :
		l=input(message)
		if inputInt(l) :
			if int(l)>0: #on exige au moins 1
				x = False
		else:
			print("Vous n'avez pas entré un nombre convenable. Ressayer")
		
	return int(l)


"""
Objectif : Gère le mode personnalisée (lettre ou phonème)
Paramètres :
	-Entrée :
		-mode : mode sélectionné par l'utilisateur (word => lettren, phon => lettre)
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def modePersonnalisé(mode,mot,langue,dicoDico):
	x = longueurSyllabe("Longueur de la syllabe à enlever dans votre mot (1: c o d e; 2: co od de; ...) : ")
	y = longueurSyllabe("Longueur de la syllabe à ajouter à la place de la syllabe enlevée (1: cOde --> cade;2: cOde --> coude; ...) : ")
	print("Recherche des contrepétries possibles ...")
	calculTempsExecution(len(mot),y,"seul")
	listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)

	if(len(listeDeMotCop) == 0 ):
		affichagePasResultat(mot,"",x,y,"","",dicoDico['config'],mode)
		return	
	boucle = True
	noPage = 1
	taillePage = 51
	nbPage = int(len(listeDeMotCop)/50)+1
	while(boucle):	
		if(mode == "word"):
			if noPage < nbPage :
				affichageBase(mot,listeDeMotCop[taillePage*(noPage-1):taillePage*noPage-1],x)
			else :
				affichageBase(mot,listeDeMotCop[taillePage*(noPage-1):],x)
		else:
			if noPage < nbPage :
				affichageBase(Mot_to_Phon_Only(arbre_mot, mot),listeDeMotCop[taillePage*(noPage-1):taillePage*noPage-1],x)
			else :
				affichageBase(Mot_to_Phon_Only(arbre_mot, mot),listeDeMotCop[taillePage*(noPage-1):],x)
		if(mode == 'word'):
			message="effectuer la recherche avec les phonèmes"
		else:
			message="effectuer la recherche avec les lettres"
		selectMot = None
		print(f"\npage {noPage}/{nbPage}\n")
		selectMot = input(f"\na: retourner au menu\nz: sélectionner un nouveau mot\ne: {message}\nr: page précédente\nt: page suivante \nou numéro de l'échange qui vous intéresse : \n")
		if selectMot == "a":
			return 0
		elif selectMot == "r" :
			if noPage != 1 :
				noPage -= 1
		elif selectMot == "t" :
			if noPage < nbPage :
				noPage += 1
		elif selectMot == "z":
			return 1
		elif selectMot == "e":
			if mode == 'word' :
				mode = 'phon'
			else :
				mode = 'word'
			listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)
		elif inputInt(selectMot) :
			selectMot = int(selectMot)
			if(selectMot > 0):
				print("Veuillez sélectionner la longueur des résultats souhaités")
				minimum=selectionLongueurMot("Longueur minimum (-1=toutes les longueurs) (1: tout les mots; 2: tout les mots sauf ceux de 1 lettre; ...) : ")
				maximum=selectionLongueurMot("Longueur maximum (-1=toutes les longueurs) (5: tous le mots de longueur comprise entre le minimum inscrit précedemment et 5; ...): ")
				listeAffichage, compteur = aideRechDicoGeneral(mot,selectMot+taillePage*(noPage-1), listeDeMotCop,minimum,maximum,dicoDico,mode)
				if selectMot <= len(listeDeMotCop): #evite les erreurs de segmentations
					boucle = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")
		else:
			print("\nL'entrée n'est pas valide, réessayez")

		

	# en cas de liste vide, affichant qu'aucune possibilité n'est trouvée
	if len(listeAffichage) >0:
		#if (diconfig["FiltreGrammatical"] == "Oui"):
		#	listeAffichage = gramFiltre(listeAffichage, mot,langue,mode)
		if(mode=='word'):
			return affiRechLettre(listeAffichage, compteur, mot)
		else:
			return affiRechSon(listeAffichage, compteur, mot,langue, dicoDico)
	else:
		if(mode=="word"):
			mot2=listeDeMotCop[selectMot-1][0]
		else:
			mot2=listeDeMotCop[selectMot-1][3]
		affichagePasResultat(mot,mot2,x,y,minimum,maximum,dicoDico['config'],mode)
	return 1

"""
Objectif : Gère le mode plusieurs (lettre ou phonème)
Paramètres :
	-Entrée :
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def recherchePlusieurs(mot,langue,dicoDico):
	dicoResWord = {}
	dicoResPhon = {}
	longueurMot = len(mot)
	valeurARetourner=0
	#Ce mode met les mots coupés et active par défaut le filtre grammatical
	oldMotCoupe=dicoDico['config']['MotCoupe']
	dicoDico['config']['MotCoupe']="Non"
	oldFiltreGram=dicoDico['config']['FiltreGrammatical']
	dicoDico['config']['FiltreGrammatical']="Oui"
	ecriturePhonMot = Mot_to_Phon_Only(arbre_mot, mot)

	calculTempsExecution(len(mot)-1,4,"plusieurs")
	for x in range(1,longueurMot): #pour chaque tranche possible du mot
		dicoResWord[f"{x}"]=[]
		dicoResPhon[f"{x}"]=[]
		for y in range(1,4): #pour chaque longueur d'échange possible
			listeRes = aide(mot,x,y,"word",langue,dicoDico)
			if(len(listeRes) != 0):
				dicoResWord[f"{x}"].extend(listeRes)
			listeRes = aide(mot,x,y,"phon",langue,dicoDico)
			if(len(listeRes) != 0):
				dicoResPhon[f"{x}"].extend(listeRes)
	boucle=True
	while(boucle):
		affichageBasePlusieurs(mot,dicoResWord,dicoResPhon)
		while(True):
			choix = input("\na: Quitter l'aide\nz: Retour au menu\nentrer le numéro des résultats à afficher : ")
			if(choix == "a"):
				valeurARetourner = choix
				break
			elif(choix == "z"):
				valeurARetourner = 1
				break
			elif inputInt(choix):
				choix=int(choix)
				if(choix < 0 or choix > (len(dicoResWord) + len(dicoResPhon))):
					print("Vous n'avez pas entrer un entier qui fonctionne. Ressayer.")
					continue
				elif(choix <= len(dicoResWord)):
					listeDeMotCop = dicoResWord[str(choix)]
					mode="word"
					break
				else:
					choix = abs(len(dicoResWord) - choix)
					listeDeMotCop = dicoResPhon[str(choix)]
					mode="phon"
					break	
		
		if(valeurARetourner == "a" or valeurARetourner == 1):
			print("coucou")
			boucle = False
			continue
		noPage = 1
		taillePage = 51
		nbPage = int(len(listeDeMotCop)/50)+1
		if(mode == "word"):
			if noPage < nbPage :
				affichageBase(mot,listeDeMotCop[taillePage*(noPage-1):taillePage*noPage-1],x)
			else :
				affichageBase(mot,listeDeMotCop[taillePage*(noPage-1):],x)
		else:
			if noPage < nbPage :
				affichageBase(Mot_to_Phon_Only(arbre_mot, mot),listeDeMotCop[taillePage*(noPage-1):taillePage*noPage-1],x)
			else :
				affichageBase(Mot_to_Phon_Only(arbre_mot, mot),listeDeMotCop[taillePage*(noPage-1):],x)
		boucle2 = True
		while(boucle2):
			selectMot = input("\na: Quitter l'aide\nz: Retour au menu\ne: Revenir à la sélection précédente\n ou numéro de l'échange qui vous intéresse : \n")
			if selectMot == "a" or selectMot == "z":
				valeurARetourner = selectMot
			elif selectMot == "e" : #evite les erreurs de segmentations
				boucle2 = False
			elif inputInt(selectMot) :
				selectMot = int(selectMot)
				if (selectMot <= len(listeDeMotCop) and selectMot > 0):
					boucle2 = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")

		if(selectMot == "e"):
			continue
		listeAffichage, compteur = aideRechDicoGeneral(mot,selectMot, listeDeMotCop,-1,-1,dicoDico,mode)

		# en cas de liste vide, affichant qu'aucune possibilité n'est trouvée
		if len(listeAffichage) >0:
			if(mode=='word'):
				continuer = affiRechLettre(listeAffichage, compteur, mot)
			else:
				continuer = affiRechSon(listeAffichage, compteur, mot,langue, dicoDico)
			if continuer == 0 or continuer == -1:
				valeurARetourner = abs(continuer)
		else:
			if(mode=="word"):
				mot2=listeDeMotCop[selectMot-1][0]
			else:
				mot2=listeDeMotCop[selectMot-1][3]
			affichagePasResultat(mot,mot2,x,y,-1,-1,dicoDico['config'],mode)
	#faire la recherche des quadruplé
	dicoDico['config']['MotCoupe']=oldMotCoupe
	dicoDico['config']['FiltreGrammatical']=oldFiltreGram
	return valeurARetourner


def affichagePasResultat(mot,mot2,x,y,minimum,maximum,diconfig,mode):
	message="Aucune correspondance n'a été trouvée\n"
	if(mode=="phon"):
		message1="phonème(s)"
	else:
		message1="lettre(s)"
	message+=f"Voici les options sélectionnées : \n\t-Recherche au sein du mot : {mot} en échangeant des {message1}"
	if mot2 != "":
		message+=f"\n\t-Echange de {x} {message1} par {y} {message1}"
		message+=f"\n\t-Recherche de quadruplé entre {mot} et {mot2}"
		if(minimum == -1):
			message+="\n\t-Longueur minimum des résultats : aucune"
		else:
			message+=f"\n\t-Longueur minimum des résultats : {minimum}"
		if(maximum == -1):
			message+="\n\t-Longueur maximum des résultats : aucune"
		else:
			message+=f"\n\t-Longueur maximum des résultats : {maximum}"

	if(len(diconfig['Themes'])==0):
		message+="\n\t-Aucun thème d'appliqué"
	else:
		message+="\n\t-Thème(s) appliqué(s) : "
		for theme in diconfig['Themes']:
			message += theme + ", "
	if(diconfig['FiltreGrammatical'] == "Oui"):
		message+=f"\n\t-Filtre grammatical : Activé\n"
	else:
		message+=f"\n\t-Filtre grammatical : Non-Activé\n"
	print(message)
	input('Tapez sur une touche pour revenir avant')