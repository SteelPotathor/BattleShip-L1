# -*- coding: utf-8 -*-


"""
GESTION DE L'INTERFACE GRAPHIQUE
"""


# Import des modules et bibliothèques nécessaires à la partie graphique
from multiprocessing.sharedctypes import Value
from tkinter.filedialog import Open
import webbrowser
from Model import *
from tkinter import *
from tkinter import DISABLED, ttk
from tkinter import Tk
from tkinter import colorchooser
from PIL import *
from PIL import ImageTk, Image
from tkinter.ttk import Progressbar
import time
import random
import pygame
import urllib
from pygame import mixer


# Initialise les sons
pygame.mixer.init()


# Exécute la fonction qui crée le launcher (fonction principale de tout le programme, toutes les autres lui sont liées)
def affichage():
    launcherTK()
    
    
    
"""
Partie LAUNCHER
"""


"""
Partie graphique LAUNCHER
"""


# Fonction qui crée le launcher
def launcherTK():
    # Utilisation des fonctions permettant de construire le launcher
    creation_fenetre_launcher()
    creation_wallpaper_launcher()
    creation_load_launcher()
    creation_bouton_launcher()
    
    # Permet de "loop" le programme ce qui donne l'impression d'animation (alors que ce ne sont que des images)
    launcher.mainloop()
    
    
# Fonction créant la fenêtre du launcher ainsi que tout ses attributs (taille, titre...)
def creation_fenetre_launcher():
    #Création d'une fenêtre tkinter launcher
    global launcher
    launcher = Tk()
    
    # Désactive le resize de la fenêtre
    launcher.resizable(0, 0)
    
    # Définition du logo de la fenêtre
    global chemin_absolu
    launcher.iconbitmap(chemin_absolu + "Images//LOGO//ancre.ico")
    
    # Définition du titre de la fenêtre
    launcher.title("Bataille Navale Launcher")
    
    # Définition de la taille de la fenêtre
    LARGEUR_LAUNCHER = 600
    HAUTEUR_LAUNCHER = 400
    
    # Définition de la taille de l'écran (ces valeurs seront réutilisées dans d'autres fenêtres)
    global LARGEUR_ECRAN, HAUTEUR_ECRAN
    LARGEUR_ECRAN = launcher.winfo_screenwidth()
    HAUTEUR_ECRAN = launcher.winfo_screenheight()
    
    # Positionnement de la fenêtre au milieu de l'écran et application de la taille
    x = (LARGEUR_ECRAN / 2) - (LARGEUR_LAUNCHER / 2)
    y = (HAUTEUR_ECRAN / 2) - (HAUTEUR_LAUNCHER / 2)
    # Les 2 premières variables appliquent la taille de la fenêtre tandis que les deux autres positionnent la fenêtre (similaire au padding mais par rapport à l'écran)
    launcher.geometry("%dx%d+%d+%d" %(LARGEUR_LAUNCHER, HAUTEUR_LAUNCHER, x, y))


# Fonction créant un fond d'écran
def creation_wallpaper_launcher():
    # Création d'un canvas qui repose sur l'entièreté de la fenêtre launcher
    global wallpaper_launcher
    wallpaper_launcher = Canvas(launcher,
                                bd = 0,
                                highlightthickness = 0)
    # On étend le canvas à toute la fenêtre
    wallpaper_launcher.pack(fill = "both", expand = True)
    
    # Ouverture d'un fichier image
    global bg_launcher
    global chemin_absolu
    bg_launcher = Image.open(chemin_absolu + "Images//WP//launcher_wp.png")
    
    # Resize du fichier image à la taille de la fenêtre launcher
    global resized_launcher, new_bg_launcher
    resized_bg_launcher = bg_launcher.resize((600, 400), Image.ANTIALIAS)
    new_bg_launcher = ImageTk.PhotoImage(resized_bg_launcher)
    
    # Application de l'image au canvas (permet de créer un fond d'écran)
    wallpaper_launcher.create_image((300, 200), image = new_bg_launcher)


# Fonction créant la barre de chargement dans le launcher
def creation_load_launcher():
    global load
    load = Progressbar(launcher,
                       orient = HORIZONTAL,
                       length = 615)
    
    # Positionnement de la barre de chargement
    load.place(x = -5, y = 385)
    
    
# Fonction créant le bouton du launcher
def creation_bouton_launcher():
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
    def survol(event):
        bouton_launcher.config(background = "#4BD5F5",
                               foreground = "#141414")
            
            
    def fin_survol(event):
        bouton_launcher.config(background = "#141414",
                               foreground = "#4BD5F5")
            
        
    # Création du bouton du launcher
    bouton_launcher = Button(launcher,
                             text = "L A N C E R",
                             bg = "#141414",
                             fg = "#4BD5F5",
                             border = 0,
                             activeforeground = "#4BD5F5",
                             activebackground = "#141414",
                             font = ("Andi", 10),
                             command = bouton_launcher_clic)
    
    # Positionnement du bouton du launcher
    bouton_launcher.place(x = 300, y = 320, anchor = CENTER)
    
    # Attribution des intéractions utilisateurs aux fonctions du dessus (survol...)
    bouton_launcher.bind("<Enter>", survol)
    bouton_launcher.bind("<Leave>", fin_survol)
    

"""
Partie commandes LAUNCHER
"""


# Fonction qui s'applique lors du clic du bouton du launcher
def bouton_launcher_clic():
    # Utilisation des fonctions résultant du clic du bouton launcher
    creation_label()
    progression_load()
    
    # Destruction de la fenêtre tkinter launcher (une fois la barre de progression à 100%)    
    launcher.destroy()
    
    # Appel de la fonction permettant la création d'une nouvelle fenêtre (une fois la fenêtre précédente détruite, on en crée une nouvelle qui contiendra le jeu)
    rootTK()
    
    
# Creation d'un label dans le launcher
def creation_label():
    global label_launcher
    label_launcher = Label(font = ('Benguiat', 20),
                           fg = "white",
                           bg = "#2C9486")
    
    # Positionnement du label
    label_launcher.place(x = 300, y = 360, anchor = CENTER)
    
    # Choix aléatoire parmi une liste d'un texte pour le label
    liste_citations1 = ["Nettoyage",
                       "Chargement",
                       "Vogue...",
                       "Océan=sel"]
    
    choix1 = random.choice(liste_citations1)
    label_launcher.config(text = choix1)
    

# Etat d'avancement de la barre et changement de texte du label en fonction du temps
def progression_load():
    # Initialisation du pourcentage initial de la barre
    compteur = 0
    # La barre passera par 100 états avant de terminer sa course
    for i in range(100):
        load['value'] = compteur
        
        # Actualisation de la barre
        launcher.update_idletasks()
        
        # Temps nécessaire pour avancer de 1% dans la barre
        time.sleep(0.01)
        
        # Après ce temps, on indente le pourcentage
        compteur += 1
        
        if compteur == 15: 
            # Choix aléatoire d'un texte pour le label à t = 15 
            liste_citations2 = ["Création de l'océan",
                               "Ajout de la gravité",
                               "Piou Piou Pam Pam",
                               "Attention à Chtulhu"]
    
            choix2 = random.choice(liste_citations2)
            label_launcher.config(text = choix2)
        
        elif compteur == 35:
            # Choix aléatoire d'un texte pour le label à t = 35
            liste_citations3 = ["Formation des liquides",
                               "Ajout d'étendues d'eau",
                               "Formation des liquides",
                               "Création des cascades",
                               "Désactivation des pièges"]
    
            choix3 = random.choice(liste_citations3)
            label_launcher.config(text = choix3)
        
        elif compteur == 65:
            # Choix aléatoire d'un texte pour le label à t = 65
            liste_citations4 = ["Nettoyage des arrière-plans",
                               "Culture de plantes aquatiques",
                               "Vérification de la radioactivité",
                               "Ne jamais regarder sous l'eau...",
                               "Made by Master Jawad & Master Timothée!"]
    
            choix4 = random.choice(liste_citations4)
            label_launcher.config(text = choix4)
     

"""
Partie graphique ROOT
"""


# Fonction qui crée le root (suite à la fermeture du launcher)
def rootTK():    
    # Utilisation des fonctions permettant de construire le root (avec les frames)
    creation_fenetre_root()
    placement_frame()
    
    # Application de la fonction permettant de choisir le frame la plus haute (calque)    
    affichage_frame(frame_principal)
    
    # Appel de la fontion meublant la fenêtre root
    creation_interface()
    
    # Lecture de la musique de fond
    play_music()
    
    # Permet de "loop" le programme ce qui donne l'impression d'animation (alors que ce ne sont que des images)
    root.mainloop()
    
    
# Fonction créant la fenêtre qui contiendra le jeu (on y place tout ses attributs, c'est-à-dire taille, titre...)
def creation_fenetre_root():
    # Création d'une fenêtre tkinter root
    global root
    root = Tk()

    # Définition du logo de la fenêtre
    global chemin_absolu
    root.iconbitmap(chemin_absolu + "Images//LOGO//bateau.ico")
    
    # Définition du titre de la fenêtre
    root.title("Bataille Navale")
    
    # On définit la fenêtre par une grille 1x1
    root.rowconfigure(0, weight=1) 
    root.columnconfigure(0, weight=1)
    
    # On définit la taille de la fenêtre par défaut
    LARGEUR_ROOT = 1100
    HAUTEUR_ROOT = 800
    
    # On rappelle les constantes de dimensions de l'écran utilisateur
    global LARGEUR_ECRAN, HAUTEUR_ECRAN
    
    # Positionnement de la fenêtre au milieu de l'écran et application de la taille
    x = (LARGEUR_ECRAN / 2) - (LARGEUR_ROOT / 2)
    y = (HAUTEUR_ECRAN / 2) - (HAUTEUR_ROOT / 2)
    # Les 2 premières variables appliquent la taille de la fenêtre tandis que les deux autres positionnent la fenêtre (similaire au padding mais par rapport à l'écran)
    root.geometry("%dx%d+%d+%d" %(LARGEUR_ROOT, HAUTEUR_ROOT, x, y))
    
    # On limite la taille minimale de la fenêtre
    root.minsize(LARGEUR_ROOT, HAUTEUR_ROOT)


# Mise en place des différent frames
def placement_frame():
    # Frame principal
    global frame_principal 
    frame_principal = Frame(root, bg = "#141414") 

    # Frame personnalisation
    global frame_personnalisation
    frame_personnalisation = Frame(root, bg = "#141414") 
    
    # Frame de jeu
    global frame_jeu
    frame_jeu = Frame(root, bg = "#141414") 
    
    # Frame des reglages
    global frame_reglages
    frame_reglages = Frame(root, bg = "#141414") 
    
    # Frame des credits
    global frame_credits
    frame_credits = Frame(root, bg = "#141414")
    
    # Frame de victoire
    global frame_victoire
    frame_victoire = Frame(root, bg = "#141414")
    
    # Placement des frames par superposition grâce au row et columnconfigure (pour passer de l'une à l'autre, on utilisera une fonction avec un tk.raise)
    for frame in (frame_principal, 
                  frame_personnalisation, 
                  frame_jeu, 
                  frame_reglages, 
                  frame_credits,
                  frame_victoire):
        frame.grid(row = 0, column = 0, sticky = "nsew")


# Fonction qui regroupe toutes les fonctions créant l'interface du root       
def creation_interface():    
    # Utilisation de la fonction permettant de meubler le frame du menu principal
    creation_ecran_principal()
    
    # Utilisation de la fonction permettant de meubler le frame du menu de personnalisation
    creation_ecran_personnalisation()
    bind_frame_personnalisation()
    
    # Utilisation de la fonction permettant de meubler le frame du menu de placement
    creation_ecran_jeu()
    bind_jeu()
    
    # Utilisation de la fonction permettant de meubler le frame des crédits
    creation_ecran_credits()
    
    # Utilisation de la fonction permettant de meubler le frame des reglages
    creation_ecran_reglages()
    
    # Utilisation de la fonction permettant de meubler le frame victoire
    creation_ecran_victoire()

    
"""
Partie commande ROOT
"""

# Sons
def play_button():
    global chemin_absolu
    son_survol = pygame.mixer.Sound(chemin_absolu + "OST//enter_button.mp3")
    son_survol.play(loops = 0)
    son_survol.set_volume(0.3)
    
    
# Sons   
def play_clic():
    global chemin_absolu
    son_clic = pygame.mixer.Sound(chemin_absolu + "OST//clic_button.mp3")
    son_clic.play(loops = 0)
    son_clic.set_volume(0.3)
    
    
# Musique  
def play_music():
    global chemin_absolu
    pygame.mixer.music.load(chemin_absolu + "OST//meow.mp3")
    pygame.mixer.music.play(loops = -1)
    pygame.mixer.music.set_volume(0.1)
    
    
# Fonction qui permet de switcher entre les différents frames du root (système de calque)
def affichage_frame(frame):
    frame.tkraise()
    
    
"""
Partie graphique menu principal
"""


# Structure du menu principal
def creation_ecran_principal():
    # On appelle toutes les fonctions dans creation_ecran_principal() cela amène à la création complète du menu principal
    carreaux_principal()
    creation_boutons_frame_principal()
    creation_canvas_frame_principal()
    
    
# Création d'une grille ixi invisible pour le bon placement des widgets
def carreaux_principal():
    for i in range(31):
        frame_principal.rowconfigure(i, weight = 1)
        frame_principal.columnconfigure(i, weight = 1)
 

# Création des boutons dans le frame principal
def creation_boutons_frame_principal():
    
    
    # Modèle de bouton (similaire à une classe en objet)
    def modele_boutons_frame_principal(i, j, text, bgcolor, fgcolor, command):
        
        
        # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
        def survol(event):
            bouton_frame_principal.config(background = bgcolor,
                                          foreground = fgcolor)
            play_button()
            
            
        def fin_survol(event):
            bouton_frame_principal.config(background = fgcolor,
                                          foreground = bgcolor)
            play_button()
            
            
        def clic(event):
            play_clic()
            
        
        # Création du bouton dans le frame principal
        global frame_principal
        bouton_frame_principal = Button(frame_principal,
                                        text = text,
                                        bg = fgcolor,
                                        fg = bgcolor,
                                        border = 0,
                                        activeforeground = fgcolor,
                                        activebackground = bgcolor,
                                        font = ("Benguiat", 15),
                                        command = command)

        # Positionnement du bouton dans le frame principal
        bouton_frame_principal.grid(row = i, column = j, sticky = "nsew")
        
        # Attribution des intéractions utilisateurs aux fontions du dessus (survol...)
        bouton_frame_principal.bind("<Enter>", survol)
        bouton_frame_principal.bind("<Leave>", fin_survol)
        bouton_frame_principal.bind("<Button-1>", clic)
        

    # Ici on crée des boutons à partir du modèle
    modele_boutons_frame_principal(11, 15, "J O U E R", "#ffcc66", "#141414", lambda:affichage_frame(frame_personnalisation))
    modele_boutons_frame_principal(13, 15, "O P T I O N S", "#25dae9", "#141414", lambda:affichage_frame(frame_reglages))
    modele_boutons_frame_principal(15, 15, "C R E D I T S", "#f86263", "#141414", lambda:affichage_frame(frame_credits))
    modele_boutons_frame_principal(17, 15, "Q U I T T E R", "#ffa157", "#141414", root.quit())


# Création des canvas textes dans le frame principal
def creation_canvas_frame_principal():
    
    
    # Modèle de canvas (similaire à une classe en objet)
    def modele_canvas_frame_principal(i, j, bgcolor, width, height, text, font, x, y, fill):
        global frame_principal
        canvas_frame_principal = Canvas(frame_principal,
                                        bg = bgcolor,
                                        width = width,
                                        height = height,
                                        border = 0,
                                        highlightthickness = 0)
        
        # Positionnement des canvas le frame principal
        canvas_frame_principal.grid(row = i, column = j, sticky = "nsew")
        
        # On crée un texte dans le canvas (les canvas textes causent moins de problèmes dans le positionnement que les labels)
        canvas_frame_principal.create_text(x, y, text = text, font = font, fill = fill)
    
    
    # Ici on crée des canvas à partir du modèle
    modele_canvas_frame_principal(5, 15, "#141414", 500, 80, "B A T A I L L E   N A V A L E", ("LeviBrush 25 underline"), 255, 40, "#0e74c7")
    modele_canvas_frame_principal(31, 0, "#141414", 130, 40, "v1.4.2", ("Andi 10"), 30, 20, "#0e74c7")
    modele_canvas_frame_principal(31, 31, "#141414", 130, 40, "Copyright © 2022 JT", ("Andi 10"), 65, 20, "#0e74c7")
     

"""
Partie graphique menu reglages
"""


# Structure du menu reglages 
def creation_ecran_reglages():
    # On appelle toutes les fonctions dans creation_ecran_reglages()
    carreaux_reglages()
    creation_canvas_frame_reglages()
    creation_boutons_frame_reglages()
    creation_scales_frame_reglages()
    
    
# Création d'une grille ixi invisible pour le bon placement des widgets
def carreaux_reglages():
    for i in range(31):
        frame_reglages.rowconfigure(i, weight = 1)
        frame_reglages.columnconfigure(i, weight = 1)
            

# Création du canvas texte dans le frame reglages
def creation_canvas_frame_reglages():
    # Création du canvas
    global frame_reglages
    global canvas_frame_reglages
    canvas_frame_reglages = Canvas(frame_reglages,
                                   bg = "#141414",
                                   width = 80,
                                   height = 80,
                                   border = 0,
                                   highlightthickness = 0)
    
    # Positionnement du canvas
    canvas_frame_reglages.grid(row = 15, column = 14, sticky = "nsew")
    
    # Création du texte dans le canvas
    canvas_frame_reglages.create_text(65, 40, text = "5 %", font = "Benguiat 25", fill = "white")
    
    
# Création des boutons dans le frame reglages
def creation_boutons_frame_reglages():
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
    def survol_valider(event):
        bouton_frame_reglages_retour.config(background = "#ffa157",
                                             foreground = "#141414")
        play_button()
        
        
    def fin_survol_valider(event):
        bouton_frame_reglages_retour.config(background = "#141414",
                                             foreground = "#ffa157")
        play_button()
        
        
    def clic(event):
            play_clic()


    # Création du bouton valider
    global bouton_frame_reglages_retour
    bouton_frame_reglages_retour = Button(frame_reglages,
                                           text = "R E T O U R",
                                           font = ("Benguiat", 15),
                                           bg = "#141414",
                                           fg = "#ffa157",
                                           border = 0,
                                           activeforeground = "#141414",
                                           activebackground = "#ffa157",
                                           command = lambda:affichage_frame(frame_principal))
    
    # Positionnement du bouton valider
    bouton_frame_reglages_retour.grid(row = 30, column = 15, sticky = "nsew")
    
    # Attribution des intéractions utilisateurs au fonctions du dessus (survol...)
    bouton_frame_reglages_retour.bind("<Enter>", survol_valider)
    bouton_frame_reglages_retour.bind("<Leave>", fin_survol_valider)
    bouton_frame_reglages_retour.bind("<Button-1>", clic)
    

def creation_scales_frame_reglages():
    # Création du scale du volume musique
    global volume_musique
    volume_musique = ttk.Scale(frame_reglages,
                              from_ = 0, 
                              to = 1, 
                              orient = HORIZONTAL, 
                              value = 0.05,
                              command = controle_volume, 
                              length = 250)
    
    # Positionnement du scale du volume musique
    volume_musique.grid(row = 15, column = 15, sticky = "nsew")

    
"""
Partie commandes menu reglages
"""

    
def controle_volume(event):
    global canvas_frame_reglages
    pygame.mixer.music.set_volume(volume_musique.get())
    volume_actuel = pygame.mixer.music.get_volume()
    canvas_frame_reglages.itemconfig(1, text = str(int(volume_actuel * 100)) + " %")

"""
Partie graphique menu credits
"""


# Structure du menu des credits
def creation_ecran_credits():
    # On appelle toutes les fonctions dans creation_ecran_credits()
    carreaux_credits()
    creation_canvas_frame_credits()
    noms_frame_credits()
    images_frame_credits()
    creation_boutons_frame_credits()
    
    
# Création d'une grille ixi invisible pour le bon placement des widgets
def carreaux_credits():
    for i in range(1):
        frame_credits.rowconfigure(i, weight = 1)
        frame_credits.columnconfigure(i, weight = 1)
       
        
def creation_canvas_frame_credits():
    # On crée un canvas (il permettra le placement du texte et des images)
    global canvas_credits
    canvas_credits = Canvas(frame_credits, highlightthickness = 0, bg = "#141414")
    
    # On l'étend à tout le frame
    canvas_credits.grid(row = 0, column = 0, sticky = "nsew")
    
    # Création d'une grille invisible ixi pour le bon placement du texte et des images
    for i in range(31):
        canvas_credits.rowconfigure(i, weight = 1)
        canvas_credits.columnconfigure(i, weight = 1)


def noms_frame_credits():
    # On rappelle les dimensions de l'écran calculées précedemment (cela servira au bon placement des items du canvas)
    global LARGEUR_ECRAN, HAUTEUR_ECRAN
    
    # Création d'une liste de texte
    global nom
    nom = ["C R E A T E U R S", "Jawad <Lorest#5095> MAACHE", "Timothee <SteelPotato#3653> DA COSTA ...", "D E S I G N E R S", "Jawad <Lorest#5095> MAACHE", "Timothee <SteelPotato#3653> DA COSTA ...", "P R O G R A M M A T I O N", "Jawad <Lorest#5095> MAACHE", "Timothee <SteelPotato#3653> DA COSTA ...", "R E M E R C I E M E N T S", "Elisee <Thorgrimm> JOUENNE", "Mathias <Hiolia> DELMAS", "Joris <jserrand#3326> SERRAND"]

    # Création d'une liste de coordonnées de placement (hauteur) des textes
    global coord_y1
    coord_y1 = [1000, 1150, 1275, 1475, 1625, 1750, 1950, 2100, 2225, 2425, 2575, 2700, 2825]
    
    # Boucle placant les textes de la liste sur le canvas
    for i in range(len(nom)):
        if i == 0 or i == 3 or i == 6 or i == 9:
            canvas_credits.create_text(LARGEUR_ECRAN / 2, coord_y1[i], text = nom[i], font = ("Benguiat", 40, "underline"), fill = "white")
        else:
            canvas_credits.create_text(LARGEUR_ECRAN / 2, coord_y1[i], text = nom[i], font = ("LeviBrush", 30), fill = "white")
        
    # On garde en mémoire la position initiale du premier texte afin de le repositionner par la suite (avec la fonction reset)
    global y1 
    x1, y1, x2, y2 = canvas_credits.bbox(1)
    
    
def images_frame_credits():
    # On rappelle les dimensions de l'écran calculées précedemment (cela servira au bon placement des items du canvas)
    global LARGEUR_ECRAN, HAUTEUR_ECRAN
    global chemin_absolu
    
    # Ouvertures d'images
    lorestImage = PhotoImage(file = chemin_absolu + "Images//AVATAR//lorest-avatar.png")
    steelpotatoImage = PhotoImage(file = chemin_absolu + "Images//AVATAR//steelpotato-avatar.png")
    thorgrimmImage = PhotoImage(file = chemin_absolu + "Images//AVATAR//thorgrimm-avatar.png")
    hioliaImage = PhotoImage(file = chemin_absolu + "Images//AVATAR//hiolia-avatar.png")
    jserrandImage = PhotoImage(file = chemin_absolu + "Images//AVATAR//jserrand-avatar.png")
    
    # Création d'une liste d'images
    global image_avatar
    image_avatar = [lorestImage, steelpotatoImage, lorestImage, steelpotatoImage, lorestImage, steelpotatoImage, thorgrimmImage, hioliaImage, jserrandImage]
    
    # Création d'une liste de coordonnées de placement (largeur et hauteur) des images
    global coord_y2
    coord_y2 = [1200, 1325, 1675, 1800, 2150, 2275, 2625, 2750, 2875]
    
    # Boucle placant les images sur le canvas
    for i in range(len(image_avatar)):
        canvas_credits.create_image(LARGEUR_ECRAN / 2, coord_y2[i], image = image_avatar[i])
            

# Création des boutons dans le frame crédits
def creation_boutons_frame_credits():
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
    def survol_retour(event):
        bouton_retour_frame_credits.config(background = "#ffa157",
                                           foreground = "#141414")
        play_button()
        
        
    def fin_survol_retour(event):
        bouton_retour_frame_credits.config(background = "#141414",
                                           foreground = "#ffa157")
        play_button()
        
    
    def survol_lancer(event):
        bouton_lancer_frame_credits.config(background = "#ffcc66",
                                           foreground = "#141414")
        play_button()
        
        
    def fin_survol_lancer(event):
        bouton_lancer_frame_credits.config(background = "#141414",
                                           foreground = "#ffcc66")
        play_button()
    
    
    def clic(event):
        play_clic()
    
    
    # Ici, on créera pas de modèle, en effet il nous faut être capable d'appeler chaque boutons pour les supprimer par la suite
    
    # Création du bouton retour
    global bouton_retour_frame_credits
    bouton_retour_frame_credits = Button(canvas_credits,
                                         text = "R E T O U R",
                                         font = ("Benguiat", 15),
                                         bg = "#141414",
                                         fg = "#ffcc66",
                                         border = 0,
                                         activeforeground = "#141414",
                                         activebackground = "#ffa157",
                                         command = lambda:affichage_frame(frame_principal))
    
    # Positionnement du bouton retour
    bouton_retour_frame_credits.grid(row = 30, column = 1, sticky = "nsew")
    
    # Création du bouton lancer
    global bouton_lancer_frame_credits
    bouton_lancer_frame_credits = Button(canvas_credits,
                                         text = "L A N C E R",
                                         font = ("Benguiat", 15),
                                         bg = "#141414",
                                         fg = "#ffcc66",
                                         border = 0,
                                         activeforeground = "#141414",
                                         activebackground = "#ffcc66",
                                         command = lambda:debut_animation())
    
    # Positionnement du bouton lancer
    bouton_lancer_frame_credits.grid(row = 30, column = 29, sticky = "nsew")
        
    # Attribution des intéractions utilisateurs aux fonctions du dessus (survol...)
    bouton_retour_frame_credits.bind("<Enter>", survol_retour)
    bouton_retour_frame_credits.bind("<Leave>", fin_survol_retour)
    bouton_retour_frame_credits.bind("<Button-1>", clic)
    bouton_lancer_frame_credits.bind("<Enter>", survol_lancer)
    bouton_lancer_frame_credits.bind("<Leave>", fin_survol_lancer)
    bouton_lancer_frame_credits.bind("<Button-1>", clic)
    
      
"""
Partie commandes menu credits
"""


# Fonction mettant en place l'animation du menu credits
def debut_animation():
    # On met la fenêtre en grand écran
    root.attributes('-fullscreen', True)
    
    # Suppression des boutons du menu
    bouton_retour_frame_credits.destroy()
    bouton_lancer_frame_credits.destroy()
    
    
    # Fonction récursive permettant le déplacement des items (textes/images) du canvas
    def animation():
        # On fait bouger vers le haut de 1 pixel tout les items du canvas
        for i in range(1, len(canvas_credits.find_all()) + 1):
            canvas_credits.move(i, 0, -1)
            
        # On détermine les coordonnées du dernier texte
        x1, y1, x2, y2 = canvas_credits.bbox(len(nom))
        
        # Si ces coordonnées ne sont pas à la bordure du dessus du menu alors la fonction se rappelle
        if y2 != 0:
            # La fonction se rappelle avec un délai (ici 5ms)
            root.after(5, animation)
            
        # Sinon, un bouton retour pour quitter le menu apparaît
        else:
            
            
            # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
            def survol_reset(event):
                bouton_reset_credits.config(background = "#ffcc66",
                                                   foreground = "#141414")
            
            
            def fin_survol_reset(event):
                bouton_reset_credits.config(background = "#141414",
                                                   foreground = "#ffcc66")
                
                
            # Création du bouton du reset credits    
            global bouton_reset_credits
            bouton_reset_credits = Button(canvas_credits, 
                                          text = "R E T O U R", 
                                          bg = "#141414",
                                          fg = "#ffcc66",
                                          border = 0,
                                          activeforeground = "#141414",
                                          activebackground = "#ffcc66",
                                          command = lambda:quitter_credits())
            
            # Positionnement du bouton reset credits
            bouton_reset_credits.grid(row = 25, column = 15, sticky = "nsew")
            
            # Attribution des intéractions utilisateurs aux fonctions du dessus (survol...)
            bouton_reset_credits.bind("<Enter>", survol_reset)
            bouton_reset_credits.bind("<Leave>", fin_survol_reset)
            
    
    # On appelle la fonction animation ce qui l'initialise
    animation()
    
    
# Fonction appliquée lors de la fin des credits et de l'appui du bouton quitter
def quitter_credits():
    # On remet la fenêtre à sa taille de départ
    root.attributes('-fullscreen', False)
    
    # On fait un retour sur le menu principal
    affichage_frame(frame_principal)
    
    reset_credits()
    
    
# Fonction permettant le reset du menu credits
def reset_credits():
    # On calcule la position du premier texte
    x11 , y11, x22, y11 = canvas_credits.bbox(1)
    
    # Avec un calcul de distance, on repositionne tout les items à leurs positions de départ (grâce à une boucle)
    for i in range(1, len(canvas_credits.find_all()) + 1):
            canvas_credits.move(i, 0, -(y11 - y1))
            
    # Destruction du bouton quitter
    bouton_reset_credits.destroy()
    
    # Recrée les boutons de base du menu
    creation_boutons_frame_credits()


"""
Partie graphique menu personnalisation
"""


# Structure du menu personnalisation
def creation_ecran_personnalisation():
    # On appelle toutes les fonctions dans creation_ecran_personnalisation()
    carreaux_personnalisation()
    creation_canvas_frame_personnalisation()
    creation_boutons_frame_personnalisation()
    creation_entree_frame_personnalisation()
    creation_boutons_radios_frame_personnalisation()
    
    
# Création d'une grille ixi invisible pour le bon placement des widgets
def carreaux_personnalisation():
    for i in range(31):
        frame_personnalisation.rowconfigure(i, weight = 1)
        frame_personnalisation.columnconfigure(i, weight = 1)


# Création des boutons dans le frame personnalisation
def creation_boutons_frame_personnalisation():
    
    
    # Modèle de bouton (similaire à une classe en objet)
    def modele_boutons_frame_personnalisation(i, j, text, bgcolor, fgcolor, command):
        
        
        # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
        def survol(event):
            bouton_frame_personnalisation.config(background = bgcolor,
                                                 foreground = fgcolor)
            play_button()
            
            
        def fin_survol(event):
            bouton_frame_personnalisation.config(background = fgcolor,
                                                 foreground = bgcolor)
            play_button()
            
        
        def clic(event):
            play_clic()
        
        
        # Création du bouton dans le frame personnalisation
        global frame_personnalisation
        bouton_frame_personnalisation = Button(frame_personnalisation,
                                               text = text,
                                               font = ("Benguiat", 15),
                                               bg = fgcolor,
                                               fg = bgcolor,
                                               border = 0,
                                               activeforeground = fgcolor,
                                               activebackground = bgcolor,
                                               command = command)
        
        # Positionnement du bouton dans le frame
        bouton_frame_personnalisation.grid(row = i, column = j, sticky = "nsew")
        
        # Attribution des intéractions utilisateurs au fonctions du dessus (survol...)
        bouton_frame_personnalisation.bind("<Enter>", survol)
        bouton_frame_personnalisation.bind("<Leave>", fin_survol)
        bouton_frame_personnalisation.bind("<Button-1>", clic)
    
    
    # Ici on crée des boutons à partir du modèle
    modele_boutons_frame_personnalisation(5, 15, "C O U L E U R", "#25dae9", "#141414", choix_couleur_pseudo)
    modele_boutons_frame_personnalisation(30, 1, "R E T O U R", "#ffa157", "#141414", lambda:affichage_frame(frame_principal))
    
    
    # On crée le bouton "valider" à part car il subira des changements en fonction de l'utilisateur
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
    def survol_valider(event):
        if bouton_frame_personnalisation_valider['state'] == NORMAL:
            bouton_frame_personnalisation_valider.config(background = "#ffcc66",
                                                         foreground = "#141414")
        play_button()
        
        
    def fin_survol_valider(event):
        if bouton_frame_personnalisation_valider['state'] == NORMAL:
            bouton_frame_personnalisation_valider.config(background = "#141414",
                                                         foreground = "#ffcc66")
        play_button()
        
    
    def clic(event):
        play_clic()


    # Création du bouton valider
    global bouton_frame_personnalisation_valider
    bouton_frame_personnalisation_valider = Button(frame_personnalisation,
                                                   text = "V A L I D E R",
                                                   font = ("Benguiat", 15),
                                                   bg = "#141414",
                                                   fg = "#ffcc66",
                                                   border = 0,
                                                   activeforeground = "#141414",
                                                   activebackground = "#ffa157",
                                                   state = DISABLED,
                                                   command = lambda:affichage_frame(frame_jeu))
    
    # Positionnement du bouton valider
    bouton_frame_personnalisation_valider.grid(row = 30, column = 29, sticky = "nsew")
    
    # Attribution des intéractions utilisateurs au fonctions du dessus (survol...)
    bouton_frame_personnalisation_valider.bind("<Enter>", survol_valider)
    bouton_frame_personnalisation_valider.bind("<Leave>", fin_survol_valider)
    bouton_frame_personnalisation_valider.bind("<Button-1>", clic)
        

# Création du canvas texte dans le frame personnalisation
def creation_canvas_frame_personnalisation():
    # Création du canvas
    global frame_personnalisation
    global canvas_frame_personnalisation
    canvas_frame_personnalisation = Canvas(frame_personnalisation,
                                           bg = "#141414",
                                           width = 50,
                                           height = 80,
                                           border = 0,
                                           highlightthickness = 0)
    
    # Positionnement du canvas
    canvas_frame_personnalisation.grid(row = 15, column = 15, sticky = "nsew")
    
    # Création du texte dans le canvas
    canvas_frame_personnalisation.create_text(115, 40, text = "C H O I S I S", font = "Benguiat 25", fill = "#4287f5")
    

# Création de la zone d'entrée de texte dans le frame de personnalisation   
def creation_entree_frame_personnalisation():
    # Création de l'entry
    global entrer_pseudo
    entrer_pseudo = Entry(frame_personnalisation,
                          font = ("journey", 20),
                          width = 14,
                          fg = "Black", 
                          bg = "white")
   
    # Positionnement de l'entry
    entrer_pseudo.grid(row = 3, column = 15, sticky = "nsew")
    
    
# Création des boutons radios dans le frame personnalisation
def creation_boutons_radios_frame_personnalisation():
    # Ouverture d'images et redimensionnement de ces dernières
    global chemin_absolu
    jppImage = Image.open(chemin_absolu + 'Images//jpp.jpg')
    jppImage_redim = jppImage.resize((200,200))
    global facileImage
    facileImage = ImageTk.PhotoImage(jppImage_redim)
    
    dignityImage = Image.open(chemin_absolu + 'Images//dignity.png')
    dignityImage_redim = dignityImage.resize((200,200))
    global normalImage
    normalImage = ImageTk.PhotoImage(dignityImage_redim)
    
    zyzzImage = Image.open(chemin_absolu + 'Images//zyzz.png')
    zyzzImage_redim = zyzzImage.resize((200, 200))
    global difficileImage
    difficileImage = ImageTk.PhotoImage(zyzzImage_redim)
    
    # Permet d'appeler chaque boutons radios en fonction de leurs 'value'
    global numero
    numero = IntVar() 
    
    # Coche le bouton 3 par défaut (n'existe pas, donc aucun bouton n'est coché)
    numero.set(3) 
    
    
    # Modèle de bouton radio (similaire à une classe en objet)
    def modele_boutons_radios_frame_personnalisation(i, j, value, text, font, image):
    
        
        # Création du bouton radio
        bouton_radio_frame_personnalisation = Radiobutton(frame_personnalisation,
                                                          variable = numero,
                                                          value = value,
                                                          text = text,
                                                          font = font,
                                                          image = image,
                                                          # Supprime les cercles à cocher
                                                          indicatoron = 0,
                                                          width = 200,
                                                          # Positionne les images au dessus du texte
                                                          compound = "top",
                                                          command = choix_difficulte)
        
        # Positionnement du bouton radio
        bouton_radio_frame_personnalisation.grid(row = i, column = j, sticky = "nsew")
        
        
    # Ici on crée des boutons radios à partir du modèle
    modele_boutons_radios_frame_personnalisation(13, 12, 0, "F A C I L E", ("League Gothic", 20, "bold"), facileImage)
    modele_boutons_radios_frame_personnalisation(13, 15, 1, "N O R M A L", ("League Gothic", 20, "bold"), normalImage)
    modele_boutons_radios_frame_personnalisation(13, 18, 2, "D I F F I C I L E", ("League Gothic", 20, "bold"), difficileImage) 
    
    
"""
Partie commandes menu personnalisation
"""


# Lance un effet sonore
def play_roblox():
    global chemin_absolu
    son_roblox = pygame.mixer.Sound(chemin_absolu + "OST//roblox.mp3")
    son_roblox.play(loops = 0)
    son_roblox.set_volume(0.5)
    
    
def play_coins():
    global chemin_absolu
    son_coins = pygame.mixer.Sound(chemin_absolu + "OST//coins.mp3")
    son_coins.play(loops = 0)
    son_coins.set_volume(0.5)
    
    
def play_zyzz():
    global chemin_absolu
    son_zyzz = pygame.mixer.Sound(chemin_absolu + "OST//fing-zyzz-brah-yeah.mp3")
    son_zyzz.play(loops = 0)
    son_zyzz.set_volume(0.5)
    

# Permet de sélectionner une couleur qui s'appliquera à l'écriture
def choix_couleur_pseudo():
    entrer_pseudo.config(fg = colorchooser.askcolor()[1]) 
    
    
def bind_frame_personnalisation():
    entrer_pseudo.bind("<KeyRelease>", pseudo_valide)
    
    
# Sélection d'une difficulté 
def choix_difficulte():
    global canvas_frame_personnalisation
    global niv_facile
    global niv_moyen
    global niv_difficile
    global mode
    # Si le premier bouton est sélectionné:
    if numero.get() == 0:
        # Flag de difficulté enclenché
        niv_facile = True
        niv_moyen = False
        niv_difficile = False
        # Actualisation du texte
        canvas_frame_personnalisation.itemconfig(1, text = "F A I B L E")
        mode = "F A C I L E"
        play_roblox()
        
    # Si le deuxième bouton est sélectionné:
    if numero.get() == 1:
        # Flag de difficulté enclenché
        niv_moyen = True
        niv_facile = False
        niv_difficile = False
        # Actualisation du texte
        canvas_frame_personnalisation.itemconfig(1, text = "B A S T O N")
        mode = "M O Y E N"
        play_coins()

    # Si le troisième bouton est sélectionné:
    if numero.get() == 2:
        # Flag de difficulté enclenché
        niv_difficile = True
        niv_facile = False
        niv_moyen = False
        # Actualisation du texte
        canvas_frame_personnalisation.itemconfig(1, text = "F O R T")
        mode = "D I F F I C I L E"
        # Effet sonore
        play_zyzz()
    deblocage_bouton_valider_frame_personnalisation()
    
    
def pseudo_valide(event):
    deblocage_bouton_valider_frame_personnalisation()
    
    
def deblocage_bouton_valider_frame_personnalisation():
    global bouton_frame_personnalisation_valider
    if entrer_pseudo.get() != "" and numero.get() <= 2:
        bouton_frame_personnalisation_valider['state'] = NORMAL
    else:
        bouton_frame_personnalisation_valider['state'] = DISABLED

        
# Reset les boutons radios 
def reset_difficultes():
    global numero
    numero.set(3)
    global niv_facile, niv_normal, niv_difficile
    niv_facile = False
    niv_moyen = False
    niv_difficile = False 
    
    
# Reset le pseudo
def reset_entry():
    global entrer_pseudo
    entrer_pseudo.delete(0)

"""
Partie graphique menu jeu
"""


# Structure du menu principal
def creation_ecran_jeu():
    # Appel de toutes les fonctions qui meublent le frame jeu
    carreaux_jeu()  
    creation_canvas_frame_jeu()
    creation_boutons_frame_jeu()
    creation_bouton_placer_jeu()
    creation_bouton_jouer_jeu()
    creation_sante_frame_jeu()
    creation_plateaux()
    
    
# Création d'une grille invisible ixi pour le bon placement des widgets
def carreaux_jeu():
    for i in range(31):
        frame_jeu.rowconfigure(i, weight = 1)
        frame_jeu.columnconfigure(i, weight = 1)
        
        
# Création des boutons dans le frame principal
def creation_boutons_frame_jeu():
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton s'il est actif, et ainsi de mieux visualiser la souris sur le bouton) 
    def survol_retour(event):
        if bouton_retour_frame_jeu['state'] == NORMAL:
            bouton_retour_frame_jeu.config(background = "#25dae9",
                                           foreground = "#141414")
            play_button()
        
    def fin_survol_retour(event):
        if bouton_retour_frame_jeu['state'] == NORMAL:
            bouton_retour_frame_jeu.config(background = "#141414",
                                           foreground = "#25dae9")
            play_button()
        
        
    def survol_abandon(event):
        if bouton_abandon_frame_jeu['state'] == NORMAL:
            bouton_abandon_frame_jeu.config(background = "#f86263",
                                           foreground = "#141414")
            play_button()
        
    def fin_survol_abandon(event):
        if bouton_abandon_frame_jeu['state'] == NORMAL:
            bouton_abandon_frame_jeu.config(background = "#141414",
                                           foreground = "#f86263")
            play_button()
        
        
    def survol_regles(event):
            bouton_regles_frame_jeu.config(background = "#5a3b9c",
                                           foreground = "#141414")
            play_button()
        
    def fin_survol_regles(event):
            bouton_regles_frame_jeu.config(background = "#141414",
                                          foreground = "#5a3b9c")
            play_button()
            
    
    def clic(event):
        play_clic()
    
    
    global frame_jeu  
    # Création du bouton retour
    global bouton_retour_frame_jeu
    bouton_retour_frame_jeu = Button(frame_jeu,
                                     text = "R E T O U R",
                                     font = ("Benguiat", 15),
                                     bg = "#141414",
                                     fg = "#25dae9", 
                                     border = 0,
                                     activebackground = "#141414",
                                     activeforeground = "#25dae9",
                                     command = defaite)
    
    # Positionnement du bouton retour
    bouton_retour_frame_jeu.grid(row = 30, column = 1, sticky = "nsew")
    
    
    # Création du bouton abandon
    global bouton_abandon_frame_jeu
    bouton_abandon_frame_jeu = Button(frame_jeu,
                                     text = "A B A N D O N",
                                     font = ("Benguiat", 15),
                                     bg = "#141414",
                                     fg = "#f86263", 
                                     border = 0,
                                     activebackground = "#141414",
                                     activeforeground = "#f86263",
                                     command = lambda:root.destroy())
    
    # Positionnement du bouton abandon
    bouton_abandon_frame_jeu.grid(row = 30, column = 29, sticky = "nsew")
    
    
    # Création du bouton regles
    global bouton_regles_frame_jeu
    bouton_regles_frame_jeu = Button(frame_jeu,
                                     text = "R E G L E S",
                                     font = ("Benguiat", 15),
                                     bg = "#141414",
                                     fg = "#5a3b9c", 
                                     border = 0,
                                     activebackground = "#141414",
                                     activeforeground = "#5a3b9c",
                                     command = open)
    
    # Positionnement du bouton regles
    bouton_regles_frame_jeu.grid(row = 25, column = 15, sticky = "nsew")
    
    # Attribution des intéractions utilisateurs aux fonctions du dessus (survol...)
    bouton_retour_frame_jeu.bind("<Enter>", survol_retour)
    bouton_retour_frame_jeu.bind("<Leave>", fin_survol_retour)
    bouton_retour_frame_jeu.bind("<Button-1>", clic)
    
    bouton_abandon_frame_jeu.bind("<Enter>", survol_abandon)
    bouton_abandon_frame_jeu.bind("<Leave>", fin_survol_abandon)
    bouton_abandon_frame_jeu.bind("<Button-1>", clic)
    
    bouton_regles_frame_jeu.bind("<Enter>", survol_regles)
    bouton_regles_frame_jeu.bind("<Leave>", fin_survol_regles)
    bouton_regles_frame_jeu.bind("<Button-1>", clic)
    

def creation_bouton_placer_jeu():
    
    
    def survol_placer(event):
        if bouton_placer_frame_jeu['state'] == NORMAL:
            bouton_placer_frame_jeu.config(background = "#ffcc66",
                                           foreground = "#141414")
            play_button()
        
    def fin_survol_placer(event):
        if bouton_placer_frame_jeu['state'] == NORMAL:
            bouton_placer_frame_jeu.config(background = "#141414",
                                           foreground = "#ffcc66")
            play_button()
            
    
    def clic(event):
        play_clic()
            
            
    global frame_jeu  
    # Création du bouton jouer
    global bouton_placer_frame_jeu
    bouton_placer_frame_jeu = Button(frame_jeu,
                                     text = "P L A C E R",
                                     font = ("Benguiat", 15),
                                     bg = "#141414",
                                     fg = "#ffcc66", 
                                     border = 0,
                                     activebackground = "#141414",
                                     activeforeground = "#ffcc66",
                                     command = placementTK)
    
    # Positionnement du bouton placer
    bouton_placer_frame_jeu.grid(row = 14, column = 15, sticky = "nsew")
            
    bouton_placer_frame_jeu.bind("<Enter>", survol_placer)
    bouton_placer_frame_jeu.bind("<Leave>", fin_survol_placer)
    bouton_placer_frame_jeu.bind("<Button-1>", clic)
    
    
def creation_bouton_jouer_jeu():


    def survol_jouer(event):
        if bouton_jouer_frame_jeu['state'] == NORMAL:
            bouton_jouer_frame_jeu.config(background = "#ffcc66",
                                          foreground = "#141414")
            play_button()
        
    def fin_survol_jouer(event):
        if bouton_jouer_frame_jeu['state'] == NORMAL:
            bouton_jouer_frame_jeu.config(background = "#141414",
                                          foreground = "#ffcc66")
            play_button()
            
            
    def clic(event):
        play_clic()


    # Création du bouton placer
    global bouton_jouer_frame_jeu
    bouton_jouer_frame_jeu = Button(frame_jeu,
                                     text = "J O U E R",
                                     font = ("Benguiat", 15),
                                     bg = "#141414",
                                     fg = "#ffcc66", 
                                     border = 0,
                                     activebackground = "#141414",
                                     activeforeground = "#ffcc66",
                                     command = lancement_jouer)
    
    bouton_jouer_frame_jeu.bind("<Enter>", survol_jouer)
    bouton_jouer_frame_jeu.bind("<Leave>", fin_survol_jouer)
    bouton_jouer_frame_jeu.bind("<Button-1>", clic)
    
    
# Création du score et du timer
def creation_canvas_frame_jeu():
    # Création du score
    global score
    global score_comm
    score_comm = Canvas(frame_jeu,
                        bg = "#141414",
                        border = 0, 
                        highlightthickness = 0,
                        width = 100,
                        height = 50)
    
    # Positionnement du score
    score_comm.grid(row = 1, column = 5, sticky = "nsew")
    
    # On crée un texte dans le canvas (les canvas textes causent moins de problèmes dans le positionnement que les labels)
    score_comm.create_text(70, 40, text = "Score : " + str(score), font = ("Andi 20 bold"), fill = "white")
    
    
    # Création du commentaire sur l'action du joueur
    global action_joueur
    action_joueur = Canvas(frame_jeu,
                           bg = "#141414",
                           border = 0, 
                           highlightthickness = 0,
                           width = 100,
                           height = 50)
    
    # Positionnement du commentaire sur l'action du joueur
    action_joueur.grid(row = 16, column = 5, sticky = "nsew")
    
    # On écrit l'action l'action du joueur
    action_joueur.create_text(95, 25, text = "Votre plateau", font = ("Andi 20 bold"), fill = "white")
    
    
    # Création du commentaire sur l'action du bot
    global action_bot
    action_bot = Canvas(frame_jeu,
                        bg = "#141414",
                        border = 0, 
                        highlightthickness = 0,
                        width = 100,
                        height = 50)
    
    # Positionnement du commentaire sur l'action du bot
    action_bot.grid(row = 16, column = 25, sticky = "nsew")
    
    # On écrit l'action du bot
    action_bot.create_text(105, 25, text = "Plateau de l'ordi", font = ("Andi 20 bold"), fill = "white")
    
    # Création d'un chronomètre ainsi qu'un afficheur de tour
    global chrono
    chrono = Canvas(frame_jeu,
                    bg = "#141414",
                    border = 0,
                    highlightthickness = 0,
                    width = 100,
                    height = 50)
    
    # Positionnement du chronomètre
    chrono.grid(row = 5, column = 15, sticky = "nsew")
    
    # On écrit le tour et le temps
    chrono.create_text(50, 25, text = "", font = ("LeviBrush", 25))
    
    
# Fonction créant les barres de santé (en test)
def creation_sante_frame_jeu():
    global sante_joueur
    sante_joueur = Progressbar(frame_jeu,
                                orient = "horizontal",
                                length = 380)
    sante_joueur.grid(row = 8, column = 5, sticky = "nsew")
    
    global sante_bot
    sante_bot = Progressbar(frame_jeu,
                            orient = "horizontal",
                            length = 380)
    sante_bot.grid(row = 8, column = 25, sticky = "nsew")
    
    global total_sante
    total_sante = 100
    
    global total_sante_b
    total_sante_b = 100
    
    sante_joueur['value'] = total_sante
    sante_bot['value'] = total_sante
    

# Fonction créant les plateaux
def creation_plateaux():
    # Utilisation des fonctions créant les 2 plateaux 
    plateau_jeu1()
    plateau_jeu2()
    
    # Utilisation de la fonction remplissant le plateau 2 avec les bateaux du bot
    bateaux_bot()
    
    
def plateau_jeu1():
    global plateau1
    plateau1 = Canvas(frame_jeu,
                      width = DIMENSION, 
                      height = DIMENSION,
                      highlightthickness = 0,
                      bg = "#141414")
    plateau1.grid(row = 15, column = 5, sticky = "nsew")
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            x, y = TAILLE_DE_CARRES * j + 2, TAILLE_DE_CARRES * i + 2
            A, B = (x, y), (x + TAILLE_DE_CARRES, y + TAILLE_DE_CARRES)
            plateau1.create_rectangle(A, B, fill = "#097ade")


def plateau_jeu2():
    global plateau2
    plateau2 = Canvas(frame_jeu, 
                      width = DIMENSION, 
                      height = DIMENSION,
                      highlightthickness = 0,
                      bg = "#141414")
    plateau2.grid(row = 15, column = 25, sticky = "nsew")
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            x, y = TAILLE_DE_CARRES * j + 2, TAILLE_DE_CARRES * i + 2
            A, B = (x, y), (x + TAILLE_DE_CARRES, y + TAILLE_DE_CARRES)
            plateau2.create_rectangle(A, B, fill = "#097ade")
    
    
# Placement des bateaux du bot
def bateaux_bot():
    long = [5,4,3,3,2]
    dir1 = [-1,0,1]
    dir2 = [-1,1]
    for i in range(len(long)):
        valide = False
        while not valide:
            valide = True
            x = random.randint(0,9)
            y = random.randint(0,9)
            while grille2[x][y] == 3:
                x = random.randint(0,9)
                y = random.randint(0,9)
            diff_x = dir1[random.randint(0,2)]
            if diff_x == 0:
                diff_y = dir2[random.randint(0,1)]
                if diff_y == -1:
                    for j in range(y, y+(diff_y*long[i]), -1):
                        if (j < 0) or (grille2[x][j] == 3):
                            valide = False
                elif diff_y == 1:
                    for j in range(y, y+(diff_y*long[i])):
                        if (j > 9) or (grille2[x][j] == 3):
                            valide = False
            else:
                diff_y = 0
                if diff_x == -1:
                    for j in range(x, x+(diff_x*long[i]), -1):
                        if (j < 0) or (grille2[j][y] == 3):
                            valide = False
                elif diff_x == 1:
                    for j in range(x, x+(diff_x*long[i])):
                        if (j > 9) or (grille2[j][y] == 3):
                            valide = False

            if valide:
                if diff_x == -1:
                    for j in range(x, x+(diff_x*long[i]), -1):
                        grille2[j][y] = 3
                elif diff_x == 1:
                    for j in range(x, x+(diff_x*long[i])):
                        grille2[j][y] = 3
                elif diff_y == -1:
                    for j in range(y, y+(diff_y*long[i]), -1):
                        grille2[x][j] = 3
                elif diff_y == 1:
                    for j in range(y, y+(diff_y*long[i])):
                        grille2[x][j] = 3
                             

"""
Partie commandes menu jeu
"""


def play_guerre():
    global chemin_absolu
    pygame.mixer.music.load(chemin_absolu + "OST//Two Steps From Hell.mp3")
    pygame.mixer.music.play(loops = -1)


# Réaction suite à un clic sur le plateau (bateau touché)
def play_explosion():
    global chemin_absolu
    son_touche = pygame.mixer.Sound(chemin_absolu + "OST//explosion.mp3")
    son_touche.play(loops = 0)
    son_touche.set_volume(0.1)


# Réaction suite à un clic sur le plateau (bateau raté)
def play_splash():
    global chemin_absolu
    son_rate = pygame.mixer.Sound(chemin_absolu + "OST//splash.mp3")
    son_rate.play(loops = 0)
    son_rate.set_volume(0.1)


# Ouverture des règles
def open():
    global chemin_absolu
    return webbrowser.open(chemin_absolu + 'Site\\Règles.html')


# Lancement de la partie
def lancement_jouer():
    global stop_duree
    global flag_partie_prete
    global bouton_jouer_frame_jeu
    stop_duree = False
    flag_partie_prete = True
    bouton_jouer_frame_jeu.destroy()
    bouton_retour_frame_jeu['state'] = DISABLED
    duree_partie()
    play_guerre()
    
    
# Attribution de l'intéraction utilisateur avec le plateau 2
def bind_jeu():
    creer_symboles()
    plateau2.bind("<Button-1>", clic_plateau_jeu2)
    root.bind("<KeyRelease-Escape>", cheat)
    

# Calcule la durée d'une partie
def duree_partie():
    global duree
    global chrono
    global stop_duree
    duree += 1
    chrono.itemconfig(1, text = str(duree), font = ("LeviBrush", 25), fill = "white")
    if not stop_duree:
        frame_jeu.after(1000, duree_partie)
 
        
# Reset la durée d'une partie
def reset_duree_partie():
    global duree
    duree = 0
    
    
# Fonction utile si implémentation du réseau
def clic_plateau_jeu1(event):
    global flag_partie_prete
    if flag_partie_prete:
        global tour
        print("tour=", tour)
        if tour == 1:
            i = event.y // TAILLE_DE_CARRES
            j = event.x // TAILLE_DE_CARRES
            if grille1[i][j] == 0:
                tour = 2
                grille1[i][j] = 1
                plateau1.itemconfigure(i * 10 + j + 1, fill="white")
                print(grille1)
                print("Ligne=", i + 1, "Colonne=", j + 1)
            elif grille1[i][j] == 3:
                tour = 2
                grille1[i][j] = 1
                plateau1.itemconfigure(i * 10 + j + 1, fill="red")
                print(grille1)
                print("Ligne=", i + 1, "Colonne=", j + 1)
            else:
                print("Veuillez sélectionner une autre case")
            test_victoire()
        else:
            print("Ce n'est pas votre tour")
    else:
        print("configurer bateaux")


def creer_symboles():
    global chemin_absolu
    global explo
    explo = PhotoImage(file = chemin_absolu + "Images\\explosion.png")

    global plouf 
    plouf = PhotoImage(file = chemin_absolu + "Images\\plouf.png")
    

def clic_plateau_jeu2(event):
    global explo
    global plouf
    global affich_plouf
    global total_sante_b
    global sante_bot
    global action_joueur
    global coords
    global flag_partie_prete
    print(flag_partie_prete)
    if flag_partie_prete:
        global tour
        print("tour=", tour)
        if tour == 2:
            i = event.y // TAILLE_DE_CARRES
            j = event.x // TAILLE_DE_CARRES
            if grille2[i][j] == 0:
                tour = 1
                grille2[i][j] = 1
                plateau2.create_image(j*TAILLE_DE_CARRES+3,i*TAILLE_DE_CARRES+3, image = plouf, anchor=NW, tags = "images")
                action_joueur.destroy()
                action_joueur = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_joueur.grid(row = 16, column = 25, sticky = "nsew")
                action_joueur.create_text(160, 25, text = entrer_pseudo.get() + " tire en " + coords[i] + str(j+1) + " : RATÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_splash()
            elif grille2[i][j] == 3:
                tour = 1
                grille2[i][j] = 2
                plateau2.create_image(j*TAILLE_DE_CARRES+2,i*TAILLE_DE_CARRES, image = explo, anchor=NW, tags = "images")
                total_sante_b -= 100/17
                sante_bot['value'] = total_sante_b
                action_joueur.destroy()
                action_joueur = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_joueur.grid(row = 16, column = 25, sticky = "nsew")
                action_joueur.create_text(170, 25, text = entrer_pseudo.get() + " tire en " + coords[i] + str(j+1) + " : TOUCHÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_explosion()
            else:
                print("Veuillez sélectionner une autre case")
            test_victoire2()
        else:
            print("Ce n'est pas votre tour")
        if niv_facile:
            frame_jeu.after(700, bot_facile)
        if niv_moyen:
            frame_jeu.after(700, bot_moyen)
        if niv_difficile:
            frame_jeu.after(700, bot_difficile)
    else:
        print("configurer bateaux")

                 
# Actions du bot si difficulté facile enclenchée
def bot_facile():
    global explo
    global plouf
    global affich_plouf
    global total_sante
    global sante_joueur
    global coords
    global action_bot
    global flag_partie_prete
    if flag_partie_prete:
        global tour
        print("tour=", tour)
        if tour == 1:
            i = random.randint(0,9)
            j = random.randint(0,9)
            while (grille1[i][j] != 0) and (grille1[i][j] != 3) and (grille1[i][j] != 4):
                i = random.randint(0,9)
                j = random.randint(0,9)
            if grille1[i][j] == 0:
                tour = 2
                grille1[i][j] = 1
                affich_plouf = plateau1.create_image(j*TAILLE_DE_CARRES+3,i*TAILLE_DE_CARRES+3, image = plouf, anchor=NW, tags = "images")
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(180, 25, text = "Bot facile tire en " + coords[i] + str(j+1) + " : RATÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_splash()
            elif grille1[i][j] == 3:
                tour = 2
                grille1[i][j] = 2
                plateau1.create_image(j*TAILLE_DE_CARRES+2,i*TAILLE_DE_CARRES, image = explo, anchor=NW, tags = "images")
                total_sante -= 100/17
                sante_joueur['value'] = total_sante
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(190, 25, text = "Bot facile tire en " + coords[i] + str(j+1) + " : TOUCHÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_explosion()
            test_victoire1()


# Action du bot si difficulté moyen enclenchée
def bot_moyen():
    global explo
    global plouf
    global affich_plouf
    global total_sante
    global sante_joueur
    global coords
    global action_bot
    global flag_partie_prete
    chance = [0,0,3]
    tir = chance[random.randint(0,2)]
    if flag_partie_prete:
        global tour
        print("tour=", tour)
        if tour == 1:
            i = random.randint(0,9)
            j = random.randint(0,9)
            while (grille1[i][j] != tir) and (grille1[i][j] != 4):
                i = random.randint(0,9)
                j = random.randint(0,9)
            if grille1[i][j] == 0:
                tour = 2
                grille1[i][j] = 1
                affich_plouf = plateau1.create_image(j*TAILLE_DE_CARRES+3,i*TAILLE_DE_CARRES+3, image = plouf, anchor=NW, tags = "images")
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                                    bg = "#141414",
                                    border = 0, 
                                    highlightthickness = 0,
                                    width = 100,
                                    height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(180, 25, text = "Bot moyen tire en " + coords[i] + str(j+1) + " : RATÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_splash()
            elif grille1[i][j] == 3:
                tour = 2
                grille1[i][j] = 2
                plateau1.create_image(j*TAILLE_DE_CARRES+2,i*TAILLE_DE_CARRES, image = explo, anchor=NW, tags = "images")
                total_sante -= 100/17
                sante_joueur['value'] = total_sante
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(190, 25, text = "Bot moyen tire en " + coords[i] + str(j+1) + " : TOUCHÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_explosion()
            test_victoire1()


# Action du bot si difficulté difficile enclenchée
def bot_difficile():
    global explo
    global plouf
    global affich_plouf
    global total_sante
    global sante_joueur
    global coords
    global action_bot
    global flag_partie_prete
    chance = [0,3]
    tir = chance[random.randint(0,1)]
    if flag_partie_prete:
        global tour
        print("tour=", tour)
        if tour == 1:
            i = random.randint(0,9)
            j = random.randint(0,9)
            while (grille1[i][j] != tir) and (grille1[i][j] != 4):
                i = random.randint(0,9)
                j = random.randint(0,9)
            if grille1[i][j] == 0:
                tour = 2
                grille1[i][j] = 1
                affich_plouf = plateau1.create_image(j*TAILLE_DE_CARRES+3,i*TAILLE_DE_CARRES+3, image = plouf, anchor=NW, tags = "images")
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(190, 25, text = "Bot difficile tire en " + coords[i] + str(j+1) + " : RATÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_splash()
            elif grille1[i][j] == 3:
                tour = 2
                grille1[i][j] = 2
                plateau1.create_image(j*TAILLE_DE_CARRES+2,i*TAILLE_DE_CARRES, image = explo, anchor=NW, tags = "images")
                total_sante -= 100/17
                print(total_sante)
                sante_joueur['value'] = total_sante
                action_bot.destroy()
                action_bot = Canvas(frame_jeu,
                            bg = "#141414",
                            border = 0, 
                            highlightthickness = 0,
                            width = 100,
                            height = 50)
                action_bot.grid(row = 16, column = 5, sticky = "nsew")
                action_bot.create_text(190, 25, text = "Bot difficile tire en " + coords[i] + str(j+1) + " : TOUCHÉ !", font = ("Andi 20 bold", 19), fill = "white")
                play_explosion()
            test_victoire1()


def test_victoire1():
    global mode
    global score
    global stop_duree
    global precision_bot, precision_joueur
    if victoire1():
        precision_bot, precision_joueur = fin_de_partie()
        canvas_frame_victoire_titre.itemconfig(1, text = "D E F A I T E")
        canvas_frame_victoire_mode.itemconfig(1, text = "M O D E : " + mode)
        canvas_frame_victoire_winstreak.itemconfig(1, text = "Victoires d'affilées  :" + str(score + 1))
        canvas_frame_victoire_sante.itemconfig(1, text = "Santé restante : " + str(int(total_sante)) + "%")
        canvas_frame_victoire_timer.itemconfig(1, text = "Durée de la partie : " + str(duree) + "s")
        canvas_frame_victoire_precision_joueur.itemconfig(1, text = "Précision de vos tirs : " + str(int(precision_joueur)) + "%")
        canvas_frame_victoire_precision_bot.itemconfig(1, text = "Précision des tirs adverses : " + str(int(precision_bot)) + "%")
        stop_duree = True
        play_defeat()
        affichage_frame(frame_victoire)


def test_victoire2():
    global mode
    global score
    global stop_duree
    global precision_bot, precision_joueur
    if victoire2():
        precision_bot, precision_joueur = fin_de_partie()
        canvas_frame_victoire_titre.itemconfig(1, text = "V I C T O I R E")
        canvas_frame_victoire_mode.itemconfig(1, text = "M O D E : " + mode)
        canvas_frame_victoire_winstreak.itemconfig(1, text = "Victoires d'affilées  :" + str(score + 1))
        canvas_frame_victoire_sante.itemconfig(1, text = "Santé restante : " + str(int(total_sante)) + "%")
        canvas_frame_victoire_timer.itemconfig(1, text = "Durée de la partie : " + str(duree) + "s")
        canvas_frame_victoire_precision_joueur.itemconfig(1, text = "Précision de vos tirs : " + str(int(precision_joueur)) + "%")
        canvas_frame_victoire_precision_bot.itemconfig(1, text = "Précision des tirs adverses : " + str(int(precision_bot)) + "%")
        stop_duree = True
        play_victory()
        affichage_frame(frame_victoire)
        
    
# Réinitialisation de la couleur des plateaux
def reset_plateaux():
    global plouf, explo
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            plateau1.itemconfig(i * 10 + j + 1, fill = "#097ade")
            plateau2.itemconfig(i * 10 + j + 1, fill = "#097ade")
    plateau1.delete("images")
    plateau2.delete("images")
            
            
# Réinitialisation de la santé
def reset_sante():
    global total_sante, total_sante_b
    total_sante = 100
    total_sante_b = 100
    global sante_bot
    sante_bot['value'] = 100
    global sante_joueur
    sante_joueur['value'] = 100

    
# Cheat Code
def cheat(event):
    global flip
    if flip == 0:
        for i in range(NOMBRE_DE_CARRES):
            for j in range(NOMBRE_DE_CARRES):
                if grille2[i][j] == 3 or grille2[i][j] == 2:
                    plateau2.itemconfigure(i * 10 + j + 1, fill = "yellow")
        flip = 1
    else:
        for i in range(NOMBRE_DE_CARRES):
            for j in range(NOMBRE_DE_CARRES):
                if grille2[i][j] == 3:
                    plateau2.itemconfigure(i * 10 + j + 1, fill = "#097ade")
        flip = 0
                    

"""
Partie graphique fenêtre placement
"""


# Fonction qui crée le placement
def placementTK():
    # Utilisation des fonctions permettant de construire le placement
    creation_fenetre_placement()
    creation_canvas_placement()
    creation_plateau_placement()
    creation_bouton_placement()
    creation_bateaux_placement()
    creation_bind_placement()
    play_prep()
    
    # On cache la fenêtre principale
    root.withdraw()
    
    # Permet de "loop" le programme ce qui donne l'impression d'animation (alors que ce ne sont que des images)
    placement.mainloop()
    
    
# Fonction créant la fenêtre de placement ainsi que tout ses attributs (taille, titre...)
def creation_fenetre_placement():
    # Création d'une fenêtre tkinter pour placer les bateaux
    global placement
    placement = Tk()
    
    # Définition de la taille de la fenêtre
    LARGEUR_PLACEMENT = 800
    HAUTEUR_PLACEMENT = 600
    
    # Définition de la taille de l'écran
    global LARGEUR_ECRAN, HAUTEUR_ECRAN
    
    # Positionnement de la fenêtre au milieu de l'écran et application de la taille
    x = (LARGEUR_ECRAN / 2) - (LARGEUR_PLACEMENT / 2)
    y = (HAUTEUR_ECRAN / 2) - (HAUTEUR_PLACEMENT / 2)
    # Positionnement de la fenêtre au milieu de l'écran et application de la taille
    placement.geometry("%dx%d+%d+%d" %(LARGEUR_PLACEMENT, HAUTEUR_PLACEMENT, x, y))
    
    # Attribue une couleur au fond de la fenêtre
    placement.configure(bg = "#141414")
    
    # Empêche le mouvement de la fenêtre et la fermeture classique
    placement.overrideredirect(1)
    
    
# Création du canvas texte dans le placement
def creation_canvas_placement():
    # Création du canvas
    global commentaire
    commentaire = Canvas(placement,
                         bg = "#141414",
                         width = 800,
                         height = 150,
                         highlightthickness = 0)
    
    # Positionnement du canvas
    commentaire.place(x = 400, y = 100, anchor = CENTER)
    
    # On crée un texte dans le canvas (les canvas textes causent moins de problèmes dans le positionnement que les labels)
    commentaire.create_text(400, 75, text = "Positionner vos navires Major !", font = ("LeviBrush 30 bold"), fill = "white")
    
    
# Creation du plateau dans la fenêtre placement
def creation_plateau_placement():
    # Création du plateau
    plateau_placement = Canvas(placement,
                               width = DIMENSION, 
                               height = DIMENSION,
                               highlightthickness = 0,
                               bg = "red")
    
    # Positionnement du plateau
    plateau_placement.place(x = DEP_X, y = DEP_Y)
    
    # On remplit le plateau d'un quadrillage de NOMBRE_DE_CARRES par NOMBRE_DE_CARRES
    for i in range(NOMBRE_DE_CARRES):
        for j in range(NOMBRE_DE_CARRES):
            x, y = TAILLE_DE_CARRES * j, TAILLE_DE_CARRES * i 
            A, B = (x, y), (x + TAILLE_DE_CARRES, y + TAILLE_DE_CARRES)
            plateau_placement.create_rectangle(A, B, fill="#097ade")
            

# Création du bouton dans la fenêtre placement
def creation_bouton_placement():
    
    
    # Fonctions liées aux binds (permet un changement de couleur du bouton si le bouton est actif et ainsi de mieux visualiser la souris sur le bouton)
    def survol(event):
        if bouton_placement['state'] == NORMAL:
                bouton_placement.config(background = "#4BD5F5",
                                        foreground = "#141414")
                play_button()
                
                
    def fin_survol(event):
        if bouton_placement['state'] == NORMAL:
            bouton_placement.config(background = "#141414",
                                    foreground = "#4BD5F5")
            play_button()
            
            
    def clic(event):
        play_clic()
            
            
    # Création du bouton
    global bouton_placement   
    bouton_placement = Button(placement,
                             text = "L A N C E R",
                             bg = "#141414",
                             fg = "#4BD5F5",
                             border = 0,
                             activeforeground = "#4BD5F5",
                             activebackground = "#141414",
                             font = ("Andi", 10),
                             state = DISABLED,
                             command = confirmer)
        
    # Positionnement du bouton
    bouton_placement.place(x = 400, y = 540, anchor = CENTER)
    
    # Attribution des intéractions utilisateurs aux fonctions du dessus (survol...)
    bouton_placement.bind("<Enter>", survol)
    bouton_placement.bind("<Leave>", fin_survol)
    bouton_placement.bind("<Button-1>", clic)
    
    
# Création des canvas bateaux
def creation_bateaux_placement():
    # Création du bateau 1
    global bateau1
    bateau1 = Canvas(placement, bg = "gray", width = TAILLE_DE_CARRES * 2 - 1, height = TAILLE_DE_CARRES - 1, bd = 0, highlightthickness = 0)
    # Positionnement du bateau 1
    bateau1.place(x = 600, y = 161)
    
    # Création du bateau 2
    global bateau2
    bateau2 = Canvas(placement, bg = "green", width = TAILLE_DE_CARRES * 3 - 1, height = TAILLE_DE_CARRES - 1, bd = 0, highlightthickness = 0)
    # Positionnement du bateau 2
    bateau2.place(x = 600, y = 231)
    
    # Création du bateau 3
    global bateau3
    bateau3 = Canvas(placement, bg = "yellow", width = TAILLE_DE_CARRES * 3 - 1, height = TAILLE_DE_CARRES - 1, bd = 0, highlightthickness = 0)
    # Positionnement du bateau 3
    bateau3.place(x = 600, y = 301)
    
    # Création du bateau 4
    global bateau4
    bateau4 = Canvas(placement, bg = "blue", width = TAILLE_DE_CARRES * 4 - 1, height = TAILLE_DE_CARRES - 1, bd = 0, highlightthickness = 0)
    # Positionnement du bateau 4
    bateau4.place(x = 600, y = 371)
    
    # Création du bateau 5
    global bateau5
    bateau5 = Canvas(placement, bg = "orange", width = TAILLE_DE_CARRES * 5 - 1, height = TAILLE_DE_CARRES - 1, bd = 0, highlightthickness = 0)
    # Positionnement du bateau 5
    bateau5.place(x = 600, y = 441)
            
    
"""
Partie commandes fenêtre placement
"""


def play_prep():
    global chemin_absolu
    pygame.mixer.music.load(chemin_absolu + "OST//Rango Returns.mp3")
    pygame.mixer.music.play(loops = -1)
    
    
# Fonction qui calcule l'emplacement du clic souris sur un bateau
def clic_bateaux(event): 
    # Détermine quel bateau est concerné par le clic
    widget = event.widget
    
    # Détermine les coordonnés du clic
    widget.clicX = event.x
    widget.clicY = event.y
    
    # Suite au clic, on permet le déplacement et le placement du bateau 
    widget.bind("<B1-Motion>", deplacements_bateaux)
    widget.bind("<ButtonRelease-1>", positionnement)
    

# Fonction calculant le déplacement d'un bateau
def deplacements_bateaux(event):
    # Détermine quel bateau est concerné par le clic
    widget = event.widget
    
    # Détermine le déplacement de la souris
    x = widget.winfo_x() - widget.clicX + event.x
    y = widget.winfo_y() - widget.clicY + event.y
    
    # Positionne le bateau à l'endroit de la souris
    widget.place(x = x, y = y)
    print(x,y)
    # Flag de déplacement du bateau (sert au flip et positionnement)
    global bateau_statique
    bateau_statique = False
    return bateau_statique 


# Fonction de rotation des bateaux         
def spiderman_do_a_flip(event):
    # Détermine quel bateau est concerné par la rotation
    widget = event.widget
    
    # Détermine les coordonnées du bateau
    x = widget.winfo_x()
    y = widget.winfo_y()
    
    # Détermine la taille du bateau
    width = widget.winfo_width()
    height = widget.winfo_height() 
    
    # Rappel du flag de déplacement
    global bateau_statique
    
    # Si le bateau est en train d'être déplacé alors:
    if not bateau_statique:
        # Inversion de la hauteur et de la largeur (rotation)
        widget.configure(width=height, height=width)
        
        # Affichage d'un commentaire sur l'action effectuée
        commentaire.itemconfigure(1, text = "ROTATION EFFECTUE")
        
    # Si le bateau est statique alors:
    else:
        # On teste si le bateau est dans la grille de positionnement
        if (DEP_X <= x <= DEP_X + DIMENSION) and (DEP_X <= x + width <= DEP_X + DIMENSION) and (DEP_X <= x + height <= DEP_X + DIMENSION) and (DEP_Y <= y <= DEP_Y + DIMENSION) and (DEP_Y <= y + height <= DEP_Y + DIMENSION) and (DEP_Y <= y + width <= DEP_Y + DIMENSION):
            # Inversion de la hauteur et de la largeur (rotation)
            widget.configure(width=height, height=width)
            
            # Délai de 10ms avant l'éxécution de la fonction collisions (définition des hit-box et replacements de bateaux qui se touchent)
            placement.after(10, collisions, event)
            
            # Affichage d'un commentaire sur l'action effectuée
            commentaire.itemconfigure(1, text = "ROTATION EFFECTUE")
        else:
            # Affichage d'un commentaire sur l'action effectuée
            commentaire.itemconfigure(1, text = "ROTATION IMPOSSIBLE")
            
    placement.after(20, test_placement, event)
 
    
# Fonction qui permet le placement du bateau sur la grille
def positionnement(event):
    # Détermine quel bateau est concerné par la rotation
    widget = event.widget 
    
    # Détermine les coordonnées du bateau
    x = widget.winfo_x() 
    y = widget.winfo_y() 
    
    print(x, y)
    
    # Détermine la taille du bateau
    largeur = widget.winfo_width() 
    hauteur = widget.winfo_height() 
    
    # Forme des emplacements qui forment une grille "imaginaire" (en fonction du positionnement de la vraie grille) qui correspond exactement à la grille de notre plateau (cependant, la grille s'étend à toute la fenêtre)
    new_x = (x + 7) - (x + 7) % TAILLE_DE_CARRES + DEP_X % TAILLE_DE_CARRES + 1 
    new_y = y - y % TAILLE_DE_CARRES + DEP_Y % TAILLE_DE_CARRES + 1
    
    # Test de présence du bateau sur la grille du plateau
    if DEP_X < new_x < DIMENSION + DEP_X and DEP_Y < new_y < DIMENSION + DEP_Y and x + largeur - TAILLE_DE_CARRES // 2 < DIMENSION + DEP_X and y + hauteur - TAILLE_DE_CARRES // 2 < DIMENSION + DEP_Y: # On teste içi si les points appartiennent à la grille du plateau
        # Positionnement du bateau sur l'emplacement de grille (effet de collage)   
        widget.place(x=new_x, y=new_y)
        
        # Délai de 10ms avant l'éxécution de la fonction collisions (définition des hit-box et replacements de bateaux qui se touchent)
        placement.after(10, collisions, event)
    else:
        widget.place(x=x, y=y)
    
    # Délai de 20ms avant l'éxécution de la fonction test_placement (test de présence des bateaux sur la grille)
    placement.after(20, test_placement, event)
    
    # Flag de déplacement remis à son état par défaut
    global bateau_statique
    bateau_statique = True
    return bateau_statique
        

# Attribution d'intéractions utilisateurs aux bateaux
def creation_bind_placement():
    bateau1.bind("<Button-1>", clic_bateaux)    
    bateau1.bind("<Button-3>", spiderman_do_a_flip)
    
    bateau2.bind("<Button-1>", clic_bateaux)
    bateau2.bind("<Button-3>", spiderman_do_a_flip)
        
    bateau3.bind("<Button-1>", clic_bateaux)
    bateau3.bind("<Button-3>", spiderman_do_a_flip)
        
    bateau4.bind("<Button-1>", clic_bateaux)
    bateau4.bind("<Button-3>", spiderman_do_a_flip)
        
    bateau5.bind("<Button-1>", clic_bateaux)
    bateau5.bind("<Button-3>", spiderman_do_a_flip)
        

# Vérifie si les bateaux sont correctements positionnés sur la grille du plateau
def test_placement(event):
    # Attribution des coordonnées des bateaux à des variables afin de connaître leurs localisations précises
    x1_bateau1 = bateau1.winfo_x() 
    x2_bateau1 = bateau1.winfo_x() + bateau1.winfo_width()
    y1_bateau1 = bateau1.winfo_y()
    y2_bateau1 = bateau1.winfo_y() + bateau1.winfo_height()
        
    x1_bateau2 = bateau2.winfo_x() 
    x2_bateau2 = bateau2.winfo_x() + bateau2.winfo_width()
    y1_bateau2 = bateau2.winfo_y()
    y2_bateau2 = bateau2.winfo_y() + bateau2.winfo_height()
        
    x1_bateau3 = bateau3.winfo_x() 
    x2_bateau3 = bateau3.winfo_x() + bateau3.winfo_width()
    y1_bateau3 = bateau3.winfo_y()
    y2_bateau3 = bateau3.winfo_y() + bateau3.winfo_height()
        
    x1_bateau4 = bateau4.winfo_x() 
    x2_bateau4 = bateau4.winfo_x() + bateau4.winfo_width()
    y2_bateau4 = bateau4.winfo_y()
    y2_bateau4 = bateau4.winfo_y() + bateau4.winfo_height()
        
    x1_bateau5 = bateau5.winfo_x() 
    x2_bateau5 = bateau5.winfo_x() + bateau5.winfo_width()
    y1_bateau5 = bateau5.winfo_y()
    y2_bateau5 = bateau5.winfo_y() + bateau5.winfo_height() 
    
    # Première vérification: On teste si le point supérieur gauche du bateau est dans un coin de quadrillage
    # On place chaque coordonnées de coin de quadrillage dans une liste
    liste_positions_x_grille = []
    for i in range(NOMBRE_DE_CARRES):
        liste_positions_x_grille.append(DEP_X + TAILLE_DE_CARRES * i + 1)
    
    # Ici on effectue la vérification  
    global flag_bateau1_en_place 
    if x1_bateau1 in liste_positions_x_grille:
        flag_bateau1_en_place = True
    else:
        flag_bateau1_en_place = False
        
    global flag_bateau2_en_place    
    if x1_bateau2 in liste_positions_x_grille:
        flag_bateau2_en_place = True
    else:
        flag_bateau2_en_place = False
    
    global flag_bateau3_en_place
    if x1_bateau3 in liste_positions_x_grille:
        flag_bateau3_en_place = True
    else:
        flag_bateau3_en_place = False
    
    global flag_bateau4_en_place
    if x1_bateau4 in liste_positions_x_grille:
        flag_bateau4_en_place = True
    else:
        flag_bateau4_en_place = False
    
    global flag_bateau5_en_place
    if x1_bateau5 in liste_positions_x_grille:
        flag_bateau5_en_place = True
    else:
        flag_bateau5_en_place = False
    
    # Attribution des valeurs de tout les flags (avec un AND) à un seul flag
    flag_bateaux_en_place = flag_bateau1_en_place and flag_bateau2_en_place and flag_bateau3_en_place and flag_bateau4_en_place and flag_bateau5_en_place
    
    # Deuxième vérification: On teste si les bateaux sont sur le plateau
    flag_bateau1_dans_grille = (DEP_X <= x1_bateau1 <= DEP_X + DIMENSION) and (DEP_X <= x2_bateau1 <= DEP_X + DIMENSION) and (DEP_Y <= y1_bateau1 <= DEP_Y + DIMENSION) and (DEP_Y <= y2_bateau1 <= DEP_Y + DIMENSION)
    flag_bateau2_dans_grille = (DEP_X <= x1_bateau2 <= DEP_X + DIMENSION) and (DEP_X <= x2_bateau2 <= DEP_X + DIMENSION) and (DEP_Y <= y1_bateau2 <= DEP_Y + DIMENSION) and (DEP_Y <= y2_bateau2 <= DEP_Y + DIMENSION)
    flag_bateau3_dans_grille = (DEP_X <= x1_bateau3 <= DEP_X + DIMENSION) and (DEP_X <= x2_bateau3 <= DEP_X + DIMENSION) and (DEP_Y <= y1_bateau3 <= DEP_Y + DIMENSION) and (DEP_Y <= y2_bateau3 <= DEP_Y + DIMENSION)
    flag_bateau4_dans_grille = (DEP_X <= x1_bateau4 <= DEP_X + DIMENSION) and (DEP_X <= x2_bateau4 <= DEP_X + DIMENSION) and (DEP_Y <= y2_bateau4 <= DEP_Y + DIMENSION) and (DEP_Y <= y2_bateau4 <= DEP_Y + DIMENSION)
    flag_bateau5_dans_grille = (DEP_X <= x1_bateau5 <= DEP_X + DIMENSION) and (DEP_X <= x2_bateau5 <= DEP_X + DIMENSION) and (DEP_Y <= y1_bateau5 <= DEP_Y + DIMENSION) and (DEP_Y <= y2_bateau5 <= DEP_Y + DIMENSION)
    
    # Attribution des valeurs de tout les flags de vérification de présence dans la grille à un seul flag
    flag_bateaux_dans_grille = flag_bateau1_dans_grille and flag_bateau2_dans_grille and flag_bateau3_dans_grille and flag_bateau4_dans_grille and flag_bateau5_dans_grille
    
    # Si tous les bateaux sont dans le plateau et qu'ils sont dans la grille alors la confirmation se déverrouille
    if flag_bateaux_dans_grille and flag_bateaux_en_place: 
        global bouton_placement
        bouton_placement['state'] = NORMAL
        commentaire.itemconfigure(1, text ="Flotte en position Major!")
    else:
        bouton_placement['state'] = DISABLED
        commentaire.itemconfigure(1, text ="En attente de placement")
        

# Définition et détection de toutes les hitbox des bateaux
def collisions(event):
    # Coordonées 1er bateau
    x1_bateau1 = bateau1.winfo_x()
    largeur_bateau1 = bateau1.winfo_width()
    x2_bateau1 = x1_bateau1 + largeur_bateau1
    
    y1_bateau1 = bateau1.winfo_y()
    hauteur_bateau1 = bateau1.winfo_height()
    y2_bateau1 = y1_bateau1 + hauteur_bateau1
    
    # Coordonées 2e bateau
    x1_bateau2 = bateau2.winfo_x()
    largeur_bateau2 = bateau2.winfo_width()
    x2_bateau2 = x1_bateau2 + largeur_bateau2
    
    y1_bateau2 = bateau2.winfo_y()
    hauteur_bateau2 = bateau2.winfo_height()
    y2_bateau2 = y1_bateau2 + hauteur_bateau2
    
    # Coordonées 3e bateau
    x1_bateau3 = bateau3.winfo_x()
    largeur_bateau3 = bateau3.winfo_width()
    x2_bateau3 = x1_bateau3 + largeur_bateau3
    
    y1_bateau3 = bateau3.winfo_y()
    hauteur_bateau3 = bateau3.winfo_height()
    y2_bateau3 = y1_bateau3 + hauteur_bateau3
    
    # Coordonées 4e bateau
    x1_bateau4 = bateau4.winfo_x()
    largeur_bateau4 = bateau4.winfo_width()
    x2_bateau4 = x1_bateau4 + largeur_bateau4
    
    y1_bateau4 = bateau4.winfo_y()
    hauteur_bateau4 = bateau4.winfo_height()
    y2_bateau4 = y1_bateau4 + hauteur_bateau4
    
    # Coordonées 5e bateau
    x1_bateau5 = bateau5.winfo_x()
    largeur_bateau5 = bateau5.winfo_width()
    x2_bateau5 = x1_bateau5 + largeur_bateau5
    
    y1_bateau5 = bateau5.winfo_y()
    hauteur_bateau5 = bateau5.winfo_height()
    y2_bateau5 = y1_bateau5 + hauteur_bateau5
        
    # Détermine quel bateau est concerné
    widget = event.widget
        
    # Si un des test ci-dessous échoue, alors le bateau qui entre en collision avec un autre (qui est en position sur le plateau) est repositionné à sa position de départ
    # Test de collision entre bateau1 et bateau2
    if x2_bateau1 >= x1_bateau2 and y2_bateau1 >= y1_bateau2 and x2_bateau2 >= x1_bateau1 and y2_bateau2 >= y1_bateau1: 
        if widget.winfo_width() == largeur_bateau1 and widget.winfo_height() == hauteur_bateau1 or widget.winfo_width() == hauteur_bateau1 and widget.winfo_height() == largeur_bateau1:
            widget.place(x = 600, y = 161)
        if widget.winfo_width() == largeur_bateau2 and widget.winfo_height() == hauteur_bateau2 or widget.winfo_width() == hauteur_bateau2 and widget.winfo_height() == largeur_bateau2:
            widget.place(x = 600, y = 231)
            
    # Test de collision entre bateau1 et bateau3
    elif x2_bateau1 >= x1_bateau3 and y2_bateau1 >= y1_bateau3 and x2_bateau3 >= x1_bateau1 and y2_bateau3 >= y1_bateau1:
        if widget.winfo_width() == largeur_bateau1 and widget.winfo_height() == hauteur_bateau1 or widget.winfo_width() == hauteur_bateau1 and widget.winfo_height() == largeur_bateau1:
            widget.place(x = 600, y = 161)
        if widget.winfo_width() == largeur_bateau3 and widget.winfo_height() == hauteur_bateau3 or widget.winfo_width() == hauteur_bateau3 and widget.winfo_height() == largeur_bateau3:
            widget.place(x = 600, y = 301) 
            
    # Test de collision entre bateau1 et bateau4
    elif x2_bateau1 >= x1_bateau4 and y2_bateau1 >= y1_bateau4 and x2_bateau4 >= x1_bateau1 and y2_bateau4 >= y1_bateau1:
        if widget.winfo_width() == largeur_bateau1 and widget.winfo_height() == hauteur_bateau1 or widget.winfo_width() == hauteur_bateau1 and widget.winfo_height() == largeur_bateau1:
            widget.place(x = 600, y = 161)
        if widget.winfo_width() == largeur_bateau4 and widget.winfo_height() == hauteur_bateau4 or widget.winfo_width() == hauteur_bateau4 and widget.winfo_height() == largeur_bateau4:
            widget.place(x = 600, y = 371) 
            
    # Test de collision entre bateau1 et bateau5
    elif x2_bateau1 >= x1_bateau5 and y2_bateau1 >= y1_bateau5 and x2_bateau5 >= x1_bateau1 and y2_bateau5 >= y1_bateau1:
        if widget.winfo_width() == largeur_bateau1 and widget.winfo_height() == hauteur_bateau1 or widget.winfo_width() == hauteur_bateau1 and widget.winfo_height() == largeur_bateau1:
            widget.place(x = 600, y = 161)
        if widget.winfo_width() == largeur_bateau5 and widget.winfo_height() == hauteur_bateau5 or widget.winfo_width() == hauteur_bateau5 and widget.winfo_height() == largeur_bateau5:
            widget.place(x = 600, y = 441) 
            
    # Test de collision entre bateau2 et bateau3
    elif x2_bateau2 >= x1_bateau3 and y2_bateau2 >= y1_bateau3 and x2_bateau3 >= x1_bateau2 and y2_bateau3 >= y1_bateau2:
        if widget.winfo_width() == largeur_bateau2 and widget.winfo_height() == hauteur_bateau2 or widget.winfo_width() == hauteur_bateau2 and widget.winfo_height() == largeur_bateau2:
            widget.place(x = 600, y = 231)
        if widget.winfo_width() == largeur_bateau3 and widget.winfo_height() == hauteur_bateau3 or widget.winfo_width() == hauteur_bateau3 and widget.winfo_height() == largeur_bateau3:
            widget.place(x = 600, y = 301) 
            
    # Test de collision entre bateau2 et bateau4
    elif x2_bateau2 >= x1_bateau4 and y2_bateau2 >= y1_bateau4 and x2_bateau4 >= x1_bateau2 and y2_bateau4 >= y1_bateau2:
        if widget.winfo_width() == largeur_bateau2 and widget.winfo_height() == hauteur_bateau2 or widget.winfo_width() == hauteur_bateau2 and widget.winfo_height() == largeur_bateau2:
            widget.place(x = 600, y = 231)
        if widget.winfo_width() == largeur_bateau4 and widget.winfo_height() == hauteur_bateau4 or widget.winfo_width() == hauteur_bateau4 and widget.winfo_height() == largeur_bateau4:
            widget.place(x = 600, y = 371) 
            
    # Test de collision entre bateau2 et bateau5
    elif x2_bateau2 >= x1_bateau5 and y2_bateau2 >= y1_bateau5 and x2_bateau5 >= x1_bateau2 and y2_bateau5 >= y1_bateau2:
        if widget.winfo_width() == largeur_bateau2 and widget.winfo_height() == hauteur_bateau2 or widget.winfo_width() == hauteur_bateau2 and widget.winfo_height() == largeur_bateau2:
            widget.place(x = 600, y = 231)
        if widget.winfo_width() == largeur_bateau5 and widget.winfo_height() == hauteur_bateau5 or widget.winfo_width() == hauteur_bateau5 and widget.winfo_height() == largeur_bateau5:
            widget.place(x = 600, y = 441)
            
    # Test de collision entre bateau3 et bateau4
    elif x2_bateau3 >= x1_bateau4 and y2_bateau3 >= y1_bateau4 and x2_bateau4 >= x1_bateau3 and y2_bateau4 >= y1_bateau3:
        if widget.winfo_width() == largeur_bateau3 and widget.winfo_height() == hauteur_bateau3 or widget.winfo_width() == hauteur_bateau3 and widget.winfo_height() == largeur_bateau3:
            widget.place(x = 600, y = 301)
        if widget.winfo_width() == largeur_bateau4 and widget.winfo_height() == hauteur_bateau4 or widget.winfo_width() == hauteur_bateau4 and widget.winfo_height() == largeur_bateau4:
            widget.place(x = 600, y = 371)
            
    # Test de collision entre bateau3 et bateau5
    elif x2_bateau3 >= x1_bateau5 and y2_bateau3 >= y1_bateau5 and x2_bateau5 >= x1_bateau3 and y2_bateau5 >= y1_bateau3:
        if widget.winfo_width() == largeur_bateau3 and widget.winfo_height() == hauteur_bateau3 or widget.winfo_width() == hauteur_bateau3 and widget.winfo_height() == largeur_bateau3:
            widget.place(x = 600, y = 301)
        if widget.winfo_width() == largeur_bateau5 and widget.winfo_height() == hauteur_bateau5 or widget.winfo_width() == hauteur_bateau5 and widget.winfo_height() == largeur_bateau5:
            widget.place(x = 600, y = 441)
            
    # Test de collision entre bateau4 et bateau5
    elif x2_bateau4 >= x1_bateau5 and y2_bateau4 >= y1_bateau5 and x2_bateau5 >= x1_bateau4 and y2_bateau5 >= y1_bateau4:
        if widget.winfo_width() == largeur_bateau4 and widget.winfo_height() == hauteur_bateau4 or widget.winfo_width() == hauteur_bateau4 and widget.winfo_height() == largeur_bateau4:
            widget.place(x = 600, y = 301)
        if widget.winfo_width() == largeur_bateau5 and widget.winfo_height() == hauteur_bateau5 or widget.winfo_width() == hauteur_bateau5 and widget.winfo_height() == largeur_bateau5:
            widget.place(x = 600, y = 441)
        

# Sauvegarde de la position des bateaux dans une grille et dans le plateau lié au jeu  
def confirmer():
    # Attribution des coordonnées des bateaux à des variables afin de connaître leurs localisations et tailles précises
    x_bateau1 = (bateau1.winfo_x() - DEP_X) // TAILLE_DE_CARRES
    largeur_bateau1 = bateau1.winfo_width()
    y_bateau1 = (bateau1.winfo_y() - DEP_Y) // TAILLE_DE_CARRES
    hauteur_bateau1 = bateau1.winfo_height()
        
    x_bateau2 = (bateau2.winfo_x() - DEP_X) // TAILLE_DE_CARRES
    largeur_bateau2 = bateau2.winfo_width()
    y_bateau2 = (bateau2.winfo_y() - DEP_Y) // TAILLE_DE_CARRES
    hauteur_bateau2 = bateau2.winfo_height()
        
    x_bateau3 = (bateau3.winfo_x() - DEP_X) // TAILLE_DE_CARRES
    largeur_bateau3 = bateau3.winfo_width()
    y_bateau3 = (bateau3.winfo_y() - DEP_Y) // TAILLE_DE_CARRES
    hauteur_bateau3 = bateau3.winfo_height()
        
    x_bateau4 = (bateau4.winfo_x() - DEP_X) // TAILLE_DE_CARRES
    largeur_bateau4 = bateau4.winfo_width()
    y_bateau4 = (bateau4.winfo_y() - DEP_Y) // TAILLE_DE_CARRES
    hauteur_bateau4 = bateau4.winfo_height()
        
    x_bateau5 = (bateau5.winfo_x() - DEP_X) // TAILLE_DE_CARRES
    largeur_bateau5 = bateau5.winfo_width()
    y_bateau5 = (bateau5.winfo_y() - DEP_Y) // TAILLE_DE_CARRES
    hauteur_bateau5 = bateau5.winfo_height() 
    
    # En fonction des coordonnées et de l'inclinaison du bateau, les cases du plateau sont coloriées
    global plateau1
    
    # Mise en couleur du bateau 1
    if (largeur_bateau1 > hauteur_bateau1):
        for i in range((largeur_bateau1 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau1][x_bateau1 + i] = 3
            plateau1.itemconfigure(y_bateau1 * 10 + x_bateau1 + i + 1,
                                       fill = "gray")
    else:
        for i in range((hauteur_bateau1 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau1 + i][x_bateau1] = 3
            plateau1.itemconfigure((y_bateau1 + i) * 10 + x_bateau1 + 1,
                                       fill="gray")
    
    # Mise en couleur du bateau 2
    if (largeur_bateau2 > hauteur_bateau2):
        for i in range((largeur_bateau2 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau2][x_bateau2 + i] = 3
            plateau1.itemconfigure(y_bateau2 * 10 + x_bateau2 + i + 1,
                                       fill = "green")
    else:
        for i in range((hauteur_bateau2 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau2 + i][x_bateau2] = 3
            plateau1.itemconfigure((y_bateau2 + i) * 10 + x_bateau2 + 1,
                                       fill="green")
    
    # Mise en couleur du bateau 3
    if (largeur_bateau3 > hauteur_bateau3):
        for i in range((largeur_bateau3 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau3][x_bateau3 + i] = 3
            plateau1.itemconfigure(y_bateau3 * 10 + x_bateau3 + i + 1,
                                       fill = "yellow")
    else:
        for i in range((hauteur_bateau3 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau3 + i][x_bateau3] = 3
            plateau1.itemconfigure((y_bateau3 + i) * 10 + x_bateau3 + 1,
                                       fill="yellow")
    
    # Mise en couleur du bateau 4
    if (largeur_bateau4 > hauteur_bateau4):
        for i in range((largeur_bateau4 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau4][x_bateau4 + i] = 3
            plateau1.itemconfigure(y_bateau4 * 10 + x_bateau4 + i + 1,
                                       fill = "blue")
    else:
        for i in range((hauteur_bateau4 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau4 + i][x_bateau4] = 3
            plateau1.itemconfigure((y_bateau4 + i) * 10 + x_bateau4 + 1,
                                       fill = "blue")
    
    # Mise en couleur du bateau 5
    if (largeur_bateau5 > hauteur_bateau5):
        for i in range((largeur_bateau5 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau5][x_bateau5 + i] = 3
            plateau1.itemconfigure(y_bateau5 * 10 + x_bateau5 + i + 1,
                                       fill = "orange")
    else:
        for i in range((hauteur_bateau5 + 1) // TAILLE_DE_CARRES):
            grille1[y_bateau5 + i][x_bateau5] = 3
            plateau1.itemconfigure((y_bateau5 + i) * 10 + x_bateau5 + 1,
                                       fill="orange")
            
    # Fermeture de la fenêtre de placement de bateaux     
    placement.destroy()
    
    # Destruction du bouton placer du menu jeu
    global bouton_placer_frame_jeu
    bouton_placer_frame_jeu.destroy()
    
    # Positionnement du bouton jouer du menu jeu (à la place de placer)
    global bouton_jouer_frame_jeu
    bouton_jouer_frame_jeu.grid(row = 14, column = 15, sticky = "nsew")
    
    # On fait réapparaître la fenêtre principale
    root.deiconify()
    
    
"""
Partie graphique pop up victoire
"""

    
def creation_ecran_victoire():
    carreaux_victoire()
    creation_boutons_frame_victoire()
    creation_canvas_frame_victoire()
    
    
# Création d'une grille ixi invisible pour le bon placement des widgets
def carreaux_victoire():
    for i in range(31):
        frame_victoire.rowconfigure(i, weight = 1)
        frame_victoire.columnconfigure(i, weight = 1)
        
        
# Fonction créant les boutons dans le frame victoire
def creation_boutons_frame_victoire():
    
    
    # Modèle de bouton (similaire à une classe en objet)
    def modele_boutons_frame_victoire(i, j, text, bgcolor, fgcolor, command):
        
        
        # Fonctions liées aux binds (permet un changement de couleur du bouton et ainsi de mieux visualiser la souris sur le bouton)
        def survol(event):
            bouton_frame_victoire.config(background = bgcolor,
                                         foreground = fgcolor)
            play_button()
                
                
        def fin_survol(event):
            bouton_frame_victoire.config(background = fgcolor,
                                         foreground = bgcolor)
            play_button()
            
            
        def clic(event):
            play_clic()
            
        
        # Création du bouton dans la fenêtre frame_victoire
        bouton_frame_victoire = Button(frame_victoire,
                                       text = text,
                                       bg = fgcolor,
                                       fg = bgcolor,
                                       border = 0,
                                       activeforeground = fgcolor,
                                       activebackground = bgcolor,
                                       font = ("Benguiat", 15),
                                       command = command)

        # Positionnement du bouton dans le frame victoire
        bouton_frame_victoire.grid(row = i, column = j, sticky = "nsew")
        
        # Attribution des intéractions utilisateurs aux fontions du dessus (survol...)
        bouton_frame_victoire.bind("<Enter>", survol)
        bouton_frame_victoire.bind("<Leave>", fin_survol)
        bouton_frame_victoire.bind("<Button-1>", clic)
        
        
    # Ici on crée des boutons à partir du modèle
    modele_boutons_frame_victoire(30, 1, "A B A N D O N N E R", "#ffa157", "#141414", lambda:abandonner())
    modele_boutons_frame_victoire(30, 29, "R E J O U E R", "#ffcc66", "#141414", lambda:rejouer())
    

# Création des canvas textes dans la fenêtre frame_victoire
def creation_canvas_frame_victoire():
    global canvas_frame_victoire_titre
    canvas_frame_victoire_titre = Canvas(frame_victoire,
                                         bg = "#141414",
                                         width = 500,
                                         height = 100,
                                         border = 0,
                                         highlightthickness = 0)
    
    canvas_frame_victoire_titre.grid(row = 3, column = 15, sticky = "nsew")
    canvas_frame_victoire_titre.create_text(200, 50, text = "V I C T O I R E", font = ("LeviBrush 35 underline"), fill = "white")
    
    global canvas_frame_victoire_mode
    canvas_frame_victoire_mode = Canvas(frame_victoire,
                                         bg = "#141414",
                                         width = 400,
                                         height = 60,
                                         border = 0,
                                         highlightthickness = 0)
    
    canvas_frame_victoire_mode.grid(row = 4, column = 15, sticky = "nsew")
    canvas_frame_victoire_mode.create_text(200, 30, text = "M O D E :", font = ("Andi 20"), fill = "white")
    
    global canvas_frame_victoire_winstreak
    canvas_frame_victoire_winstreak = Canvas(frame_victoire,
                                         bg = "#141414",
                                         width = 300,
                                         height = 60,
                                         border = 0,
                                         highlightthickness = 0)
    
    canvas_frame_victoire_winstreak.grid(row = 6, column = 15, sticky = "nsew")
    canvas_frame_victoire_winstreak.create_text(200, 30, text = "Victoires d'affilées ", font = ("Andi 20"), fill = "white")
    
    global canvas_frame_victoire_sante
    canvas_frame_victoire_sante = Canvas(frame_victoire,
                                         bg = "red",
                                         width = 100,
                                         height = 60,
                                         border = 0,
                                         highlightthickness = 0)
    
    canvas_frame_victoire_sante.grid(row = 13, column = 15, sticky = "nsew")
    canvas_frame_victoire_sante.create_text(200, 30, text = "Santé restante ", font = ("Andi 15 bold"), fill = "white")
    
    global canvas_frame_victoire_timer
    canvas_frame_victoire_timer = Canvas(frame_victoire,
                                         bg = "red",
                                         width = 100,
                                         height = 60,
                                         border = 0,
                                         highlightthickness = 0)
    
    canvas_frame_victoire_timer.grid(row = 15, column = 15, sticky = "nsew")
    canvas_frame_victoire_timer.create_text(200, 30, text = "Durée de la partie ", font = ("Andi 15 bold"), fill = "white")
    
    global canvas_frame_victoire_precision_joueur
    canvas_frame_victoire_precision_joueur = Canvas(frame_victoire,
                                             bg = "red",
                                             width = 100,
                                             height = 60,
                                             border = 0,
                                             highlightthickness = 0)
    
    canvas_frame_victoire_precision_joueur.grid(row = 18, column = 15, sticky = "nsew")
    canvas_frame_victoire_precision_joueur.create_text(200, 30, text = "Précision de vos tirs ", font = ("Andi 15 bold"), fill = "white")
    
    global canvas_frame_victoire_precision_bot
    canvas_frame_victoire_precision_bot = Canvas(frame_victoire,
                                             bg = "red",
                                             width = 100,
                                             height = 60,
                                             border = 0,
                                             highlightthickness = 0)
    
    canvas_frame_victoire_precision_bot.grid(row = 20, column = 15, sticky = "nsew")
    canvas_frame_victoire_precision_bot.create_text(200, 30, text = "Précision des tirs adverses ", font = ("Andi 15 bold"), fill = "white")
    
    
"""
Partie commandes pop up victoire
"""


def play_victory():
    global chemin_absolu
    pygame.mixer.music.load(chemin_absolu + "OST//Victory.mp3")
    pygame.mixer.music.play(loops = -1)
    pygame.mixer.music.set_volume(0.1)
    
    
def play_defeat():
    global chemin_absolu
    pygame.mixer.music.load(chemin_absolu + "OST//Defeat.mp3")
    pygame.mixer.music.play(loops = -1)
    pygame.mixer.music.set_volume(0.1)


def rejouer():
    # Reset les grilles des joueurs
    reInitialisation()
    
    # Reset de la couleur du plateau
    reset_plateaux()
    
    # Reset de la santé
    reset_sante()
    
    # Incrémentation du score
    global score
    score += 1
    
    # Réinitialisation de l'état de la partie
    global flag_partie_prete, tour
    flag_partie_prete = False
    tour = 2
    
    # Recréation du bouton placer et du bouton jouer
    creation_bouton_placer_jeu()
    creation_bouton_jouer_jeu()
    
    # On détruit et recrée le score, actions...
    action_joueur.destroy()
    action_bot.destroy()
    score_comm.destroy()
    chrono.destroy()
    
    creation_canvas_frame_jeu()
    
    # Repositionnement des bateaux adverses
    bateaux_bot()
    
    # On remet le temps à zéro
    reset_duree_partie()
    
    # Repositionnement sur le frame jeu
    affichage_frame(frame_jeu)
    

def abandonner():
    # Reset les grilles de joueurs
    reInitialisation()
    
    # Reset de la couleur du plateau
    reset_plateaux()
    
    # Reset de la santé
    reset_sante()
    
    # Remise à zéro du score
    reset_score()
    
    # Réinitialisation de l'état de la partie
    global flag_partie_prete, tour
    flag_partie_prete = False
    tour = 2
    
    # On détruit et recrée le score, actions...
    action_joueur.destroy()
    action_bot.destroy()
    score_comm.destroy()
    chrono.destroy()
    
    creation_canvas_frame_jeu()
    
    # Repositionnement des bateaux adverses
    bateaux_bot()
    
    # On remet le temps à zéro
    reset_duree_partie()
    
    # On réinitialise le frame personnalisation
    reset_difficultes()
    reset_entry() 
    
    # Repositionnement sur le frame_principal
    affichage_frame(frame_principal)
