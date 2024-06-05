from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from random import *
import math
from time import *

#Grille aléatoire
def randomGrille(L=6,C=5):
    """
    création d'une grille aléatoire.
    cette fonction modfie au passage la grille courante
    cette variable est donc déclarrée globale.
    
    paramètres L (int) nombre de lignes
               C (int) nombre de colonnes
    
    renvoie grille courante (liste)

    """
    grille = [] #Crée un liste vide qui servira de grille
    for y in range(C):
        ligne = [] #Crée un liste qui servira de ligne
        for x in range(L):
            ligne.append(choice(["P", "B", "F"])) #Ajoute un type de case aléatoire entre pierre("P"), bois("B") et feuille("F")
        grille.append(ligne) #Ajoute la ligne à la grille
    return grille #Renvoie la grille aléatoire

#Partie Joueur
def sontVoisines(case1, case2):
    """
    vérifie si deux cases sont adjacentes

    paramètres case1 (liste) case 1
               case2 (liste) case 2

    renvoie un booléen qui vaut True ou False selon le résultat
    """
    dist = math.sqrt((case1[1] - case2[1])**2 + (case1[0] - case2[0])**2) #Utilise Pythagore pour déterminer la distance entre les deux cases
    if dist == 1: #Si la distance séparant les deux cases est de 1
        return True
    return False

def cheminContinu(parcours):
    """
    vérifie si toutes cases sont adjacentes (
    
    paramètres parcours (liste) 
    
    renvoie True ou False selon le résultat    
    """
    for i in range(len(parcours) - 1): #len(mot)-1 car on va comparer une case de mot avec la suivante
        case1 = (parcours[i][0], parcours[i][1]) #Une case de parcours
        case2 = (parcours[i+1][0], parcours[i+1][1]) #La suivante dans la liste
        if not sontVoisines(case1, case2): #Si case1 et case2 ne sont pas voisines
            return False
    return True

def ordreDesCases(parcours,grilleATester):
    """
    vérifie si l'odre des cases est respécté (alternance des cases avec un joker permis)
    
    paramètres parcours (liste) 
               grilleATester (liste) 
    
    renvoie True ou False selon le résultat    
    """
    mot = "" #Crée un chaine de caractère
    JokerUsed = False #Si le joker est utilisé
    for case in parcours: #Pour chaque case dans le parcours
        mot += grilleATester[case[0]][case[1]] #Ajoute le symbole sur la grille correspondant une case de parcours
    for i in range(len(mot) - 1): #len(mot)-1 car on va comparer un symbole de mot avec le suivant
        if mot[i] == mot[i+1]: #Si les deux symboles sont identiques
            if JokerUsed: #Si le joker a déjà été utilisé
                return False
            else:
                JokerUsed = True #le joker est utilisé
    return True

def departArrivee(parcours,grille):
    """
    vérifie si les cases de départ et d'arrivée sont correctes.
    
       
    paramètres parcours (liste) 
               grille (par défaut la grillecourante (liste) 
    
    renvoie True ou False selon le résultat    
    """
    if parcours[-1] == (0, 0) and parcours[0] == (len(grille) - 1, len(grille[0]) - 1): #Si la dernière case de parcours est située en haut à gauche 
                                                                                        #et la première case de parcours est située en bas à droite
        return True
    return False

#Différents éléments graphiques
def loadImg(path, width, height):
    """
    Fonction servant à charger une image.

    paramètres path (string): le chemin sur le disque pour accéder à l'image
               width (int): la longueur voulue
               height (int): la largeur voulue

    renvoie une PhotoImage correspondant l'image chargée et redimentionnée
    """
    image = Image.open(path) #charge l'image correspondant au path
    resize_image = image.resize((width, height)) #redimentionne l'image selon width et height
    img = ImageTk.PhotoImage(resize_image) #transforme l'image en PhotoImage, nécéssaire pour l'ajouter sur un bouton tkinter
    return img

def addSlider(fenetre, name, y, x):
    """
    Fonction servant à créer un slider.

    paramètres fenetre (Tk): la fenetre tkinter sur laquelle ajouter le slider
               name (string): le nom du slider
               y (int): la ligne de la grid où ajouter le slider
               x (int): la colonne de la grid où ajouter le slider

    renvoie un Slider (Scale) en tkinter
    """
    slider = Scale(fenetre, font=fenetre.font, label=name, from_=2, to=20, orient=HORIZONTAL) #Crée le slider pouvant aller de 2 à 20 et orienté horizontalement
    slider.grid(row=y,column=x) #positionne le slider dans la grille selon y et x
    slider.config(font=('Helvetica bold',10)) #change la police du slider en Helvetica bold et met sa taille à 10
    return slider

def addButton(fenetre, name, y, x, func):
    """
    Fonction servant à créer un bouton.

    paramètres fenetre (Tk): la fenetre tkinter sur laquelle ajouter le bouton
               name (string): le nom du bouton
               y (int): la ligne de la grid où ajouter le bouton
               x (int): la colonne de la grid où ajouter le bouton
               func (function): ce qu'il faut executer lors du click

    renvoie un bouton (Button) en tkinter
    """
    button = Button(fenetre, text = name,font=fenetre.font,relief='raised', borderwidth=5) #Crée un bouton dans fenetre correspondant aux arguments donnée
    button.grid(row=y, column=x) #positionne le bouton dans la grille selon y et x
    button.configure(command=func) #ajoute l'exécution de func lors du click
    return button

def addButtonToTable(tableauBoutons, coords, btn):
    """
    Fonction servant ajouter un bouton dans la grille tableauBoutons aux coordonnées coords.

    paramètres tableauBoutons (list): la grille avant l'ajout du bouton
               coords (tuple of ints): les coordonnées dans tableauBoutons où on veux ajouter le bouton
               btn (Button): le bouton à ajouter

    renvoie une grille similaire à tableauBouton avec le bouton aux coordonnées changé
    """
    tableB = tableauBoutons.copy() #Crée tableB, une liste identique à tableauBouton par précaution
    tableB[coords[0]][coords[1]]=btn #Remplace l'element correspondant aux coords dans tableB par btn
    tableB[coords[0]][coords[1]].grid(row=coords[0], column=coords[1]) #positionne btn dans la grille selon coords
    return tableB

#Recherches de chemins
def rechercheCasesVoisinesPossibles(grille, cheminParcouru, caseActuelle):
    """
    cherche les cases possibles au cours du mouvement

    paramètres grille (liste) 
               cheminParcouru (liste) : le chemin déjà parcouru
               caseActuelle (liste) : case sur laquelle se trouve le castor

    renvoie une liste contenant les différentes cases possibles
    """
    possibleWays = [] #liste contenant les différentes cases possibles
    allDirs = [(0, -1), (-1, 0), (0, 1), (1, 0)] #les différentes directions possibles
    for dir in allDirs:
        tempChemin = cheminParcouru.copy() #crée une copie de cheminParcouru
        caseToGo = (caseActuelle[0] + dir[0], caseActuelle[1] + dir[1]) #la case où le bot va aller
        if 0 <= caseToGo[0] <= (len(grille) - 1) and 0 <= caseToGo[1] <= (len(grille[0]) - 1): #si la case est dans la grille (elle ne sort pas)
            tempChemin.append(caseToGo) #ajoute la case au chemin temporaire
            if ordreDesCases(tempChemin, grille) and cheminContinu(tempChemin) and caseToGo not in cheminParcouru: #teste si le chemin est valide et la case n'a pas déjà été parcourue
                possibleWays.append(caseToGo) #ajoute la case aux possibilités
    return possibleWays

def cheminAleatoire1(grille):
    """
    propose un chemin aléatoire progressant vers l'arrivée (déplacement vers le haut ou la gauche uniquement)
    
    paramètres grille (liste) 
    
    renvoie le chemin proposé et si la grille est possible
    """
    caseActuelle = (len(grille) - 1, len(grille[0]) - 1) #défini la case de départ en bas à droite
    cheminActuel = [caseActuelle] #crée une liste chemin qui contient toujours au moins la case de départ
    while True: #Boucle infinie car on utilisera un return pour sortir
        possibleWays = [] #liste des cases où on peux se diriger (uniquement les cases en haut et à gauche)
        allDirs = [(0, -1), (-1, 0)] #Les directions vers la gauche et vers le haut
        for dir in allDirs: #pour chaque direction
            tempChemin = cheminActuel.copy() #crée un chemin temporaire
            caseToGo = (caseActuelle[0] + dir[0], caseActuelle[1] + dir[1]) #ajoute le vecteur dir à la case Actuelle pour trouver la case où il va se déplacer
            if 0 <= caseToGo[0] and 0 <= caseToGo[1]: #si caseToGo ne sort pas de la grille
                tempChemin.append(caseToGo) #ajoute caseToGo au chemin temporaire
                if ordreDesCases(tempChemin, grille) and cheminContinu(tempChemin) and caseToGo not in cheminActuel: #teste si le chemin est valide et la case n'a pas déjà été parcourue
                    possibleWays.append(caseToGo) #ajoute la case aux possibilités

        if len(possibleWays) > 0: #Si on peut bouger
            if (0, 0) not in possibleWays: #Si l'arrivée n'est pas dans les possibilités
                caseToGo = choice(possibleWays) #choisi une case aléatoire parmis celle possible
            else:
                caseToGo = (0, 0) #Se déplace à l'arrivée
            caseActuelle = caseToGo #déplace sur cette case
            cheminActuel.append(caseToGo) #ajoute la case dans cheminActuel
        else:
            return cheminActuel, False #renvoie le chemin et False car il est bloqué

        if caseActuelle == (0, 0): #si il est à l'arrivée
            return cheminActuel, True #renvoie le chemin et True car il a fini

def cheminAleatoire2(grille):
    """
    propose un chemin aléatoire progressant aléatoirement .
    
    paramètres grille (liste)
    
    renvoie le chemin proposé et si la grille est possible
    """
    caseActuelle = (len(grille) - 1, len(grille[0]) - 1) #défini la case de départ en bas à droite
    cheminActuel = [caseActuelle] #crée une liste chemin qui contient toujours au moins la case de départ
    while True: #Boucle infinie car on utilisera un return pour sortir
        possibleWays = rechercheCasesVoisinesPossibles(grille, cheminActuel, caseActuelle) #renvoie une liste des cases possibles

        if len(possibleWays) > 0: #Si on peut bouger
            if (0, 0) not in possibleWays: #Si l'arrivée n'est pas dans les possibilités
                caseToGo = choice(possibleWays) #choisi une case aléatoire parmis celle possible
            else:
                caseToGo = (0, 0) #choisi l'arrivée
            caseActuelle = caseToGo #Se déplace sur caseToGo
            cheminActuel.append(caseToGo) #ajoute la case dans cheminActuel
        else:
            return cheminActuel, False #renvoie le chemin et False car il est bloqué

        if caseActuelle == (0, 0): #si il est à l'arrivée
            return cheminActuel, True #renvoie le chemin et True car il a fini

def chercheChemin(grille, cheminDejaFait):
    """
    cherche un chemin valide pour le castor
    
    paramètres:
        grille(liste): la grille actuelle
        cheminDejaFait(list): le chemin déja parcouru
    
    renvoie le chemin proposé et si la grille est possible
    """
    caseActuelle = cheminDejaFait[-1] #défini la case Actuelle à la dernière case de cheminDejaFait
    cheminActuel = [] #crée une liste chemin
    invalidWays = [] #crée une liste contenant les chemins déjà testés
    while True: #Boucle infinie car on utilisera un return pour sortir
        possibleWays = rechercheCasesVoisinesPossibles(grille, cheminDejaFait + cheminActuel, caseActuelle) #renvoie une liste des cases possibles
        hasAvaliableCases = False #booléen True si on a avancé

        for caseToGo in possibleWays: #Teste chaque case possible
            tempChemin = cheminActuel.copy() #crée un chemin temporaire
            tempChemin.append(caseToGo) #ajoute la case au chemin temporaire
            if tempChemin not in invalidWays: #si le chemin temporaire n'est pas dans invalidWays
                caseActuelle = caseToGo #Se déplace sur caseToGo
                cheminActuel.append(caseToGo) #ajoute la case dans cheminActuel
                hasAvaliableCases = True #On a avancé
                break #Arrète la boucle for car on s'est déplacé

        if not hasAvaliableCases: #Si on n'a pas avancé
            invalidWays.append(cheminActuel.copy()) #On ajoute le chemin aux chemins impossibles
            if len(cheminActuel) > 1: #Si le chemin a au moins une case en plus de celle de départ
                cheminActuel.pop() #On supprime une case
                caseActuelle = cheminActuel[-1] #retourne en arrière
            else: #Si on ne peux pas retourner en arriére
                return cheminActuel, False #Le chemin n'a pas de solution

        if caseActuelle == (0, 0): #si il est à l'arrivée
            return cheminActuel, True #renvoie le chemin et True car il a fini

#debug
if __name__ == "__main__": #S'exécute si le fichier est lancé et non si il est importé
    failed = 0 #nombre de chemins impossibles
    for i in range(100): #test 100 chemins
        grille2 = createRandomGrille() #fait une grille aléatoire
        way, possible = chercheChemin(grille2) #Cherche un chemin dans la grille
        if possible: #si le bot trouve un chemin
            if not (departArrivee(way, grille2) and cheminContinu(way) and ordreDesCases(way, grille2)): #si le chemin trouvé par le bot n'est pas valide
                print(grille2) #affiche la grille
                print(way) #affiche le chemin pris par le bot
        else: #si il ne trouve pas de chemin
            failed += 1 #ajoute 1 au grilles impossibles
    print(failed) #affiche le nombre de grilles impossibles