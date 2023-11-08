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
# Le tour de jeu commencera par le personnage 1
tour_personnage = 1

# Largeur et hauteur de la barre de vie
largeur_barre_max = 250  # Largeur maximale de la barre de vie
hauteur_barre = 20  # Hauteur de la barre de vie

# Liste des arènes disponibles
arenes = ["Champ de bataille", "Place Delfino", "Pont Ordinn"]

#jump
taille_saut = 56
floor=300
# mouvement perso
pvitesse_mouv_haut = 150  # vitesse de mouvement du personnage en montée (vers le haut)
pvitesse_mouv_bas = 150  # vitesse de mouvement du personnage en descente (vers le haut)
monte = False
descente = False



class perso:

    def __init__(self, name, image, pv_init, pv_courant, forceinit, force, position=(0,0)):
        self.name=name #type==str
        self.position= position #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.forceinit=forceinit  #type==int pour les 3   
        self.force=force #force au début et à la fin de la partie
        self.vitesse=-180 #vitesse de saut
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

        """cette methode permet de calculer la faiblesse des personnages au fil de la partie """

        if self.pv_courant<0.5*self.pv_init:
            nf=int(self.force-0.10*self.force)
            self.set_force(nf)
        if self.pv_courant<0.25*self.pv_init:
            nf=int(self.force-0.1*self.force)
            self.set_force(nf)


    def frappe(self,perso1):
        """
        celle ci permet de faire perdre des point a adversaire
        elle prend en parametre le perso1 et self?
        """
        perso1.set_pv_courant(int(perso1.pv_courant-self.force)) 

    def est_frappe(self,perso1):
        """
        celle ci permet de recevoire les coup venant de l'adversaire
        elle prend en parametre le perso1 et self ??
        """
        self.set_pv_courant(int(self.pv_courant-perso1.force))

    def combat(self,perso1):
        """
        cette focntion permet de combattre durant la partie tant que les pv_courant 
        des deux personnages le permette l'un frappe et l'autre recoiu jusqu'a ce que 
        l'un des deux soit a 0 ou moins de pv_courant
        elle prend en parametre le perso1
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

        """cette methode permet de se deplacer a droite, elle utilise la position des personnages, 
        et ajoute 20 ou soustrait 20 a valeur des ordonnées du personnage et fait en sorte qu'aucun 
        de adversaires sortent de l'ecran.
        """

        (x,y)=self.get_position()
        if 0<=x<largeur-170:
            self.set_position(x+60,y)
        else:
            self.set_position(x-60,y)
    def gauche(self):

        """
        cette methode permet de ce deplacer a gauche, elle utilise la position des personnages, 
        et soustrait 20 ou ajoute 20 a valeur des ordonnées du personnage, permet aussi de ne pas sortir de l'ecran.
        """

        (x,y)=self.get_position()
        if 20<=x<=largeur-170:
            self.set_position(x-60,y)
        else:
            self.set_position(x+60,y)
        
    def reset(self):

        """ 
        elle permet de mettre les compteurs initiaux a leurs valeur de base après chaque partie    
        """

        self.pv_courant=self.pv_init
        self.forcecourante=self.forceinit
        self.vitesse=-180 #vitesse de saut
        self.saute=0
        self.saut_duree=0

    def sauter(self):

        """permet de lancer l'action sauter """

        if self.saute ==0:
            self.saute = 1
     
    
    def update(self):

        """change la hauteur du perso pr effectuer un saut puis redescendre grace à une "gravité" """
        (x,y)=self.get_position()
        if self.saute == 1: # si l'action sauter est lancée
            self.saut_duree += 1 
            y -= 5
            self.set_position(x,y)
        if self.saut_duree == 50:
            self.saute = 2 # lorsque le perso arrive en haut du saut
            self.saut_duree = 0
        if self.saute == 2 and y <= floor :
            y += 6 #gravite sup à la vitesse du saut
            self.set_position(x,y)
            if y >= floor:
                y = floor
        if y >= floor:
            self.saute = 0
            self.set_position(x,y)


    
    
#création des persos
pit1=perso("Pit","images/pit.png", 400,400, 50, 50)
pit2=perso("Pit","images/pit.png", 400,400, 50, 50)
mario1=perso("Mario","images/mario.png", 450, 450, 30, 30) 
mario2=perso("Mario","images/mario.png", 450, 450, 30, 30)     
ike1 = perso("Ike","images/ike.png",500, 500, 20, 20)
ike2 = perso("Ike","images/ike.png",500, 500, 20, 20)
#liste des persos disponibles 
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
    #méthode qui affiche le perso choisi, ne marche que lorsque les options ne sont pas sous forme de chaine de caractères
    def afficher_selectionp(self):
        imgperso = pygame.image.load("images/"+self.selection+".png").convert_alpha()
        imgperso= pygame.transform.scale(imgperso,(220,260))
        ecran.blit(imgperso, (self.x,self.y-300))

class items:
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


    def ajoutpv(self,perso):
        perso.set_pv_courant(perso.get_pv_courant()+self.pvsup)

    def ajoutforce(self,perso):
        perso.set_force(perso.get_force()+self.forcesup)


    def effet(self,perso):
        if self.pvsup!=0:
            self.ajoutpv(perso)
        elif self.forcesup!=0:
            self.ajoutforce(perso)

champi= items("images/champi.png",50)
star= items("images/etoilesup.png",0,10)
badstar= items("images/etoileinf.png",0,-5)
banana= items("images/banana.png",-20)


def ecran_accueil():

    """dans  cette methode met en page l'ecran d'accueil
    elle utilise une image pour le fond d'accueil, elle creer un rectangle pour tout les boutons. 
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
    cette methode permet de lancer le jeu, elle prend en parametre les joueurs 1 et 2 ainsi que l'arene, 
    elle recupere les position des joueurs leurs images associer a chaque personnage elle permet de detecter
    les cliques ou les touches pressées afin de definir une action( A,Z,Q pour le joueur 1; O,P,M pour le joueur 2)
    cette methode permet egalement d'afficher la barre de vie de chaqu'un des joueurs et leurs forces, de se deplacer
    
    """

    mapping1 = {"mario": mario1, "pit": pit1, "ike": ike1} #associer la selection a un obj de la classe perso
    if p1 in mapping1:
        p1=mapping1[p1]
    mapping2 = {"mario": mario2, "pit": pit2, "ike": ike2} #associer la selection a un obj de la classe perso
    if p2 in mapping2:
        p2=mapping2[p2]
            
        
    liste=[champi, star, badstar, banana]#on prend trois items au pif
    i1=random.choice(liste)
    i2=random.choice(liste)
    i3=random.choice(liste)
    
    p1.set_position(100,floor)
    p2.set_position(600,floor)
    (x,y)=p1.get_position()
    (a,b)=p2.get_position()
    #img persos
    imgp1=(pygame.image.load(p1.get_image())).convert_alpha()
    imgp1=pygame.transform.scale(imgp1,(150,150))
    imgp2=(pygame.image.load(p2.get_image())).convert_alpha()
    imgp2=pygame.transform.scale(imgp2,(150,150))
    
    
    imgi1=(pygame.image.load(i1.get_image())).convert_alpha()
    imgi1=pygame.transform.scale(imgi1,(70,70))
    imgi2=(pygame.image.load(i2.get_image())).convert_alpha()
    imgi2=pygame.transform.scale(imgi2,(70,70))
    imgi3=(pygame.image.load(i3.get_image())).convert_alpha()
    imgi3=pygame.transform.scale(imgi3,(70,70))
    
    imgi1bis=pygame.transform.scale(imgi1,(50,50))#pour afficher en haut, plus petite
   
    imgi2bis=pygame.transform.scale(imgi2,(50,50))

    imgi3bis=pygame.transform.scale(imgi3,(50,50))
    posi1=(355,10)
    posi2=(425, 10)
    posi3=(495, 10)
    afficheri1=True#afficher les items 1 a la fois
    afficheri2=False
    afficheri3=False
    i1p1=False
    i2p1=False
    i3p1=False
    i1p2=False
    i2p2=False
    i3p2=False
    
    l=[i1,i2,i3]
    for i in l:
        z=random.randint(0,largeur-70)
        while not((z<x-75 or z>x+155) and(z<a-75 or z>a+155)):#pour que l'objet ne soit pas sur un perso
            z=random.randint(0,largeur-70)
        i.set_position(z,floor+70)#abscisse "au hasard"
    #Boucle infinie du programme
    
    while True:
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
                    pygame.quit()
                if event.key == pygame.K_a:
                    p1.gauche()
                    lastevent="a"
                if event.key == pygame.K_z:
                    p1.droite()
                    lastevent="z"
                if event.key == pygame.K_o:
                    p2.gauche()
                    lastevent="o"
                if event.key == pygame.K_p:
                    p2.droite()
                    lastevent="p"
                if event.key == pygame.K_q:
                    p1.sauter()
                    
                if event.key == pygame.K_m:
                    p2.sauter()
                    
        if rect1.colliderect(rect2) and (lastevent=="z" or lastevent=="a"):
            p1.frappe(p2)
            p1.gauche()
            p2.droite()
            if p2.get_force()>=15:
                p2.faiblesse()
        elif rect1.colliderect(rect2) and (lastevent=="o" or lastevent=="p"):#si les perso se chevauchent et le joueur2 est le dernier
            p2.frappe(p1)#à avoir effectué un mouvement, l'attaque s'effectue sur joueur1
            p1.gauche()#les deux persos s'éloignent l'un de l'autre
            p2.droite()# sauf dans le cas où ils sont au bords de la fenêtre
            if p1.get_force()>=15:#si sa force est sup à 10
                p1.faiblesse()# pour leur eviter de se retrouver avc 0 de force
            
            
        if afficheri1:
            recti1=pygame.Rect(i1.get_position(), (70,70))
            ecran.blit(imgi1, i1.get_position())# afficher un item à la fois
        
            if recti1.colliderect(rect1):
                i1.effet(p1)
                afficheri1=False
                afficheri2=True
                i1p1=True
        
            elif recti1.colliderect(rect2):
                i1.effet(p2)
                afficheri1=False
                afficheri2=True
                i1p2=True
        
        if afficheri2:
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
        
        if afficheri3:
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

    
        ecran.blit(imgi1bis, posi1)
        ecran.blit(imgi2bis, posi2)
        ecran.blit(imgi3bis, posi3)
    

    
        if i1p1:
            posi1=(30, 10)#placement des objets à cote du perso qui l'obtient
        if i1p2:
            posi1=(740, 10)
        if i2p1:
            posi2=(100, 10)
        if i2p2:
            posi2=(670, 10)
        if i3p1:
            posi3=(170, 10)
        if i3p2:
            posi3=(590, 10) 
            
            
            
            
            
        #Affichage des noms des personnages
        ecran.blit(police.render(p1.get_name(), True, couleur2), (x_barre1, 500))
        ecran.blit(police.render(p2.get_name(), True, couleur2), (x_barre2, 500))

        ecran.blit(imgp1, pos_p1)
        ecran.blit(imgp2, pos_p2)
        #Affichage des pv et de la force des personnages
            #Création de la chaine de caractère
        pv1= str(p1.get_pv_courant())+"/"+str(p1.get_pv_init())
        pv2= str(p2.get_pv_courant())+"/"+str(p2.get_pv_init())
        force1=str(p1.get_force())
        force2=str(p2.get_force())
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
        ecran.blit(textef2, (largeur-30,10))


        #Affichage des barres de vie des personnages
            #Calcul de la largeur de la barre en pourcentage par rapport à son nombre de pv
        largeur_barre_actuelle1 = (p1.get_pv_courant()* largeur_barre_max)/p1.get_pv_init()
        largeur_barre_actuelle2 = (p2.get_pv_courant()* largeur_barre_max)/p2.get_pv_init()
            #Affichage du rectangle de barre de vie à l'écran
        pygame.draw.rect(ecran, couleur_barre, (x_barre1, y_barre1, largeur_barre_actuelle1, hauteur_barre))
        pygame.draw.rect(ecran, couleur_barre, (x_barre2, y_barre2, largeur_barre_actuelle2, hauteur_barre))

        #update pour le jump
        p1.update()
        p2.update()

        #Lorsque l'un des deux personnages a ses pv égaux ou inférieurs à 0 alors le jeu s'arrête
        if p1.get_pv_courant() <= 0 or p2.get_pv_courant()<=0:
            return ecran_fin(p1,p2)

        #Actualisation de la fenêtre (obligatoire c'est ce qui actualise l'affichage de la fenêtre)
        pygame.display.flip()

def ecran_fin(p1,p2):
    """
    cette methode nous permet d'afficher une page de fin apres la partie qui affiche le gagnant 
    et les bouton rejouer/quitter 
    """
    #Chargement, redimension de l'image de fond de l'écran d'accueil
    fond_fin = pygame.image.load("images/fond_pagef.jpg").convert()
    fond_fin = pygame.transform.scale(fond_fin, (largeur, hauteur))
    #bouton start
    bouton_start = pygame.Rect(320, 110, 200, 50) #coordonnées en x, coordonnées en y, largeur, hauteur
    #Définition du bouton quitter qui servira à quitter le jeu
    bouton_quitter = pygame.Rect(320, 200, 200, 50)
    #Boucle infinie de la page d'accueil (obligatoire car l'affichage doit se faire en continue
    while True:
        #Attention !: Il faut afficher en premier ce qui sera tout en dessous puis
        #ce qu'on affichera ensuite va venir se superposer par dessus

        #Affichage du fond d'écran
        ecran.blit(fond_fin, (0, 0))

        #Affichage du rectangle du bouton start
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
                    pygame.quit()
        
        pygame.display.flip()


     
ecran_accueil()

#Fermeture du module pygame à la fin du programme
pygame.quit()
