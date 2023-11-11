import pygame
import random
pygame.init()

clock=pygame.time.Clock()
clock.tick(60)

(largeur, hauteur) = (850, 600)

#Création de la fenêtre aux bonnes dimensions
ecran = pygame.display.set_mode((largeur, hauteur))

#Définition du nom de la fenêtre : ce sera le nom de votre jeu
pygame.display.set_caption("Smashy")

#Chargement puis définition de l'icone de la fenêtre
image = pygame.image.load("images/Smash_Ball.png").convert()
image=pygame.transform.scale(image,(20,20))
pygame.display.set_icon(image)

# Définition des couleurs utilisées
police = pygame.font.Font(None, 32)  # Utilisation de la police par défaut avec une taille de 32
couleur1 = (255, 255, 255) #blanc
couleur2 =  (0,0,0) #noir
couleur3 = (255,128,0)#orange
couleur_pv = (255, 0, 0) # rouge
couleur_barre = (0, 255, 0) # vert
couleur_bouton = (0, 0, 255) # bleu
couleur_menu = (0,0,255) # bleu

x_barre1 = 100
y_barre1 = 550
x_barre2=550
y_barre2=550

#### Paramètres sonores ####

# Chargement et lancement d'une musique de fond (-1 pour la mettre en continu)
pygame.mixer.music.load('musiques/smashtheme.mp3')
pygame.mixer.music.play(-1)

#### Paramètres du jeu ###

# Largeur et hauteur de la barre de vie
largeur_barre_max = 250  # Largeur maximale de la barre de vie
hauteur_barre = 20  # Hauteur de la barre de vie

# Liste des arènes disponibles
arenes = ["Champ de bataille", "Place Delfino", "Pont Ordinn"]
#ordonée minimale/ sol du jeu
floor=300


class perso:

    def __init__(self, name, image, pv_init, pv_courant, forceinit, force, position=(0,0)):
        self.name=name #type==str
        self.position= position #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.forceinit=forceinit  #type==int pour les 3   
        self.force=force #force au début et à la fin de la partie
        self.saute=0
        self.saut_duree=0


    def get_name(self):
        return self.name
    def get_position(self):
        return self.position
    def get_image(self):
        return self.image
    def get_pv_init(self):
        return self.pv_init
    def get_pv_courant(self):
        return self.pv_courant
    def get_force_init(self):
        return  self.forceinit
    def get_force(self):
        return  self.force
    def set_name(self,nn):
        self.name=nn
    def set_position(self,x,y):
        self.position=(x,y)
    def set_image(self,ni):
        self.image=ni
    def set_pv_init(self,npvi):
        self.pv_init=npvi
    def set_pv_courant(self,npvc):
        self.pv_courant=npvc
    def set_force(self,nf):
        self.force=nf

    def faiblesse(self):

        """cette methode permet d'appliquer une "faiblesse" sur personnages au fil de la partie 
        diminuant leur force en fonction de leurs pv"""

        if self.pv_courant<0.5*self.pv_init:# -50% pv= -10% force
            nf=int(self.force-0.10*self.force)
            self.set_force(nf)
        if self.pv_courant<0.25*self.pv_init:# pareil lorsque pv<25% pv initiaux
            nf=int(self.force-0.10*self.force)
            self.set_force(nf)# redéfinition de la force


    def frappe(self,perso1):
        """
        methode qui soustrait la force de self aux pv de perso1
        elle prend deux objets de la classe perso en paramètre
        """
        perso1.set_pv_courant(int(perso1.pv_courant-self.force)) #int pour eviter les float

    def est_frappe(self,perso1):
        """
        méthode inverse de frappe:soustrait la force de perso1 aux pv de self
        elle prend deux objets de la classe perso en paramètre
        """
        self.set_pv_courant(int(self.pv_courant-perso1.force))

    def combat(self,perso1):
        """
        cette methode permet de combattre durant la partie tant que les pv_courant 
        des deux personnages le permette elle utilise la méthode frappe et est_frappé 
        elle prend en parametre deux objets de la classe perso
        """

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

        """cette methode permet de se deplacer a droite, elle utilise la position du personnage, 
        et ajoute 50  à son abscisse.
        elle prend un objet de la classe perso en paramètre
        """
        (x,y)=self.get_position()
        if 0<=x<largeur-150: # comprise dans la fenetre (150 pour la taille de l'image de self)
            self.set_position(x+50,y)

    def gauche(self):

        """
        cette methode permet de se deplacer a gauche, elle utilise la position du personnage, 
        et soustrait 50 à son abscisse.
        elle prend un objet de la classe perso en paramètre
        """
        (x,y)=self.get_position()
        if 20<=x<=largeur-150:
            self.set_position(x-50,y)
        
    def reset(self):

        """ 
        elle remet les variables a leurs valeurs initiales   
        """

        self.pv_courant=self.pv_init
        self.force=self.forceinit
        self.saute=0
        self.saut_duree=0

    def sauter(self):

        """permet de lancer l'action sauter """

        if self.saute ==0:
            self.saute = 1
     
    
    def update(self):

        """change la hauteur du perso petit à petit pr effectuer un saut puis redescendre grace à une "gravité" """
        (x,y)=self.get_position()
        if self.saute == 1: # si l'action sauter est lancée
            self.saut_duree += 1 
            y -= 5
            self.set_position(x,y)
        if self.saut_duree == 40: # permet de definir la vitesse du saut
            self.saute = 2 # lorsque le perso arrive en haut du saut
            self.saut_duree = 0
        if self.saute == 2 and y <= floor :#seulement si self est en haut du saut alors il redescend
            y += 6 #gravite sup à la vitesse du saut
            self.set_position(x,y)#obligatoire pour que le mouvement du perso soit visible
            if y >= floor:#si il arrive en dessousdu sol
                y = floor
        if y >= floor:
            self.saute = 0
            self.set_position(x,y)


    
    
#création des objets de la classe perso
pit1=perso("Pit","images/pit.png", 400,400, 50, 50)
pit2=perso("Pit","images/pit.png", 400,400, 50, 50)
mario1=perso("Mario","images/mario.png", 450, 450, 30, 30) 
mario2=perso("Mario","images/mario.png", 450, 450, 30, 30)     
ike1 = perso("Ike","images/ike.png",500, 500, 20, 20)
ike2 = perso("Ike","images/ike.png",500, 500, 20, 20)
#liste des persos disponibles pour les menus
chperso1=["mario","pit","ike"] 
chperso2=["mario","pit","ike"]


class MenuDeroulant:
    # Constructeur de la classe
    def __init__(self, x, y, largeur, hauteur, options, titre, selection):
        self.x=x
        self.y=y
        self.rect = pygame.Rect(x, y, largeur, hauteur) # On crée un rectangle aux coordonnées (x,y)
        self.options = options # Liste de chaines de caractère contenant les options disponibles
        self.ouvert = False  # Le menu déroulant est fermé initialement
        self.selection = selection # Par défaut on choisit une selection
        self.titre = titre # titre affiché sur le Menu

    # Méthode permettant d'afficher le menu à l'écran
    def afficher(self, ecran):
        #Affichage du rectangle de couleur de la taille et des coordonnées définie dans l'attribut rect
        pygame.draw.rect(ecran, couleur_menu, self.rect)
        #Récupération du titre dans l'attribut titre et création du texte
        texte_menu = police.render(self.titre, True, couleur1)
        #Affichage du texte aux mêmes coordonnées que le rectangle + 10 (permet de le centrer)
        ecran.blit(texte_menu, (self.rect.x + 10, self.rect.y + 10))

        #Si le menu est ouvert (donc si l'utilisateur a cliqué dessus)
        if self.ouvert:
            for i in range(len(self.options)):
                y_offset = (i + 1) * 30  # Espacement vertical entre les options
                #On construit un rectangle espacé avec le bon décalage et de taille 30
                option_rect = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 30)
                #On affiche le rectangle à l'écran avec la couleur souhaitée
                pygame.draw.rect(ecran, couleur_menu, option_rect)
                #On crée le texte affiché sur le rectangle d'option
                texte_option = police.render(self.options[i], True, couleur1)
                #On affiche le texte aux même coordonnées que le rectangle + 10
                ecran.blit(texte_option, (option_rect.x + 10, option_rect.y + 10))

    # Méthode qui détecte le clic sur le menu et va l'ouvrir pour afficher les options
    def gerer_clic(self, event):
        #Détection du clic sur le menu déroulant
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                #Si le menu est ouvert, il le ferme alors que s'il est fermé il l'ouvre
                self.ouvert = not self.ouvert
            #Si le menu est ouvert
            elif self.ouvert:
                for i in range(len(self.options)):
                    #Recalcul des positions des rectangles d'options
                    y_offset = (i + 1) * 30
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 30)
                    #Détection du clic sur la position d'un des rectangles d'options
                    if option_rect.collidepoint(event.pos):
                        #Affectation de l'option sélectionnée dans l'attribut sélection
                        self.selection = self.options[i]
                        #Fermeture du menu déroulant
                        self.ouvert = False
                        #Le titre du menu déroulant devient l'option sélectionnée
                        self.titre= self.selection
    #méthode supplémentaire qui affiche le perso choisi, ne marche que lorsque les options sont sous forme de chaine de caractères
    def afficher_selectionp(self):
        imgperso = pygame.image.load("images/"+self.selection+".png").convert_alpha()
        imgperso= pygame.transform.scale(imgperso,(220,260))#redimensionnage
        ecran.blit(imgperso, (self.x,self.y-300))#affichage

class items:#classe supp
    def __init__(self,image,pvsup=0,forcesup=0,position=(0,0)):
        self.image=image
        self.position=position
        self.pvsup=pvsup
        self.forcesup=forcesup

    def get_position(self):
        return self.position
    def get_image(self):
        return self.image
    def get_pvsup(self):
        return self.pvsup
    def get_forcesup(self):
        return  self.forcesup
    def set_position(self,x,y):
        self.position=(x,y)
    def set_image(self,ni):
        self.image=ni
    #setter pour la force et les pv inutiles


    def ajoutpv(self,perso):
        """méthode qui ajoute à un objet de la classe perso les pv que contient self"""
        perso.set_pv_courant(perso.get_pv_courant()+self.pvsup)

    def ajoutforce(self,perso):
        """méthode qui ajoute à un objet de la classe perso la force que contient self"""
        perso.set_force(perso.get_force()+self.forcesup)


    def effet(self,perso):
        """application des methodes précédentes en fonction des attributs de self"""
        if self.pvsup!=0:
            self.ajoutpv(perso)
        elif self.forcesup!=0:
            self.ajoutforce(perso)

#création objets de la classe items
champi= items("images/champi.png",50)
star= items("images/etoilesup.png",0,10)
badstar= items("images/etoileinf.png",0,-5)
banana= items("images/banana.png",-20)


def ecran_accueil():

    """fonction qui affiche l'ecran d'accueil
    elle utilise une image pour le fond d'accueil, elle creer un rectangle pour les boutons. 
    elle fait aussi apparaitre les menus deroulant pour le choix des personnages et le choix de l'arene.
    
    """

    #Chargement, redimension de l'image de fond de l'écran d'accueil
    fond_accueil = pygame.image.load("images/pokemon_accueil.png").convert()
    fond_accueil = pygame.transform.scale(fond_accueil, (largeur, hauteur))

    #Définition du bouton start qui servira à lancer le jeu
    bouton_start = pygame.Rect(320, 110, 200, 50) #coordonnées en x, coordonnées en y, largeur, hauteur
    #Définition du bouton quitter qui servira à quitter le jeu
    bouton_quitter = pygame.Rect(320, 200, 200, 50)
    #Définition d'une instance de menu déroulant qui servira à choisir l'arene du jeu
    menu = MenuDeroulant(320, 400, 200, 40, arenes, "Choisir une arène", "Place Delfino")
    #menus de choix des persos pour les joueurs 1 et 2
    choixperso1 =MenuDeroulant(50, 450, 200, 40, chperso1, "Choisir un perso", "mario")
    choixperso2 =MenuDeroulant(600, 450, 200, 40, chperso2, "Choisir un perso", "pit")

    #Boucle infinie de la page d'accueil (obligatoire car l'affichage doit se faire en continu)
    while True:
        #Attention !: Il faut afficher en premier ce qui sera tout en dessous puis
        #ce qu'on affichera ensuite va venir se superposer par dessus

        #Affichage du fond d'écran
        ecran.blit(fond_accueil, (0, 0))

        #Affichage du rectangle du bouton start
        pygame.draw.rect(ecran, couleur_bouton, bouton_start)
        pygame.draw.rect(ecran, couleur_bouton, bouton_quitter)
        #Affichage du texte du bouton start
        texte_start = police.render("Start", True, couleur1)
        ecran.blit(texte_start, (390, 125))
        #Affichage du texte du bouton quitter
        texte_quitter = police.render("Quitter", True, couleur1)
        ecran.blit(texte_quitter, (385, 215))
        #affichage du texte du choix des persos
        txt_p1=police.render("Joueur 1", True, couleur1)
        txt_p2=police.render("Joueur 2", True, couleur1)
        ecran.blit(txt_p1, (100,100))
        ecran.blit(txt_p2, (650,100))
        #Affichage du menu déroulant des arènes et des persos
        menu.afficher(ecran)
        choixperso1.afficher(ecran)
        choixperso2.afficher(ecran)
        choixperso1.afficher_selectionp()
        choixperso2.afficher_selectionp()
        #Récupération de tous les évènements captés par la fenêtre
        for event in pygame.event.get():

            #Si l'utilisateur a cliqué sur la croix
            if event.type == pygame.QUIT:
                #Fermeture de la fenêtre en quittant pygame
                pygame.quit()

            #Si l'utilisateur a cliqué dans la fenêtre
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Si le clic a été fait à la position du bouton_start
                if bouton_start.collidepoint(event.pos):
                    #On lance le jeu avec comme paramètre l'arêne qui a été choisie
                    return jeu(menu.selection, choixperso1.selection, choixperso2.selection)
                if bouton_quitter.collidepoint(event.pos):
                    pygame.quit()
            #Lancement de la méthode gérer clic qui va capter les évènement de clic sur les options des menus
            menu.gerer_clic(event)
            choixperso1.gerer_clic(event)
            choixperso2.gerer_clic(event)

        #Actualisation de la fenêtre (obligatoire c'est ce qui actualise l'affichage de la fenêtre)
        pygame.display.flip()
        

def jeu(arene, p1, p2): #p1 et p2 doivent être des objets de la classe perso

    """
    fonction qui permet de lancer le jeu, elle prend en parametre les joueurs 1 et 2 ainsi que l'arene choisie, 
    elle place les joueurs et leur image associée, elle permet de detecter
    les touches pressées afin de definir une action : sauter aller à droite ou à gauche
    cette methode permet egalement d'afficher la barre de vie de chaqu'un des joueurs
    et leurs forces, leur nom, chaque objet qu'il recupere.
    
    """

    mapping1 = {"mario": mario1, "pit": pit1, "ike": ike1} #associer la selection du menu a un obj de la classe perso
    if p1 in mapping1:
        p1=mapping1[p1]
    mapping2 = {"mario": mario2, "pit": pit2, "ike": ike2} #associer la selection du menu a un obj de la classe perso
    if p2 in mapping2:
        p2=mapping2[p2]
            
        
    liste=[champi, star, badstar, banana]#on prend trois items au pif
    i1=random.choice(liste)
    i2=random.choice(liste)
    i3=random.choice(liste)
    
    p1.set_position(100,floor)#on place les persos à leur position de base
    p2.set_position(600,floor)
    
    #img persos
    imgp1=(pygame.image.load(p1.get_image())).convert_alpha()
    imgp1=pygame.transform.scale(imgp1,(150,150))
    imgp2=(pygame.image.load(p2.get_image())).convert_alpha()
    imgp2=pygame.transform.scale(imgp2,(150,150))
    
    #images items
    imgi1=(pygame.image.load(i1.get_image())).convert_alpha()#images itemssur le plateau
    imgi1=pygame.transform.scale(imgi1,(70,70))
    imgi2=(pygame.image.load(i2.get_image())).convert_alpha()
    imgi2=pygame.transform.scale(imgi2,(70,70))
    imgi3=(pygame.image.load(i3.get_image())).convert_alpha()
    imgi3=pygame.transform.scale(imgi3,(70,70))
    
    imgi1bis=pygame.transform.scale(imgi1,(50,50))#pour afficher en haut, plus petite les images des items
   
    imgi2bis=pygame.transform.scale(imgi2,(50,50))

    imgi3bis=pygame.transform.scale(imgi3,(50,50))

    posi1=(355, 20) # affichage des items en haut de la page avant qu'ils soient récupérés
    posi2=(425, 20)
    posi3=(495, 20)

    afficheri1=True#pour gerer l'apparition des items
    afficheri2=False
    afficheri3=False

    i1p1=False # variables permettant de savoir qui obtient les items
    i2p1=False #pour ensuite les afficher a cote de la force de celui ci
    i3p1=False
    i1p2=False
    i2p2=False
    i3p2=False
    (x,y)=p1.get_position()
    (a,b)=p2.get_position()
    l=[i1,i2,i3]
    for i in l: # choisie une abscisse aléatoire avant le lancement du jeu: les items peuvent apparaitrent sur un perso qui le récupère immédiatemment
        z=random.randint(0,largeur-70)# 
        while not((z<x-75 or z>x+155) and(z<a-75 or z>a+155)):#pour que au moins le premier objet ne soit pas sur un perso
            z=random.randint(0,largeur-70)
        i.set_position(z,floor+70)#abscisse "au hasard"
    #Boucle infinie du programme
    continuer = True
    
    while continuer:
        pos_p1 = p1.get_position()
        pos_p2 = p2.get_position()

        (x,y)=p1.get_position()
        (a,b)=p2.get_position()

        rect1=pygame.Rect(p1.get_position(), (150,150))
        rect2=pygame.Rect(p2.get_position(), (150,150))
        #Chargement et redimension de l'image de fond d'écran dont le nom est passé en paramètre
        fond = pygame.image.load("images/"+arene+".jpg").convert()
        fond = pygame.transform.scale(fond, (largeur, hauteur))

        #Affichage de l'image de fond
        ecran.blit(fond, (0, 0))

        
        lastevent=""

        #Récupération de tous les évènements captés par la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_SPACE: 
                    continuer = False

                if event.key == pygame.K_q:
                    p1.gauche()
                    lastevent="q"
                if event.key == pygame.K_d:
                    p1.droite()
                    lastevent="d"
                if event.key == pygame.K_k:
                    p2.gauche()
                    lastevent="k"
                if event.key == pygame.K_m:
                    p2.droite()
                    lastevent="m"

                if event.key == pygame.K_z:
                    p1.sauter()
                    
                if event.key == pygame.K_o:
                    p2.sauter()
                    
        if rect1.colliderect(rect2) and (lastevent=="q" or lastevent=="d"):#lorsque contact et p1 est le dernier à s'être déplacé
            p1.frappe(p2)
            if x<a:#s'éloigne vers la gauche si il est a gauche de p2
                p1.gauche()
            elif x>=a:# et inversement
                p1.droite()
            if p2.get_force()>=15:
                p2.faiblesse()
        elif rect1.colliderect(rect2) and (lastevent=="k" or lastevent=="m"):#si les perso se touchent et le joueur2 est le dernier
            p2.frappe(p1)#à avoir effectué un mouvement, l'attaque s'effectue sur joueur1
            #perso 2 s'éloigne
            if x<a:
                p2.droite()
            elif x>=a:
                p2.gauche()
                
            if p1.get_force()>=15:#si sa force est sup à 10
                p1.faiblesse()# pour leur eviter de se retrouver avc 0 de force
            
            
        if afficheri1:#afficher item1
            recti1=pygame.Rect(i1.get_position(), (70,70))
            ecran.blit(imgi1, i1.get_position())# afficher un item à la fois
        
            if recti1.colliderect(rect1):#si joueur 1 le récupère
                i1.effet(p1)
                afficheri1=False# on arrête l'affichage de i1
                afficheri2=True#on lance l'affichage de i2
                i1p1=True
        
            elif recti1.colliderect(rect2):# si c joueur2
                i1.effet(p2)
                afficheri1=False
                afficheri2=True
                i1p2=True
        
        if afficheri2:#pareil avc i2
            recti2=pygame.Rect(i2.get_position(), (70,70))
            ecran.blit(imgi2, i2.get_position())
            if recti2.colliderect(rect1):
                i2.effet(p1)
                afficheri2=False
                afficheri3=True
                i2p1=True
            elif recti2.colliderect(rect2):
                i2.effet(p2)
                afficheri2=False
                afficheri3=True
                i2p2=True
        
        if afficheri3:# et i3
            recti3=pygame.Rect(i3.get_position(), (70,70)) #seulement dans le if pour que les contacts
            ecran.blit(imgi3, i3.get_position())#ne s'opèrent que lorsque l'item s'affiche
            if recti3.colliderect(rect1):
                i3.effet(p1)
                afficheri3=False
                i3p1=True
            elif recti3.colliderect(rect2):
                i3.effet(p2)
                afficheri3=False
                i3p2=True

    
        ecran.blit(imgi1bis, posi1)# affichage des petits items en haut de la fenetre
        ecran.blit(imgi2bis, posi2)
        ecran.blit(imgi3bis, posi3)
    

    
        if i1p1:
            posi1=(10, 25)#placement des objets à cote du perso qui l'obtient
        if i1p2:
            posi1=(760, 25)
        if i2p1:
            posi2=(80, 25)
        if i2p2:
            posi2=(690, 25)
        if i3p1:
            posi3=(150, 25)
        if i3p2:
            posi3=(620, 25) 
            
    
        #Affichage des noms des personnages
        ecran.blit(police.render(p1.get_name(), True, couleur2), (x_barre1, 500))
        ecran.blit(police.render(p2.get_name(), True, couleur2), (x_barre2, 500))

        ecran.blit(imgp1, pos_p1)
        ecran.blit(imgp2, pos_p2)
        #Affichage des pv et de la force des personnages
            #Création de la chaine de caractère
        pv1= str(p1.get_pv_courant())+"/"+str(p1.get_pv_init())
        pv2= str(p2.get_pv_courant())+"/"+str(p2.get_pv_init())
        force1="force joueur1: " + str(p1.get_force())
        force2="force joueur2: " + str(p2.get_force())
            #Création du texte
        texte_pv1 = police.render(pv1, True, couleur_pv)
        texte_pv2 = police.render(pv2, True, couleur_pv)
        #couleur du texte de force qui change
        if p1.get_force()>p1.get_force_init()*0.75:
            textef1=police.render(force1, True, couleur2)
        elif p1.get_force()<p1.get_force_init()*0.75:
            textef1=police.render(force1, True, couleur3)
        if p2.get_force()>p2.get_force_init()*0.75:
            textef2=police.render(force2, True, couleur2)
        elif p2.get_force()<p2.get_force_init()*0.75:
            textef2=police.render(force2, True, couleur3)

            #Affichage du texte à l'écran
        ecran.blit(texte_pv1,(x_barre1,525))
        ecran.blit(texte_pv2,(x_barre2,525))
        ecran.blit(textef1, (10,10))
        ecran.blit(textef2, (largeur-190,10))


        #Affichage des barres de vie des personnages
            #Calcul de la largeur de la barre en pourcentage par rapport à son nombre de pv
        largeur_barre_actuelle1 = (p1.get_pv_courant()* largeur_barre_max)/p1.get_pv_init()
        largeur_barre_actuelle2 = (p2.get_pv_courant()* largeur_barre_max)/p2.get_pv_init()
            #Affichage du rectangle de barre de vie à l'écran
        if p1.get_pv_courant()>p1.get_pv_init()*0.3:# affichage en vert si >30% pv initiaux
            pygame.draw.rect(ecran, couleur_barre, (x_barre1, y_barre1, largeur_barre_actuelle1, hauteur_barre))
        elif p1.get_pv_courant()<p1.get_pv_init()*0.3:#sinon affichageen orange
            pygame.draw.rect(ecran, couleur3, (x_barre1, y_barre1, largeur_barre_actuelle1, hauteur_barre))
        if p2.get_pv_courant()>p2.get_pv_init()*0.3:#pareil pour p2
            pygame.draw.rect(ecran, couleur_barre, (x_barre2, y_barre2, largeur_barre_actuelle2, hauteur_barre))
        elif p2.get_pv_courant()<p2.get_pv_init()*0.3:
            pygame.draw.rect(ecran, couleur3, (x_barre2, y_barre2, largeur_barre_actuelle2, hauteur_barre))
        
        #update pour le jump
        p1.update()
        p2.update()

        #Lorsque l'un des deux personnages a ses pv égaux ou inférieurs à 0 alors le jeu s'arrête
        if p1.get_pv_courant() <= 0 or p2.get_pv_courant()<=0:
            return ecran_fin(p1,p2)

        #Actualisation de la fenêtre
        pygame.display.flip()

def ecran_fin(p1,p2):
    """
    fonction  qui affiche la page de fin apres la partie qui affiche le gagnant 
    et les bouton rejouer/quitter 
    """
    #Chargement, redimension de l'image de fond de l'écran de fin
    fond_fin = pygame.image.load("images/fond_pagef.jpg").convert()
    fond_fin = pygame.transform.scale(fond_fin, (largeur, hauteur))
    #bouton start
    bouton_start = pygame.Rect(320, 110, 200, 50) 
    #Définition du bouton quitter qui servira à quitter le jeu
    bouton_quitter = pygame.Rect(320, 200, 200, 50)
    #Boucle infinie de la page de fin 
    continuer =True
    while continuer:

        #Affichage du fond d'écran
        ecran.blit(fond_fin, (0, 0))

        #Affichage du rectangle du bouton start et quitterddk
        pygame.draw.rect(ecran, couleur_bouton, bouton_start)
        pygame.draw.rect(ecran, couleur_bouton, bouton_quitter)
        #txt bouton restart
        texte_start = police.render("Restart", True, couleur1)
        ecran.blit(texte_start, (390, 125))
        #Affichage du texte du bouton quitter
        texte_quitter = police.render("Quitter", True, couleur1)
        ecran.blit(texte_quitter, (385, 215))
        #variable du texte du gagnant
        txt_p1=police.render("Joueur 1 à Gagné", True, couleur1)
        txt_p2=police.render("Joueur 2 à Gagné", True, couleur1)
        #affichage du gagnant
        if p1.get_pv_courant()<= 0 :
            ecran.blit(txt_p2, (325,300))
        if p2.get_pv_courant()<= 0 :
            ecran.blit(txt_p1, (325,300))
        for event in pygame.event.get():
            #Si l'utilisateur a cliqué dans la fenêtre
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Si le clic a été fait à la position du bouton_start
                if bouton_start.collidepoint(event.pos):
                    p1.reset()
                    p2.reset()
                    return ecran_accueil()
                #Si le clic a été fait à la position du bouton_quitter
                if bouton_quitter.collidepoint(event.pos):
                    continuer = False
        
        pygame.display.flip()


     
ecran_accueil()

#Fermeture du module pygame à la fin du programme
pygame.quit()
