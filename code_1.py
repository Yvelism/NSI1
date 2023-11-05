import pygame
pygame.init()

(largeur, hauteur) = (850, 600)

#Création de la fenêtre aux bonnes dimensions
ecran = pygame.display.set_mode((largeur, hauteur))

#Définition du nom de la fenêtre : ce sera le nom de votre jeu
pygame.display.set_caption("Smashy")

#Chargement puis définition de l'icone de la fenêtre
image = pygame.image.load("Projet POO/imgprof/accueil.png").convert()
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
pygame.mixer.music.load('musique/smashtheme.mp3')
pygame.mixer.music.play(-1)

#### Paramètres du jeu ###
# Le tour de jeu commencera par le personnage 1
tour_personnage = 1

# Largeur et hauteur de la barre de vie
largeur_barre_max = 250  # Largeur maximale de la barre de vie
hauteur_barre = 20  # Hauteur de la barre de vie

# Liste des arènes disponibles
arenes = ["Champ de bataille", "Place Delfino", "Pont Ordinn"]

class perso:
    
    def __init__(self, name, image, pv_init, pv_courant, forceinit, force, position=(0,0)):
        self.name=name #type==str
        self.position= position #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.forceinit=forceinit  #type==int pour les 3   
        self.force=force #force au début et à la fin de la partie


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
        if self.pv_courant<0.5*self.pv_init:
            nf=int(self.force-0.10*self.force)
            self.set_force(nf)
        if self.pv_courant<0.25*self.pv_init:
            nf=int(self.force-0.1*self.force)
            self.set_force(nf)


    def frappe(self,perso1):
        perso1.set_pv_courant(int(perso1.pv_courant-self.force)) 

    def est_frappe(self,perso1):
        self.set_pv_courant(int(self.pv_courant-perso1.force))

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
        (x,y)=self.get_position()
        if 0<=x<largeur-170:
            self.set_position(x+20,y)
        else:
            self.set_position(x-20,y)
    def gauche(self):
        (x,y)=self.get_position()
        if 20<=x<=largeur-170:
            self.set_position(x-20,y)
        else:
            self.set_position(x+20,y)
        
    def reset(self):
        self.pv_courant=self.pv_init
        self.forcecourante=self.forceinit
    
#création des persos
pit=perso("Pit","images/pit.png", 400,400, 50, 50)
mario=perso("Mario","images/mario.png", 450, 450, 30, 30)     
ike = perso("Ike","images/ike.png",500, 500, 20, 20)
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




def ecran_accueil():
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
        txt_p1=police.render("Joueur 1", True, couleur2)
        txt_p2=police.render("Joueur 2", True, couleur2)
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
    #On précise que ce sont des variables globales et pas locales à la fonction pour éviter les erreurs d'interprêtation
    global tour_personnage, pos_p1, pos_p2
    mapping = {"mario": mario, "pit": pit, "ike": ike} #associer la selection a un obj de la classe perso
    if p1 and p2 in mapping:
        p1=mapping[p1]
        p2=mapping[p2]

    pos_p1 = p1.set_position(100,300)
    pos_p2 = p2.set_position(600,300)
    #img persos
    imgp1=(pygame.image.load(p1.get_image())).convert_alpha()
    imgp1=pygame.transform.scale(imgp1,(150,150))
    imgp2=(pygame.image.load(p2.get_image())).convert_alpha()
    imgp2=pygame.transform.scale(imgp2,(150,150))
    #Boucle infinie du programme
    
    while True:
        pos_p1 = p1.get_position()
        pos_p2 = p2.get_position()
        rect1=pygame.Rect(p1.get_position(), (150,150))
        rect2=pygame.Rect(p2.get_position(), (150,150))
        #Chargement et redimension de l'image de fond d'écran dont le nom est passé en paramètre
        fond = pygame.image.load("images/"+arene+".jpg").convert()
        fond = pygame.transform.scale(fond, (largeur, hauteur))

        #Affichage de l'image de fond
        ecran.blit(fond, (0, 0))

        ecran.blit(imgp1, pos_p1)
        ecran.blit(imgp2, pos_p2)
        lastevent=""
        #Récupération de tous les évènements captés par la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p1.gauche()
                    ecran.blit(imgp1, pos_p1)
                    lastevent="a"
                if event.key == pygame.K_z:
                    p1.droite()
                    ecran.blit(imgp1, pos_p1)
                    lastevent="z"
                if event.key == pygame.K_o:
                    p2.gauche()
                    ecran.blit(imgp2, pos_p2)
                    lastevent="o"
                if event.key == pygame.K_p:
                    p2.droite()
                    ecran.blit(imgp2, pos_p2)
                    lastevent="p"
        if rect1.collidepoint(pos_p2) and lastevent=="z":
            p1.frappe(p2)
            p1.gauche()
            p2.droite()
            if p2.get_force()>=10:
                p2.faiblesse()
        elif rect1.collidepoint(pos_p2) and lastevent=="o":
            p2.frappe(p1)
            p1.gauche()
            p2.droite()
            if p1.get_force()>=10:
                p1.faiblesse()
            
        #Affichage des noms des personnages
        ecran.blit(police.render(p1.get_name(), True, couleur2), (x_barre1, 500))
        ecran.blit(police.render(p2.get_name(), True, couleur2), (x_barre2, 500))

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
        ecran.blit(textef1, (x_barre1+60,125))
        ecran.blit(textef2, (x_barre2+60,125))


        #Affichage des barres de vie des personnages
            #Calcul de la largeur de la barre en pourcentage par rapport à son nombre de pv
        largeur_barre_actuelle1 = (p1.get_pv_courant()* largeur_barre_max)/p1.get_pv_init()
        largeur_barre_actuelle2 = (p2.get_pv_courant()* largeur_barre_max)/p2.get_pv_init()
            #Affichage du rectangle de barre de vie à l'écran
        pygame.draw.rect(ecran, couleur_barre, (x_barre1, y_barre1, largeur_barre_actuelle1, hauteur_barre))
        pygame.draw.rect(ecran, couleur_barre, (x_barre2, y_barre2, largeur_barre_actuelle2, hauteur_barre))

        #Lorsque l'un des deux personnages a ses pv égaux ou inférieurs à 0 alors le jeu s'arrête
        if p1.get_pv_courant() <= 0 or p2.get_pv_courant()<=0:
            return ecran_fin(p1,p2)

        #Actualisation de la fenêtre (obligatoire c'est ce qui actualise l'affichage de la fenêtre)
        pygame.display.flip()

def ecran_fin(p1,p2):
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

        
     
ecran_accueil()

#Fermeture du module pygame à la fin du programme
pygame.quit()