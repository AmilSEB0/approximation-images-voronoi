import pygame
import numpy as np
import random

# Fonction de distance Euclidienne
def distance_euclidienne(p1, p2):
    return np.linalg.norm(p1 - p2)

# Fonction de distance Manhattan
def distance_manhattan(p1, p2):
    return np.sum(np.abs(p1 - p2))

# Fonction de distance Chebyshev
def distance_chebyshev(p1, p2):
    return np.max(np.abs(p1 - p2))

# Fonction pour choisir la distance
def choisir_distance():
    print("Choisissez la distance à utiliser :")
    print("1. Euclidienne")
    print("2. Manhattan")
    print("3. Chebyshev")
    choix = input("Entrez le numéro de votre choix (1/2/3): ")
    if choix == "1":
        return distance_euclidienne
    elif choix == "2":
        return distance_manhattan
    elif choix == "3":
        return distance_chebyshev
    else:
        print("Choix invalide, la distance euclidienne sera utilisée par défaut.")
        return distance_euclidienne

# Dimensions de l'image
width, height = 500, 500

# Nombre de germes
nb_germes = 5

# Générer des positions aléatoires pour les germes
germs = np.array([(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(nb_germes)])

# Générer des couleurs aléatoires pour les germes
colors = np.array([tuple(np.random.randint(0, 256, 3)) for _ in range(nb_germes)])

# Demander à l'utilisateur de choisir la distance
distance = choisir_distance()

# Initialiser Pygame
pygame.init()

# Créer une fenêtre Pygame
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Diagramme de Voronoi")

# Boucle principale pour l'affichage en temps réel
running = True
clock = pygame.time.Clock()

# Dessiner le diagramme de Voronoi en temps réel
for y in range(height):
    for x in range(width):
        # Calculer les distances aux germes
        distances = np.array([distance(np.array([x, y]), germ) for germ in germs])
        # Trouver le germe le plus proche
        closest_germ = np.argmin(distances)
        # Assigner la couleur du germe le plus proche
        color = colors[closest_germ]
        
        # Dessiner le pixel avec la couleur du germe le plus proche
        screen.set_at((x, y), color)

    # Mettre à jour l'affichage à chaque ligne (effet d'animation)
    pygame.display.update()

    # Gérer les événements Pygame (fermer la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limiter les frames par seconde pour contrôler la vitesse de l'animation
    clock.tick(60)

# Afficher les germes avec des cercles rouges
for x, y in germs:
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)

pygame.display.update()

# Attendre la fermeture de la fenêtre
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quitter Pygame
pygame.quit()