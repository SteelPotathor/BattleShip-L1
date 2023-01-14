# -*- coding: utf-8 -*-

import os

"""
GESTION DES DONNEES
"""


global chemin_absolu
path2 = os.path.realpath(__file__)
split_string = path2.split("\\")
chemin_absolu = ""
for j in range(len(split_string) - 1):
    chemin_absolu += split_string[j] + "\\"


# Définition de la taille des carres du plateau
global TAILLE_DE_CARRES
TAILLE_DE_CARRES = 36

# Définition de la nombre de carres du plateau
global NOMBRE_DE_CARRES
NOMBRE_DE_CARRES = 10

# Définition de la dimension du plateau
global DIMENSION
DIMENSION = TAILLE_DE_CARRES * NOMBRE_DE_CARRES + 1

# Décalage (abscisse) du plateau de placement 
global DEP_X
DEP_X = 225

# Décalage (ordonnée) du plateau de placement
global DEP_Y
DEP_Y = 160

# Définition des matrices contenant les informations de l'état de la partie
global grille
grille1 = [[0 for colonne in range(NOMBRE_DE_CARRES)] for ligne in range(NOMBRE_DE_CARRES)]
grille2 = [[0 for colonne in range(NOMBRE_DE_CARRES)] for ligne in range(NOMBRE_DE_CARRES)]

# Définition du score
global score
score = 0

global vainqueur
vainqueur = 0

global tour
tour = 2

global niv_facile
global niv_moyen
global niv_difficile
niv_facile = False
niv_moyen = False
niv_difficile = False

global flag_partie_prete
flag_partie_prete = False

global coords
coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

global is_on
is_on = True

global calcul_tirs_bot
calcul_tirs_bot = 0

global calcul_tirs_joueur
calcul_tirs_joueur = 0

global calcul_tirs_reussis_bot
calcul_tirs_reussis_bot = 0

global calcul_tirs_reussis_joueur
calcul_tirs_reussis_joueur = 0

global timer
timer = 5

global flip
flip = 0

global duree
duree = 0


# Remise à zéro des grilles
def reInitialisation():
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            grille1[i][j] = 0
            grille2[i][j] = 0
    global vainqueur
    vainqueur = 1


# Remise à zéro du score
def reset_score():
    global score
    score = 0


# Victoire1 et victoire2 en une seule fonction?
def victoire1():
    global vainqueur
    vainqueur = 0
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            if grille1[i][j] == 2:
                vainqueur += 1
    if vainqueur == 17:
        return True
    else:
        return False

def victoire2():
    global vainqueur
    vainqueur = 0
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            if grille2[i][j] == 2:
                vainqueur += 1
    if vainqueur == 17:
        return True
    else:
        return False


def fin_de_partie():
    global flag_partie_prete
    global calcul_tirs_bot, calcul_tirs_joueur
    global calcul_tirs_reussis_bot, calcul_tirs_reussis_joueur
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            if grille1[i][j] != 0 and grille1[i][j] != 3:
                calcul_tirs_bot += 1
            if grille2[i][j] != 0 and grille2[i][j] != 3:
                calcul_tirs_joueur += 1
            if grille1[i][j] == 2:
                calcul_tirs_reussis_bot += 1
            if grille2[i][j] == 2:
                calcul_tirs_reussis_joueur += 1
                print("i=",i," j=",j)
            grille1[i][j] = 4
            grille2[i][j] = 4
    precision_bot = calcul_tirs_reussis_bot / calcul_tirs_bot * 100
    precision_joueur = calcul_tirs_reussis_joueur / calcul_tirs_joueur * 100
    flag_partie_prete = False
    return precision_bot, precision_joueur
