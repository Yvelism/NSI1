import pygame
pygame.init()

(largeur, hauteur) = (850, 600)

#Création de la fenêtre aux bonnes dimensions
ecran = pygame.display.set_mode((largeur, hauteur))

#Définition du nom de la fenêtre : ce sera le nom de votre jeu
pygame.display.set_caption("Smashy")

#Chargement puis définition de l'icone de la fenêtre
image = pygame.image.load("perso\ELEVES_LYC\T01\MOLTENIS\Documents\nsi2023\projet1\Projet_POO\Projet POO/accueil.png").convert()
pygame.display.set_icon(image)

# Définition des couleurs utilisées
police = pygame.font.Font(None, 32)  # Utilisation de la police par défaut avec une taille de 32
couleur_texte = (255, 255, 255)  # blanc
couleur_pv = (255, 0, 0) # rouge
couleur_barre = (0, 255, 0) # vert
couleur_bouton = (0, 0, 255) # bleu
couleur_menu = (0,0,255) # bleu



#### Paramètres sonores ####

# Chargement et lancement d'une musique de fond (-1 pour la mettre en continu)
pygame.mixer.music.load('musiques/fond.mp3')
pygame.mixer.music.play(-1)

#### Paramètres du jeu ###
# Le tour de jeu commencera par le personnage 1
tour_personnage = 1

# Largeur et hauteur de la barre de vie
largeur_barre_max = 100  # Largeur maximale de la barre de vie
hauteur_barre = 20  # Hauteur de la barre de vie

# Liste des arènes disponibles
arenes = ["ciel", "foret", "grotte","ring"] 

# on créer toutes les variables dont on aura besoin plus tard


class MenuDeroulant:
    # Constructeur de la classe
    def __init__(self, x, y, largeur, hauteur, options): #defifinition de la classe pour pouvoir créer des menus déroulants 
        self.rect = pygame.Rect(x, y, largeur, hauteur) # On crée un rectangle aux coordonnées (x,y)
        self.options = options # Liste de chaines de caractère contenant les options disponibles
        self.ouvert = False  # Le menu déroulant est fermé initialement
        self.selection = "ciel" # Par défaut on choisit l'arene ciel
        self.titre = "Choisir une arène" # titre affiché sur le Menu

    # Méthode permettant d'afficher le menu à l'écran
    def afficher(self, ecran):
        #Affichage du rectangle de couleur de la taille et des coordonnées définie dans l'attribut rect
        pygame.draw.rect(ecran, couleur_menu, self.rect) # fonction inclue dans pygame qui affiche le rectangle
        #Récupération du titre dans l'attribut titre et création du texte
        texte_menu = police.render(self.titre, True, couleur_texte) 
        #Affichage du texte aux mêmes coordonnées que le rectangle + 10 (permet de le centrer)
        ecran.blit(texte_menu, (self.rect.x + 10, self.rect.y + 10))

        #Si le menu est ouvert (donc si l'utilisateur a cliqué dessus)
        if self.ouvert: #donc si == True
            for i in range(len(self.options)): # pour le nombre d'options qu'on a mis
                y_offset = (i + 1) * 30  # Espacement vertical entre les options
                #On construit un rectangle espacé avec le bon décalage et de taille 30
                option_rect = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 30)
                #On affiche le rectangle à l'écran avec la couleur souhaitée
                pygame.draw.rect(ecran, couleur_menu, option_rect)
                #On crée le texte affiché sur le rectangle d'option
                texte_option = police.render(self.options[i], True, couleur_texte)
                #On affiche le texte aux même coordonnées que le rectangle + 10 pour centrer le texte
                ecran.blit(texte_option, (option_rect.x + 10, option_rect.y + 10))

    # Méthode qui détecte le clic sur le menu et va l'ouvrir pour afficher les options
    def gerer_clic(self, event):
        #Détection du clic sur le menu déroulant
        if event.type == pygame.MOUSEBUTTONDOWN:# event.type c'est le type d'action que fait le joueur et pygame.M... c'est l'action de cliquer
            if self.rect.collidepoint(event.pos): # si le clic est sur le rectangle de base (menu fermé)
                #Si le menu est ouvert, il le ferme alors que s'il est fermé il l'ouvre
                self.ouvert = not self.ouvert#le not permet de faire l'inverse 
            #Si le menu est ouvert
            elif self.ouvert:
                for i in range(len(self.options)): #on parcours chaque options du menu
                    #Recalcul des positions des rectangles d'options
                    y_offset = (i + 1) * 30
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 30)
                    #Détection du clic sur la position d'un des rectangles d'options
                    if option_rect.collidepoint(event.pos): # si le clic est sur une l' options du menu
                        #Affectation de l'option sélectionnée dans l'attribut sélection
                        self.selection = self.options[i]
                        #Fermeture du menu déroulant
                        self.ouvert = False
                        #Le titre du menu déroulant devient l'option sélectionnée
                        self.titre= self.selection




def ecran_accueil(): # première page du jeux 
    #Chargement, redimension de l'image de fond de l'écran d'accueil
    fond_accueil = pygame.image.load("images/accueil.png").convert() #on importe l'image
    fond_accueil = pygame.transform.scale(fond_accueil, (largeur, hauteur)) #on la met à la bonne taille, larg et haut definie au debut du code

    #Définition du bouton start qui servira à lancer le jeu, on ne l'affiche pas encore
    bouton_start = pygame.Rect(320, 200, 200, 50) #coordonnées en x, coordonnées en y, largeur, hauteur

    #Définition d'une instance de menu déroulant qui servira à choisir l'arene du jeu on créerun menu
    menu = MenuDeroulant(100, 200, 200, 30, arenes)#les options sont dans la liste arenes definit au début

    #Boucle infinie de la page d'accueil (obligatoire car l'affichage doit se faire en continu)
    while True:
        #Attention !: Il faut afficher en premier ce qui sera tout en dessous puis
        #ce qu'on affichera ensuite va venir se superposer par dessus

        #Affichage du fond d'écran
        ecran.blit(fond_accueil, (0, 0)) #fonction d'affichage pygame

        #Affichage du rectangle du bouton start
        pygame.draw.rect(ecran, couleur_bouton, bouton_start)#on affiche le rectangle avec les valeurs définits au dessus

        #Affichage du texte du bouton start
        texte_start = police.render("Start", True, couleur_texte)
        ecran.blit(texte_start, (390, 215))#coordonées auquelles le placer

        #Affichage du menu déroulant des arènes
        menu.afficher(ecran)#on utilise la méthode de la classe menu_deroulant

        #Récupération de tous les évènements captés par la fenêtre
        for event in pygame.event.get(): # pour chaque actions du joueur

            #Si l'utilisateur a cliqué sur la croix
            if event.type == pygame.QUIT:
                #Fermeture de la fenêtre en quittant pygame
                pygame.quit()

            #Si l'utilisateur a cliqué dans la fenêtre
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Si le clic a été fait à la position du bouton_start
                if bouton_start.collidepoint(event.pos):
                    #On lance le jeu avec comme paramètre l'arêne qui a été choisie
                    return jeu(menu.selection)
                #ici on pourra rajouter des conditions de lancements en mode "si il a cliquer sur changer de perso"...
            #Lancement de la méthode gérer clic qui va capter les évènement de clic sur les options du menu
            menu.gerer_clic(event) #si il n'a pas cliquer sur start on lance la methode de classe pour gérer son action

        #Actualisation de la fenêtre (obligatoire c'est ce qui actualise l'affichage de la fenêtre)
        pygame.display.flip() # je sais pas ce que c'est mais faut pas l'oublier
        
        
        
        
        
        
def jeu(arene): # création de ce qui s'affiche après l'accueil
    #On précise que ce sont des variables globales et pas locales à la fonction pour éviter les erreurs d'interprêtation
    global pos_brute1,pos_brute2, pv_courant1, pv_courant2, tour_personnage #global permet de rendre les variables utilisables pour toutes les fonctions pas que celle là


    #Boucle infinie du programme comme dans accueil
    continuer = True
    while continuer: # c'est a dire toujours

        #Chargement et redimension de l'image de fond d'écran dont le nom est passé en paramètre
        fond = pygame.image.load("images/"+arene+".jpg").convert() #le +arene permet de charger la bonne image correspondante
        fond = pygame.transform.scale(fond, (largeur, hauteur))# meme chose que plus haut on redimensionne pour que ca rentre dans la fenetre

        #Affichage de l'image de fond
        ecran.blit(fond, (0, 0))
        #Affichage des personnages
        ecran.blit(brute1, pos_brute1) #les position devront venir de nos persos directement avec get_position()
        ecran.blit(brute2, pos_brute2)
        #dans le blit tu mets : ce que tu affiches, où est-ce que tu l'affiche
        #Récupération de tous les évènements captés par la fenêtre
        for event in pygame.event.get(): #pour chaque actions
            #Si l'utilisateur a cliqué sur la croix
            if event.type == pygame.QUIT:
                #Fin de la boucle infinie et le programme se termine
                continuer = False
            # Si c'est au personnage 1 de jouer et que l'utilisateur a tapé sur une touche (le tour du perso est défini à 1 au debut)
            if tour_personnage == 1 and event.type == pygame.KEYDOWN: #n'importe quelle touche
                # Si la touche était la barre d'espace
                if event.key == pygame.K_SPACE:  
                    # Le personnage 1 attaque le personnage 2, cela réduit les pv du personnage 2 de 20
                    pv_courant2 -= 20

                    #Déplacement de l'image du personnage 1 vers le personnage 2
                    pos_brute1 = (500, 300)
                    #Ré-affichage de l'écran
                    ecran.blit(fond, (0, 0))
                    #Ré-affichage des personnages
                    ecran.blit(brute1, pos_brute1)
                    ecran.blit(brute2, pos_brute2)
                    #Re-déplacement du personnage 1 à sa position initiale
                    pos_brute1 = (100, 300)
                    #à remplacer par nos méthode de classe perso , attaquer et est_attaqué
                    #Le tour passe au prochain personnage
                    tour_personnage = 3 - tour_personnage#soit 3-1=2 soit 3-2=1


            #Même chose pour le personnage 2
            elif tour_personnage == 2 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pv_courant1 -= 20
                    pos_brute2 = (200, 300)
                    ecran.blit(fond, (0, 0))
                    ecran.blit(brute1, pos_brute1)
                    ecran.blit(brute2, pos_brute2)
                    pos_brute2 = (600, 300)
                    tour_personnage = 3 - tour_personnage


        #Affichage des noms des personnages
        ecran.blit(nom1, (100, 500))
        ecran.blit(nom2,(600,500))

        #Affichage des pv des personnages
            #Création de la chaine de caractère
        pv1= str(pv_courant1)+"/"+str(pv_inital1)
        pv2= str(pv_courant2)+"/"+str(pv_inital2)
            #Création du texte
        texte_pv1 = police.render(pv1, True, couleur_pv)
        texte_pv2 = police.render(pv2, True, couleur_pv)
            #Affichage du texte à l'écran
        ecran.blit(texte_pv1,(100,525))
        ecran.blit(texte_pv2,(600,525))

        #Affichage des barres de vie des personnages
            #Calcul de la largeur de la barre en pourcentage par rapport à son nombre de pv
        largeur_barre_actuelle1 = (pv_courant1/ 100) * largeur_barre_max
        largeur_barre_actuelle2 = (pv_courant2/ 100) * largeur_barre_max
            #Affichage du rectangle de barre de vie à l'écran
        pygame.draw.rect(ecran, couleur_barre, (x_barre1, y_barre1, largeur_barre_actuelle1, hauteur_barre))
        pygame.draw.rect(ecran, couleur_barre, (x_barre2, y_barre2, largeur_barre_actuelle2, hauteur_barre))

        #Lorsque l'un des deux personnages a ses pv égaux ou inférieurs à 0 alors le jeu s'arrête
        if pv_courant1 <= 0 or pv_courant2<=0:
                 continuer = False

        #Actualisation de la fenêtre (obligatoire c'est ce qui actualise l'affichage de la fenêtre)
        pygame.display.flip()




        
        
#Chargement de l'image en conservant la transparence grâce au convert_alpha (il faut utiliser des .png)
brute1 = pygame.image.load("images/brute1.png").convert_alpha()
#Redimension de l'image
brute1 = pygame.transform.scale(brute1, (150, 150))
#Définition de la position initiale de l'image dans la fenêtre
pos_brute1 = (100, 300)
#Définition du nom du personnage
nom_brute1 = "Lithia la Féroce"
#Création du texte contenant le nom du personnage
nom1 = police.render(nom_brute1, True, couleur_texte)
#Définition des points de vie initiaux et courants
pv_inital1 = 250
pv_courant1 = 120
#Définition des coordonnées de départ de la barre de vie du personnage 1
x_barre1 = 100
y_barre1 = 550
brute2 = pygame.image.load("images/brute2.png").convert_alpha()
brute2 = pygame.transform.scale(brute2, (150,150))
pos_brute2=(600, 300)
nom_brute2="Darian la Lame d'Acier"
nom2 = police.render(nom_brute2, True, couleur_texte)
pv_inital2=250
pv_courant2=240
x_barre2=600
y_barre2=550

# tout ces paramètres de perso doivent disparaitre pour être rangés dans la classe perso qu'on a créer

brute2=perso("luigi","images/brute2.png", 250,240,500,500,(600,550))

brute1=perso("mario","images/brute1.png", 250, 120, 500, 500, (100,550))

class perso:
    def _init_(self, name, image, pv_init, pv_courant, forceinit, force, position=(0,0)):
        self.name=name #type==str
        self.position= position #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.forceinit=forceinit  #type==int pour les 3   
        self.forcecourante=force #force au début et à la fin de la partie

    def get_name(self):
        print(self.name)
    def get_position(self):
        print(self.position)
    def get_image(self):
        print(self.image)
    def get_pv_init(self):
        print(self.pv_init)
    def get_pv_courant(self):
        print(self.pv_courant)
    def get_force(self):
        print(self.force)
    def set_name(self,nn):
        self.name=nn
    def set_positionx(self,npx): #changer la valeur de x pas de la liste entière
        self.position[0]=npx
    def set_positiony(self,npy): # pareil pour y, permet de changer leurs valeurs indépendamment 
        self.position[1]=npy
    def set_image(self,ni):
        self.image=ni
    def set_pv_init(self,npvi):
        self.pv_init=npvi
    def set_pv_courant(self,npvc):
        self.pv_courant=npvc
    def set_force(self,nf):
        self.force=nf

    def faiblesse(self):
        if self.pv_courant<0.5*self.pv_init:
            self.set_force(self.force-0,1*self.force)
        if self.pv_courant<0.25*self.pv_init:
            self.set_force(self.force-0,2*self.force)


    def frappe(self,perso1):
        perso1.set_pv_courant(perso1.pv_courant-self.force) 

    def est_frappe(self,perso1):
        self.set_pv_courant(self.pv_courant-perso1.force)

    def combat(self,perso1):
        while self.pv_courant>0 and perso1.pv_courant>0 :
            self.frappe(perso1)
            if perso1.pv_courant>0:
                self.est_frappe(perso1)
                self.faiblesse()
                perso1.faiblesse()
        if self.pv_courant>perso1.pv_courant:
            return self.name
        else:
            return perso1.get_name()
        
    def droite(self):
        self.position[0]+=10
    def gauche(self):
        self.position[0]-=10

    def reset(self):
        self.pv_courant=self.pv_init
        self.forcecourante=self.forceinit

class items:
    def _init_(self,pvsup,forcesup,pvinf,forceinf,position=(0,0)):
        self.position=position
        self.pvsup=pvsup
        self.forcesup=forcesup
        self.pvinf=pvinf
        self.forceinf=forceinf

    def ajoutpv(self,perso):
        perso.set_pv_courant(perso.get_pv_courant+self.pvsup)

    def ajoutforce(self,perso):
        perso.set_force(perso.get_force+self.forcesup)

    def maluspv(self,perso):
        perso.set_pv_courant(perso.get_pv_courant+self.pvinf)

    def malusforce(self,perso):
        perso.set_force(perso.get_force+self.forceinf)


    
class arene:
    def _init_(self,background,platform,sound):
        self.background=background #image
        self.platform=platform #liste de plateforme
        self.sound=sound #bande son attitrée
        
ecran_accueil()

#Fermeture du module pygame à la fin du programme
pygame.quit()
