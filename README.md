# Mazegame_SenseHat

Projet de jeu de labyrinthe multijoueurs sur Raspberry-SenseHat.

La version solo du jeu et sans Raspberry est disponible à cette adresse:
https://trinket.io/python/714c062a5e

Descriptif des fichiers:

- mazegen.py: générateur de labyrinthe, selon le tutoriel suivant: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

- mazegame.py: moteur du jeu qui calcule les positions des joueurs, leur vision du labyrinthe selon leur position et leurs déplacements

- player.py: récupère les données du joystick SenseHat manipulé par le joueur et le communique à broker.py (via MQTT) puis réceptionne les données de la grille et de la position du joueur envoyées par broker.py (toujours via MQTT) pour l'afficher sur les Led du SenseHat

- broker.py: récupère les données envoyées par player puis calcule l'état du jeu à l'aide du moteur mazegame, puis restitue la grille à chacun des joueurs selon leur position

- digit_grid: un petit module qui affiche un nombre à 2 chiffres sur les Led du SenseHat; dans ce projet, sert uniquement à afficher le classement d'un joueur qui vient de résoudre le labyrinthe
