import random
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def calcul_voronoi(image, germes):
    """
    Calcule le diagramme de Voronoï pour l'image donnée en fonction des positions des germes.
    
    Paramètres :
        image (numpy.ndarray) : Tableau représentant l'image (initialisé à np.inf).
        germes (list of tuples) : Liste des coordonnées des germes.
    
    Retourne :
        numpy.ndarray : Tableau représentant la carte Voronoï, assignant chaque pixel à un germe.
    """
    # Récupérer les dimensions de l'image
    rows, cols = image.shape

    # Création d'une carte Voronoï initialisée à -1 (aucun germe)
    voronoi_map = np.full((rows, cols), -1)

    # Initialisation des germes dans la carte Voronoï
    for idx, (x, y) in enumerate(germes):
        image[x, y] = 0  # La distance du germe à lui-même est 0
        voronoi_map[x, y] = idx  # L'indice du germe est assigné à sa position dans la carte Voronoï

    # Définition des masques avant (haut, gauche, diagonaux) et arrière (bas, droite, diagonaux)
    masque_avant = [(0, -1), (-1, 0), (-1, -1), (-1, 1)]
    masque_arriere = [(0, 1), (1, 0), (1, -1), (1, 1)]

    # Étape avant : Parcours de l'image de haut-gauche à bas-droit
    for i in range(1, rows):
        for j in range(1, cols):
            min_distance = image[i, j]  # Initialisation de la distance minimale
            closest_seed = voronoi_map[i, j]  # Initialisation du germe associé
            # Vérification des voisins dans la direction "avant" (haut et gauche)
            for dx, dy in masque_avant:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    if image[x, y] + 1 < min_distance:  # Mise à jour de la distance et du germe le plus proche
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]
            image[i, j] = min_distance  # Mettre à jour la distance pour le pixel
            voronoi_map[i, j] = closest_seed  # Mettre à jour le germe associé au pixel

    # Étape arrière : Parcours de l'image de bas-droit à haut-gauche
    for i in range(rows - 2, -1, -1):
        for j in range(cols - 2, -1, -1):
            min_distance = image[i, j]  # Initialisation de la distance minimale
            closest_seed = voronoi_map[i, j]  # Initialisation du germe associé
            # Vérification des voisins dans la direction "arrière" (bas et droite)
            for dx, dy in masque_arriere:
                x, y = i + dx, j + dy
                if 0 <= x < rows and 0 <= y < cols:
                    if image[x, y] + 1 < min_distance:  # Mise à jour de la distance et du germe le plus proche
                        min_distance = image[x, y] + 1
                        closest_seed = voronoi_map[x, y]
            image[i, j] = min_distance  # Mettre à jour la distance pour le pixel
            voronoi_map[i, j] = closest_seed  # Mettre à jour le germe associé au pixel

    return voronoi_map  # Retourner la carte de Voronoï


def calculer_moyenne_couleurs(image, voronoi_map, nb_germes):
    """
    Calcule la couleur moyenne pour chaque zone du diagramme de Voronoï.
    
    Paramètres :
        image (numpy.ndarray) : Tableau représentant l'image.
        voronoi_map (numpy.ndarray) : Tableau représentant la carte Voronoï.
        nb_germes (int) : Nombre de germes (zones).
    
    Retourne :
        dict : Dictionnaire avec la couleur moyenne de chaque zone.
    """
    # Initialisation d'un dictionnaire pour stocker les couleurs par zone
    zones_couleurs = {i: [] for i in range(nb_germes)}
    rows, cols = image.shape[:2]

    # Parcours de chaque pixel de l'image et ajout de sa couleur à la zone correspondante
    for i in range(rows):
        for j in range(cols):
            zone = voronoi_map[i, j]
            if zone != -1 and zone < nb_germes:  # Ignorer les pixels non affectés
                zones_couleurs[zone].append(image[i, j])

    # Calcul de la couleur moyenne pour chaque zone
    moyennes = {
        zone: np.mean(couleurs, axis=0) if couleurs else [0, 0, 0]
        for zone, couleurs in zones_couleurs.items()
    }

    return moyennes  # Retourner les couleurs moyennes pour chaque zone


def trouver_zones_non_homogenees(image, voronoi_map, moyennes, seuil=20):
    """
    Identifie les zones non homogènes dans l'image en fonction de l'écart type des pixels dans chaque zone.
    
    Paramètres :
        image (numpy.ndarray) : Tableau représentant l'image.
        voronoi_map (numpy.ndarray) : Tableau représentant la carte Voronoï.
        moyennes (dict) : Dictionnaire des couleurs moyennes de chaque zone.
        seuil (int) : Seuil de tolérance pour détecter une zone non homogène.
    
    Retourne :
        list : Liste des zones non homogènes (zones dont l'écart type moyen dépasse le seuil).
    """
    rows, cols = image.shape[:2]
    zones_non_homogenees = []

    # Parcours des zones pour vérifier l'homogénéité
    for zone, moyenne in moyennes.items():
        pixels = [
            image[i, j]
            for i in range(rows)
            for j in range(cols)
            if voronoi_map[i, j] == zone
        ]
        if pixels:
            pixels = np.array(pixels)
            ecart_type = np.std(pixels, axis=0)  # Calcul de l'écart type des couleurs
            ecart_type_moyen = np.mean(ecart_type)  # Moyenne de l'écart type
            if ecart_type_moyen > seuil:  # Si l'écart type moyen dépasse le seuil, la zone est considérée non homogène
                zones_non_homogenees.append(zone)

    return zones_non_homogenees  # Retourner les zones non homogènes


def afficher_voronoi(voronoi_map, moyennes):
    """
    Affiche le diagramme de Voronoï avec les couleurs moyennes calculées pour chaque zone.
    
    Paramètres :
        voronoi_map (numpy.ndarray) : Tableau des indices des germes assignés à chaque pixel.
        moyennes (dict) : Dictionnaire des couleurs moyennes pour chaque zone.
    """
    rows, cols = voronoi_map.shape
    voronoi_img = np.zeros((rows, cols, 3), dtype=np.uint8)  # Image pour afficher le Voronoï avec couleurs moyennes

    # Affecter la couleur moyenne à chaque pixel de l'image Voronoï
    for i in range(rows):
        for j in range(cols):
            zone = voronoi_map[i, j]
            if zone != -1:
                voronoi_img[i, j] = moyennes[zone]

    nb_germes = len(set(voronoi_map.flatten())) - 1  # Nombre de germes

    # Créer une palette de couleurs pour chaque germe
    cmap = ListedColormap(plt.cm.get_cmap('tab20').colors[:nb_germes])

    # Créer une figure avec deux sous-graphes côte à côte
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))  # 1 ligne, 2 colonnes

    # Affichage du diagramme de Voronoï discret (avec indices des germes)
    ax[0].imshow(voronoi_map, cmap=cmap, interpolation='nearest')
    ax[0].set_title("Diagramme de Voronoï Discret avec les germes")
    ax[0].axis("off")

    # Afficher les positions des germes en rouge sur l'image (dans la première figure)
    for idx, (x, y) in enumerate(germes):
        ax[0].scatter(y, x, color='red', edgecolor='black', s=100, label=f"Germe {idx}")  # Marquer les germes

    # Affichage du diagramme de Voronoï avec couleurs moyennes
    ax[1].imshow(voronoi_img)
    ax[1].set_title("Diagramme de Voronoï avec Couleurs Moyennes")
    ax[1].axis("off")

    # Ajustement des espacements pour ne pas chevaucher les images
    plt.tight_layout()  
    plt.show()


def ajouter_germes_tant_qu_il_y_a_des_zones_non_homogenees(image, voronoi_map, germes, seuil=20):
    """
    Ajoute de nouveaux germes dans les zones non homogènes tant qu'il y en a.
    
    Paramètres :
        image (numpy.ndarray) : Tableau représentant l'image.
        voronoi_map (numpy.ndarray) : Tableau représentant la carte Voronoï.
        germes (list of tuples) : Liste des coordonnées des germes.
        seuil (int) : Seuil pour identifier les zones non homogènes.
    
    Retourne :
        list, numpy.ndarray, dict : La liste mise à jour des germes, la carte Voronoï mise à jour et les couleurs moyennes.
    """
    iteration = 0
    nouveaux_germes = list(germes)
    while True:
        print(f"\nItération {iteration}: Calcul du diagramme Voronoï...")
        image_voronoi = np.full(image.shape[:2], np.inf)
        voronoi_map = calcul_voronoi(image_voronoi, nouveaux_germes)

        # Calcul des moyennes de couleurs pour chaque zone
        moyennes = calculer_moyenne_couleurs(image, voronoi_map, len(nouveaux_germes))

        # Identification des zones non homogènes
        zones_non_homogenees = trouver_zones_non_homogenees(image, voronoi_map, moyennes, seuil)

        print(f"Zones non homogènes restantes : {len(zones_non_homogenees)}")
        if not zones_non_homogenees:
            break

        # Ajout de nouveaux germes dans les zones non homogènes
        for zone in zones_non_homogenees:
            pixels_zone = [
                (i, j)
                for i in range(image.shape[0])
                for j in range(image.shape[1])
                if voronoi_map[i, j] == zone
            ]
            nb_germes_ajoutes = max(1, int(len(pixels_zone) * 0.1))
            nouveaux_germes_zone = np.random.choice(len(pixels_zone), nb_germes_ajoutes, replace=False)
            for idx in nouveaux_germes_zone:
                nouveaux_germes.append(pixels_zone[idx])

        iteration += 1

    return nouveaux_germes, voronoi_map, moyennes


# Chargement de l'image et redimensionnement
width, height = 500, 500
img = Image.open("image_source_chat.jpg").resize((width, height))
img_array = np.array(img)

# Définition du nombre de germes en fonction de la taille de l'image
nb_germes = int(0.002 * (width * height))
print(nb_germes)

# Génération des positions aléatoires des germes
germes = np.array([(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(nb_germes)])

# Initialisation de la carte Voronoï et calcul des germes
voronoi_map = np.full(img_array.shape[:2], np.inf)
germes, voronoi_map, moyennes = ajouter_germes_tant_qu_il_y_a_des_zones_non_homogenees(
    img_array, voronoi_map, germes, seuil=20
)

# Affichage du diagramme de Voronoï
afficher_voronoi(voronoi_map, moyennes)
