import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

# Fonction pour calculer le diagramme de Voronoï
def calcul_voronoi(image, germes):
    """
    Calcule la carte de Voronoï pour une image donnée et une liste de germes.

    Paramètres :
        image (numpy.ndarray) : Image contenant la distance minimale à chaque pixel.
        germes (list of tuples) : Liste des positions des germes.

    Retourne :
        numpy.ndarray : La carte de Voronoï, où chaque pixel est associé au germe le plus proche.
    """
    rows, cols = image.shape  # Récupère les dimensions de l'image
    voronoi_map = np.full((rows, cols), -1)  # Initialisation de la carte de Voronoï avec -1 (indiquant aucune zone assignée)

    # Assigner les germes à leur position sur la carte de Voronoï et marquer l'image
    for idx, (x, y) in enumerate(germes):
        image[x, y] = 0  # La distance du germe à lui-même est 0
        voronoi_map[x, y] = idx  # Chaque germe est assigné à son propre index dans la carte de Voronoï

    # Masques pour vérifier les voisins avant (en haut, gauche, diagonaux)
    masque_avant = [(0, -1), (-1, 0), (-1, -1), (-1, 1)]
    # Masques pour vérifier les voisins arrière (en bas, droite, diagonaux)
    masque_arriere = [(0, 1), (1, 0), (1, -1), (1, 1)]

    # Calculer les distances minimales depuis les germes vers le bas et la droite
    for i in range(1, rows):
        for j in range(1, cols):
            min_distance = image[i, j]  # Initialisation à la distance actuelle
            closest_seed = voronoi_map[i, j]  # Initialisation de l'indice du germe associé
            # Vérifier les voisins dans la direction "avant"
            for dx, dy in masque_avant:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:  # Assurer que les indices sont dans les limites
                    if image[x, y] + 1 < min_distance:  # Si une distance plus petite est trouvée
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]  # Mettre à jour le germe le plus proche
            image[i, j] = min_distance
            voronoi_map[i, j] = closest_seed

    # Vérifier les voisins arrière (en haut, gauche, diagonaux)
    for i in range(rows - 2, -1, -1):
        for j in range(cols - 2, -1, -1):
            min_distance = image[i, j]
            closest_seed = voronoi_map[i, j]
            # Vérifier les voisins dans la direction "arrière"
            for dx, dy in masque_arriere:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    if image[x, y] + 1 < min_distance:
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]
            image[i, j] = min_distance
            voronoi_map[i, j] = closest_seed

    return voronoi_map  # Retourne la carte de Voronoï calculée


# Fonction pour calculer la moyenne des couleurs dans chaque zone de Voronoï
def calculer_moyenne_couleurs(image, voronoi_map, nb_germes):
    """
    Calcule la moyenne des couleurs pour chaque zone de Voronoï.

    Paramètres :
        image (numpy.ndarray) : Image RGB sous forme de tableau numpy.
        voronoi_map (numpy.ndarray) : Carte des zones de Voronoï.
        nb_germes (int) : Nombre de germes.

    Retourne :
        dict : Dictionnaire avec la moyenne des couleurs pour chaque zone.
    """
    # Initialiser un dictionnaire pour stocker les couleurs des zones
    zones_couleurs = {i: [] for i in range(nb_germes)}

    rows, cols = image.shape[:2]
    # Parcourir chaque pixel de l'image
    for i in range(rows):
        for j in range(cols):
            zone = voronoi_map[i, j]  # Trouver la zone associée au pixel
            if zone != -1:  # Ignorer les pixels sans zone assignée
                zones_couleurs[zone].append(image[i, j])  # Ajouter la couleur du pixel à la zone correspondante

    # Calculer la moyenne des couleurs pour chaque zone
    moyennes = {
        zone: np.mean(couleurs, axis=0) if couleurs else [0, 0, 0]  # Moyenne des couleurs en RGB
        for zone, couleurs in zones_couleurs.items()
    }

    return moyennes  # Retourner le dictionnaire des couleurs moyennes


# Fonction pour afficher le diagramme de Voronoï avec les couleurs moyennes
def afficher_voronoi(voronoi_map, moyennes, nb_germes):
    """
    Affiche le diagramme de Voronoï coloré avec les couleurs moyennes.

    Paramètres :
        voronoi_map (numpy.ndarray) : Tableau des indices des germes assignés à chaque pixel.
        moyennes (dict) : Couleurs moyennes pour chaque zone.
    """
    rows, cols = voronoi_map.shape
    voronoi_img = np.zeros((rows, cols, 3), dtype=np.uint8)  # Image vide pour le diagramme de Voronoï coloré

    # Parcourir chaque pixel et assigner la couleur moyenne de la zone correspondante
    for i in range(rows):
        for j in range(cols):
            zone = voronoi_map[i, j]
            if zone != -1:
                voronoi_img[i, j] = moyennes[zone]

    # Afficher l'image du diagramme de Voronoï
    plt.figure(figsize=(8, 8))
    plt.imshow(voronoi_img)
    plt.title(f"Diagramme de Voronoi Discret pour {nb_germes} germes")  # Titre de l'image
    plt.axis("off")  # Désactiver l'affichage des axes
    plt.show()  # Afficher l'image


# Dimensions de l'image (500x500)
width, height = 500, 500

# Charger une image et la redimensionner
img = Image.open("image_source_chat.jpg").resize((width, height))
img_array = np.array(img)  # Convertir l'image en tableau numpy

# Dimensions de l'image
rows, cols, _ = img_array.shape
image = np.full((rows, cols), np.inf)  # Initialisation de l'image avec des distances infinies

# Nombre de germes (2000)
nb_germes = 2000

# Générer des positions de germes aléatoires dans l'image
germes = np.array([(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(nb_germes)])

# Calculer la carte de Voronoï
voronoi_map = calcul_voronoi(image, germes)

# Calculer la moyenne des couleurs pour chaque zone
moyennes = calculer_moyenne_couleurs(img_array, voronoi_map, nb_germes)

# Afficher le diagramme de Voronoï avec les couleurs moyennes calculées
afficher_voronoi(voronoi_map, moyennes, nb_germes)
