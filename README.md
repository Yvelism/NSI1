# NSI1
projet 1 Imane et Alis

1- Créez une classe Personnage qui contiendra à minima (vous pourrez ajouter ensuite autant d’attributs que vous voudrez si vous en avez besoin) les attributs suivants dans son constructeur :

Un nom : chaine de caractères

Une position à l’écran : tuple (coordonnées en x, coordonnées en y), on peut par défaut placer le personnage à la place (0,0)(Cela le placera dans le coin en haut à gauche dans la fenêtre Pygame)

Une adresse de chemin vers une image : chaine de caractères qui indiquera le chemin pour aller chercher l’image du personnage sous la forme "images/brute1.png" par exemple

Une valeur de points de vie initial : entier représentant les PV maximum initiaux du personnage

Une valeur de points de vie courant : entier , au départ cette valeur sera égale aux PV initiaux, mais dès que le personnage perdra des PV on fera baisser cette valeur

Une valeur de force : entier qui représente la force de frappe du personnage

2- Ajoutez les accesseurs (getters et setters) liés à chacun des attributs de la classe Personnage.

3- Créez une méthode de classe frappe prenant en paramètre un autre personnage et modifiant les PV courants du deuxième personnage en soustrayant ceux-ci par la valeur de force du personnage courant.

4- Créez une méthode de classe est_frappé prenant en paramètre un autre personnage et modifiant les PV courants du personnage courant en soustrayant ceux-ci par la valeur de force du deuxième personnage.

5- Créez une méthode de classe combat prenant en paramètre un autre personnage et en faisant frapper les personnages les uns après les autres jusqu’à ce que l’un des deux PV courants arrive à 0. Elle affiche le gagnant du combat.

6- Intégrez votre classe à l’interface graphique proposée en remplaçant toutes les variables « en dur » liées aux personnages par des personnages créés à l’aide de votre classe. Vous devrez modifier tout le programme pour qu’à chaque fois qu’une variable liée à un personnage était appelée, vous remplaciez cela par l’appel à une méthode de classe pour accéder à l’attribut voulu du personnage. Avant de faire cela assurez-vous d’avoir bien compris le fonctionnement du programme donné en lisant les commentaires, c’est très important.

7- Personnalisez maintenant toute l’interface graphique en modifiant les images, les sons, les titres, les noms des personnages… tout doit changer vous devez vous l’approprier totalement.

8- Ajoutez au moins une autre classe de votre choix dans votre projet : soit une classe pour représenter des armes (par ex : épée qui ajouterai des points d’attaque au personnage, bouclier qui ajouterai des points de défense…), des sorts spéciaux, des lieux, ou n'importe quelle autre classe de votre choix…

9- Créez un nouveau mode de combat un peu plus complexe que le mode de base programmé dans la méthode combat de votre classe Personnage (par ex : ajouter des points de défense aux personnages, ajouter de l’aléatoire avec des attaques qui pourraient échouer…)

10- Ajoutez des menus déroulants sur la page d’accueil en utilisant la classe MenuDeroulant qui vous est fournie, et permettant à chaque joueur de choisir son personnage.

11- Ajoutez une page de fin dans l’interface graphique qui sera appelée à la fin du jeu, sur laquelle sera annoncé le gagnant du combat et qui proposera de rejouer en relançant la page d’accueil.

