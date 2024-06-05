from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from random import *
from functions import *
from time import *

class Game(Tk): #Crée une classe game héritant de la classe Tk de tkinter qui crée une fenêtre
    def __init__(self): #Actions à éxécuter lors de la création
        super().__init__() #Actions à éxécuter lors de la création définies dans la classe parent
        self.grille_1= [["P","B","P","F","P","P"], #grille standard
                        ["F","P","P","P","B","B"],
                        ["P","P","F","P","B","P"],
                        ["P","B","F","F","F","B"],
                        ["P","B","P","F","B","F"]]
        self.grillecourante=self.grille_1.copy() #crée un copie de la grille standart et l'assigne à la grille courante
        self.font = font.Font(family='Arial', size=18, weight='bold') #défini le font par défaut utilisé
        
        self.initialisenew() #Initialise le jeu

    def initialisenew(self):
        """
        Initialise le jeu Tkinter en ajoutant les boutons et les différentes variables
        """
        #Declaration des variables principales
        self.player = (len(self.grillecourante)-1, len(self.grillecourante[0])-1) #Positionne le joueur en bas à droite de la grille
        self.chemin = [self.player] #chemin est la variable qui recueille le chemin au fur et à mesure des clics dans la grille
        self.JokerUsed = False #True si le joker a été utilisé
        
        #Initialisation de la grille
        self.loadAssets(60) #charge les images en 60x60 pixels
        self.draw_screen(60) #Crée la grille
        self.initLabels() #Crée les boutons
        
        #Check si la grille est possible
        self.soluce, possible = chercheChemin(self.grillecourante, self.chemin) #cherche un chemin
        self.reponse.set("Possible" if possible else "Impossible") #ecrit sur le label reponse si le chemin est possible

    def createRandomGrille(self):
        """
            Crée un grille aléatoire puis la dessine
        """
        self.grillecourante=randomGrille(self.longueurMeter.get(), self.largeurMeter.get()) #Crée une grille aléatoire avec les dimentions en fonction des Scales

        self.supprimeElements() #Supprime touts les éléments de la fenêtre
        self.initialisenew() #Initialise le jeu

    def supprimeElements(self):
        """
            Supprime tous les éléments de la fenêtre
        """
        for button in self.labels: #Pour chaque bouton (autre que ceux de la grille)
            button.destroy() #supprime le bouton
        for ligne in self.tableauBoutons: #Pour chaque liste dans tableauBoutons
            for button in ligne: #Pour chaque bouton dans la liste
                button.destroy() #supprime le bouton

    def loadAssets(self, size):
        """
            Charge les images nécéssaires au jeu

        Args:
            size (int): la taille des images
        """
        self.playerSprite=loadImg("../assets/playerBase.png", size, size) #charge l'image du joueur
        self.photoF=loadImg("../assets/feuille.png", size, size) #charge l'image de la feuille
        self.photoB=loadImg("../assets/bois.png", size, size) #charge l'image du bois
        self.photoP=loadImg("../assets/pierre.png", size, size) #charge l'image de la pierre

        self.assets = {"F": self.photoF, "B": self.photoB, "P": self.photoP} #crée un dictionnaire permettant de retrouver l'image correspondant au symbole sur la grille

    def initLabels(self):
        """
            Crée tous les éléments de la fenetre autre que la grille
        """
        self.labels = [] #Liste contenant tous les éléments utilisateur
        longueurGrille = len(self.grillecourante[0]) #la longueur de la grille
        largeurGrille = len(self.grillecourante) #la largeur de la grille
        
        self.labels.append(addButton(self, "Chemin Aléatoire 1", 0, longueurGrille, lambda: print(cheminAleatoire1(self.grillecourante)))) #crée le bouton executant la fonction cheminAleatoire1
        self.labels.append(addButton(self, "Chemin Aléatoire 2", 1, longueurGrille, lambda: print(cheminAleatoire2(self.grillecourante)))) #crée le bouton executant la fonction cheminAleatoire2
        self.labels.append(addButton(self, "Help Me", 2, longueurGrille, lambda: print(chercheChemin(self.grillecourante, [(len(self.grillecourante)-1, len(self.grillecourante[0])-1)])))) #crée le bouton executant la fonction chercheChemin
        self.labels.append(addButton(self, "Walk", 3, longueurGrille, lambda: self.walkWay())) #crée le bouton permettant de déplacer le bot dans la grille

        self.labels.append(addButton(self, "Nouvelle Grille", 0, longueurGrille + 1, lambda: self.createRandomGrille())) #crée le bouton permettant de créer une nouvelle grille aléatoire
        self.labels.append(addButton(self, "Parcours terminé", 1, longueurGrille + 1, lambda: self.verification(self.chemin,self.grillecourante))) #crée le bouton vérifiant si le chemin est correct
        self.labels.append(addButton(self, "Annule", 2, longueurGrille + 1, lambda: self.rollback())) #crée le bouton permettant de retourner en arrière
        self.labels.append(addButton(self, "Réinitialiser", 3, longueurGrille + 1, lambda: self.initialisenew())) #crée le bouton permettant de rénétialiser la grille sans la changer

        self.longueurMeter = addSlider(self, "Colonnes", 1, longueurGrille + 2) #crée un Scale ajustable pour définir la longueur de la grille aléatoire
        self.largeurMeter = addSlider(self, "Lignes", 2, longueurGrille + 2) #crée un Scale ajustable pour définir la largeur de la grille aléatoire
        self.longueurMeter.set(longueurGrille) #met la valeur à la longueur de la grille actuelle
        self.largeurMeter.set(largeurGrille) #met la valeur à la largeur de la grille actuelle
        self.labels.append(self.longueurMeter) #ajoute longueurMeter aux labels
        self.labels.append(self.largeurMeter) #ajoute largeurMeter aux labels

        self.reponse=StringVar() #le texte écrit sur le label commentaire
        self.reponse.set("") #Par défaut vide

        commentaire= Label(self,font=self.font, textvariable=self.reponse) # label qui contient le commentaire Gagné / Perdu ou Possible / Impossible
        commentaire.grid(row=4,column=longueurGrille) #Positionne commentaire
        self.labels.append(commentaire) #ajoute commentaire aux labels

    def draw_screen(self, size):
        """
            fonction qui initialise le jeu : mise en place de la grille graphique et activation des boutons asscociés.
            Par défaut c'est la grille_1. Chaque image est affichée à sa place sur la grille.
            La grille est une liste de liste comprenant des "P", "F", "B"

        Args:
            size (int): taille des boutons (identique à la taille des images)
        """
        lines=len(self.grillecourante) #la largeur de la grille
        columns=len(self.grillecourante[0]) #la longueur de la grille
        self.tableauBoutons=[[0 for _ in range(columns)] for _ in range(lines)] #crée un matrice remplie de zéros qu'on remplacera par les boutons de la grille
    
        for y in range(lines):
            for x in range(columns):
                bouton = Button(image=self.assets.get(self.grillecourante[y][x], self.playerSprite), width=size, height=size) #crée un bouton ayant une image correspondant au symbole sur la grille
                bouton.configure(command= lambda b=bouton, absc=y, ordon=x: self.clic(b, absc, ordon, self.grillecourante[y][x])) #lors du click la fonction click() est appelée
                
                self.tableauBoutons=addButtonToTable(self.tableauBoutons, (y, x), bouton) #ajoute le bouton dans tableauBoutons

        boutonPlayer = self.tableauBoutons[self.player[0]][self.player[1]] #Obtient le bouton aux coordonées du joueur dans tableauBoutons
        boutonPlayer.configure(image=self.playerSprite) #change l'image du bouton en celle du joueur
        boutonPlayer["state"]=DISABLED #Le bouton n'est plus cliquable

    def clic (self, btn, ligne, colon, typecase):
        """fonction qui gére le clic sur un bouton

        Args:
            btn (Button): le bouton cliqué
            ligne (int): la ligne correspondant au bouton cliqué dans tableauBoutons
            colon (int): la colonne correspondant au bouton cliqué dans tableauBoutons
            typecase (str): le type de la case cliquée
        """
        btn.configure(image=self.playerSprite) #on lui met l'image du joueur
        btn["state"]=DISABLED  # on désactive le bouton
        self.chemin.append((ligne, colon))  #on ajoute  la case au chemin
        
        boutonPrecedent = self.tableauBoutons[self.player[0]][self.player[1]] #on recupere le bouton depuis lequel le joueur bouge
        boutonPrecedent.configure(image=self.assets.get(self.grillecourante[self.player[0]][self.player[1]], self.playerSprite)) #on lui remet son image correspondante à son type
        
        self.player = (ligne, colon) #on déplace le joueur

    def walkWay(self):
        """
            Fonction permettant au bot de se déplacer dans la grille

        Args:
            chemin (list of tuples): le chemin trouvé par le bot
        """
        cheminToDo, possible = chercheChemin(self.grillecourante, self.chemin)
        travel = cheminToDo.copy() #crée un liste travel temporaire
        if possible: #si le chemin est possible
            for case in travel:
                button = self.tableauBoutons[case[0]][case[1]] #on recupere le bouton ou le joeur veux se déplacer
                if button["state"]!=DISABLED: #Si le bouton n'est déjà pas cliqué
                    self.clic(button, case[0], case[1], self.grillecourante[case[0]][case[1]]) #on simule un click dessus

    def rollback(self):
        """
            Permet un retour en arrière (si le joueur n'est pas au départ)
        """
        if len(self.chemin) > 1: #si le joueur n'est pas au départ
            boutonPlayer = self.tableauBoutons[self.player[0]][self.player[1]] #récupère le bouton actuel
            boutonPlayer.configure(image=self.assets.get(self.grillecourante[self.player[0]][self.player[1]])) #on lui remet son image correspondante à son type
            boutonPlayer["state"]=NORMAL #on le réactive

            self.chemin.pop() #on supprime la derniere case de chemin
            self.player = self.chemin[-1] #on fait reculer le joueur

            boutonPrecedent = self.tableauBoutons[self.player[0]][self.player[1]] #récupère le bouton précédent
            boutonPrecedent.configure(image=self.playerSprite) #on lui met l'image du joueur

    def verification(self, chemin, grille):
        """
            Fonction qui teste la validité d'un chemin et affichera le message "Bravo" ou "Perdu" sur la grille

        Args:
            chemin (list of tuples): le chemin parcouru
            grille (list of lists): la grille actuelle
        """
        if departArrivee(chemin, grille) and cheminContinu(chemin) and ordreDesCases(chemin, grille): #Si le chemin est valide (alternance des case, chemin continu et part du départ et arrive a l'arrivée)
            self.reponse.set("Bravo") #Affiche le message "Bravo" sur la grille
        else:
            self.reponse.set("Perdu") #Affiche le message "Perdu" sur la grille

game = Game() #Crée un objet game
game.geometry("1280x720") #défini la taille de la fenêtre
game.mainloop() #boucle la fenetre