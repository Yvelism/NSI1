#import pygame
class perso:
    def _init_(self, name, image, pv_init, pv_courant, force, position=(0,0)):
        self.name=name #type==str
        self.position= position #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.force=force  #type==int pour les 3   

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
    def set_positionx(self,npx):
        self.position[0]=npx
    def set_positiony(self,npy):
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

objet1=items((10,43),20,0,0,0)
objet2=items((20,78),0,0,0,24)


    
class arène:
    def _init_(self,background,platform,sound):
        self.background=background #image
        self.platform=platform #liste de plateforme
        self.sound=sound #bande son attitrée
