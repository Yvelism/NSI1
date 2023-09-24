#import pygame
class perso:
    def _init_(self, position, image, pv_init, pv_courant, force):
        self.position=position
        self.image=image
        self.pv_init=pv_init
        self.pv_courant=pv_courant
        self.force=force
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
