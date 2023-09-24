#import pygame
class perso:
    def _init_(self, name, position, image, pv_init, pv_courant, force):
        self.name=name #type==str
        self.position=position  #type==tuple (x,y)
        self.image=image #adresse du chemin d'accès type==str
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.force=force  #type==int pour les 3
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
    def set_position(self,np):
        self.position=np
    def set_image(self,ni):
        self.image=ni
    def set_pv_init(self,npvi):
        self.pv_init=npvi
    def set_pv_courant(self,npvc):
        self.pv_courant=npvc
    def set_force(self,nf):
        self.force=nf
    
