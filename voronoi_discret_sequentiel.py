import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def calcul_voronoi(image, germes):
    """
    Algorithme séquentiel pour calculer le diagramme de Voronoï discret avec masques avant et arrière.

    Paramètres :
        image (numpy.ndarray) : Tableau représentant l'image (initialisé à np.inf).
        germes (list of tuples) : Liste des coordonnées des germes.

    Retourne :
        numpy.ndarray : Tableau contenant les indices des germes assignés à chaque pixel.
    """
    rows, cols = image.shape  # Récupération des dimensions de l'image (hauteur et largeur)

    # Création d'une matrice pour assigner chaque pixel à un germe, initialisée à -1 (aucun germe)
    voronoi_map = np.full((rows, cols), -1)

    # Initialisation des germes dans la carte Voronoï
    for idx, (x, y) in enumerate(germes):
        image[x, y] = 0  # La distance du germe à lui-même est 0
        voronoi_map[x, y] = idx  # Assigner un index au germe dans la carte Voronoï

    # Définition des masques de voisinage avant (haut, gauche, diagonaux) et arrière (bas, droite, diagonaux)
    masque_avant = [(0, -1), (-1, 0), (-1, -1), (-1, 1)]
    masque_arriere = [(0, 1), (1, 0), (1, -1), (1, 1)]

    # Étape avant : Parcours de l'image de haut-gauche à bas-droit
    for i in range(1, rows):
        for j in range(1, cols):
            min_distance = image[i, j]  # Initialisation de la distance minimale au pixel actuel
            closest_seed = voronoi_map[i, j]  # Récupération du germe associé au pixel
            # Vérification des voisins dans la direction "avant" (haut et gauche)
            for dx, dy in masque_avant:
                x, y = i + dx, j + dy
                # Vérification des limites de l'image pour éviter des erreurs d'indexation
                if 0 <= x < rows and 0 <= y < cols:
                    if image[x, y] + 1 < min_distance:  # Si un voisin est plus proche
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]  # Mise à jour du germe le plus proche
            image[i, j] = min_distance  # Mettre à jour la distance minimale pour le pixel
            voronoi_map[i, j] = closest_seed  # Mettre à jour le germe assigné au pixel

    # Étape arrière : Parcours de l'image de bas-droit à haut-gauche
    for i in range(rows - 2, -1, -1):
        for j in range(cols - 2, -1, -1):
            min_distance = image[i, j]  # Initialisation de la distance minimale
            closest_seed = voronoi_map[i, j]  # Initialisation du germe associé
            # Vérification des voisins dans la direction "arrière" (bas et droite)
            for dx, dy in masque_arriere:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    if image[x, y] + 1 < min_distance:  # Si un voisin est plus proche
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]  # Mise à jour du germe le plus proche
            image[i, j] = min_distance  # Mettre à jour la distance minimale pour le pixel
            voronoi_map[i, j] = closest_seed  # Mettre à jour le germe assigné au pixel

    return voronoi_map  # Retourner la carte de Voronoï, avec l'index des germes pour chaque pixel


def afficher_voronoi(voronoi_map, germes, nb_germes):
    """
    Affiche le diagramme de Voronoï discret avec des zones colorées.

    Paramètres :
        voronoi_map (numpy.ndarray) : Tableau des indices des germes assignés à chaque pixel.
        germes (list of tuples) : Liste des coordonnées des germes.
    """

    # Créer une palette de couleurs avec la fonction 'tab20' (20 couleurs distinctes)
    cmap = ListedColormap(plt.cm.get_cmap('tab20').colors[:nb_germes])

    # Créer une figure pour afficher l'image
    plt.figure(figsize=(8, 8))
    plt.imshow(voronoi_map, cmap=cmap, interpolation='nearest')  # Afficher la carte de Voronoï avec la palette

    # Afficher les positions des germes en rouge sur l'image
    for idx, (x, y) in enumerate(germes):
        plt.scatter(y, x, color='red', edgecolor='black', s=100, label=f"Germe {idx}")  # Marquer les germes
    
    plt.title(f"Diagramme de Voronoi Discret pour {nb_germes} germes")  # Titre de l'image
    plt.axis("off")  # Désactiver l'affichage des axes
    plt.show()  # Afficher l'image avec matplotlib


# Taille de l'image (500x500 pixels)
width, height = 500, 500

# Initialiser l'image avec des distances infinies
image = np.full((width, height), np.inf)

# Nombre de germes (20 dans cet exemple)
nb_germes = 20

# Générer des germes aléatoires dans l'image
germes = np.array([(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(nb_germes)])

# Calculer le diagramme de Voronoï en utilisant les germes générés
voronoi_map = calcul_voronoi(image, germes)

# Afficher le diagramme de Voronoï avec les germes marqués
afficher_voronoi(voronoi_map, germes, nb_germes)
