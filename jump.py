jump = False
taille_saut = 56
floor=300
# mouvement perso
pvitesse_mouv_haut = 7  # vitesse de mouvement du personnage en montée (vers le haut)
pvitesse_mouv_bas = 8  # vitesse de mouvement du personnage en descente (vers le haut)
monte = False
descente = False

    if pyxel.btn(pyxel.KEY_SPACE):
            p1.jump()
def jump(self):
    (x,y)=self.get_position()
    if floor - taille_saut - 150 <= y and not descente:
           monte = True
    else:  # si la hauteur du saut est atteinte : commencer à descendre
           monte = False
           descente = True
           # si le personage est atterri sur le sol : fin du saut et
           # réinitialisé emplacement (y) pour être bien aligné
           if y + 150 + pvitesse_mouv_bas >= floor:
               descente = False
               y = floor - 150
    if monte:
        y-= pvitesse_mouv_haut
    if descente:
        y += pvitesse_mouv_bas
