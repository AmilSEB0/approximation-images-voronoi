import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, ConvexHull
import alphashape
from shapely.geometry import Polygon

# Générer des points dans un anneau autour du centre (0.5, 0.5)
n = 300  # Nombre de points à générer
# Générer des angles aléatoires (uniformes) entre 0 et 2pi
theta = np.random.uniform(0, 2 * np.pi, n)
# Générer des distances aléatoires avec une distribution uniforme entre 0.25 et 0.5 (rayons de l'anneau)
r = np.sqrt(np.random.uniform(0.25**2, 0.5**2, n))
# Calculer les coordonnées x et y des points à partir de ces coordonnées polaires
x = np.column_stack((0.5 + r * np.cos(theta), 0.5 + r * np.sin(theta)))

# Affichage des points générés
plt.figure(figsize=(8, 8))
plt.scatter(x[:, 0], x[:, 1], color='blue', s=10, label='Points')  # Afficher les points sous forme de nuage de points
plt.title("Points générés")
plt.axis("equal")  # Pour que l'échelle des axes soit égale
plt.legend()  # Afficher la légende
plt.show()  # Afficher le graphique

# Calcul de l'alpha shape
alpha = 0.1  # Paramètre alpha pour l'alpha-shape (plus petit alpha = forme plus précise)
alpha_shape = alphashape.alphashape(x, alpha)  # Calcul de l'alpha shape

# Affichage de la triangulation de Delaunay et du contour convexe
plt.figure(figsize=(8, 8))

# Triangulation de Delaunay : création d'un diagramme de triangulation pour les points
delaunay = Delaunay(x)
for simplex in delaunay.simplices:  # Pour chaque triangle formé par la triangulation
    triangle_points = x[simplex]  # Extraire les points du triangle
    plt.fill(triangle_points[:, 0], triangle_points[:, 1], edgecolor='black', alpha=0.2, color='pink')  # Afficher chaque triangle

# Calcul du contour convexe des points
hull = ConvexHull(x)
for simplex in hull.simplices:  # Pour chaque côté du contour convexe
    plt.plot(x[simplex, 0], x[simplex, 1], color='green', lw=2, label='Contour Convexe' if simplex[0] == 0 else "")  # Afficher les côtés du contour convexe

# Affichage de l'alpha-shape, si elle est valide
if isinstance(alpha_shape, Polygon) and alpha_shape.is_valid:  # Vérifier que l'alpha shape est un polygone valide
    x_alpha = np.array(alpha_shape.exterior.coords)  # Extraire les coordonnées de la frontière de l'alpha-shape
    plt.plot(x_alpha[:, 0], x_alpha[:, 1], color='red', linewidth=2, label='Alpha Shape')  # Afficher l'alpha-shape en rouge

# Afficher les points à nouveau sur le graphique
plt.scatter(x[:, 0], x[:, 1], color='blue', s=10, label='Points')

# Ajouter des titres et légendes
plt.title("Alpha Shape")
plt.axis("equal")  # Pour que l'échelle des axes soit égale
plt.legend()  # Afficher la légende
plt.show()  # Afficher le graphique final
