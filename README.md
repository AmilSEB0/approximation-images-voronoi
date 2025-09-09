# Géométrie algorithmique appliquée aux images

Ce projet est un travail pratique sur les diagrammes de Voronoï et la triangulation de Delaunay, appliqués à l’approximation d’images et aux alpha-shapes.  

---

## Contenu du projet

Le dépôt contient plusieurs scripts Python correspondant aux différentes parties du cours :

- **`voronoi_discret_force_brute.py`**  
  Implémentation du diagramme de Voronoï discret par **force brute**.  
  - Distances supportées : euclidienne, Manhattan, Chebyshev.  
  - Visualisation en temps réel avec **Pygame**.  

- **`voronoi_discret_sequentiel.py`**  
  Implémentation de l’algorithme séquentiel (balayage avec masques avant et arrière) pour calculer le Voronoï discret.  
  - Affichage avec **Matplotlib**.  

- **`approximation_image_voronoi_brute.py`**  
  Approximation d’image en utilisant le diagramme de Voronoï par **force brute**.  
  - Chaque région est colorée par la moyenne des pixels de l’image source.  
  - Résultat : effet mosaïque / pixellisation artistique.  

- **`approximation_image_voronoi_adaptatif.py`**  
  Version **adaptative** de l’approximation d’image :  
  - Démarrage avec peu de germes.  
  - Ajout de nouveaux germes dans les zones non homogènes (variance > seuil).  
  - Amélioration progressive de l’approximation.  

- **`alpha_forme_delaunay.py`**  
  Calcul et visualisation d’une **alpha-shape** (forme alpha) à partir d’un nuage de points.  
  - Basé sur la **triangulation de Delaunay** (`scipy.spatial`).  
  - Utilise le module `alphashape` et `shapely` pour calculer le contour alpha.  

- **`image_source_chat.jpg`**  
  Image de test utilisée pour l’approximation Voronoï.  

- **Dossier `images/`**  
  Contient des exemples de figures générées par les différents scripts.  

---

## Installation et dépendances

Avant de lancer les scripts, il faut installer les bibliothèques nécessaires.  
Créez un environnement virtuel (optionnel mais recommandé) et installez les dépendances :

```bash
pip install -r requirements.txt
```

---

## Comment exécuter les scripts

Chaque fichier Python peut être exécuté indépendamment :

1. Diagramme de Voronoï discret – force brute
```bash
python voronoi_discret_force_brute.py
```
Choisissez le type de distance dans la console (euclidienne, Manhattan ou Chebyshev).
L’affichage se fait en temps réel avec **Pygame**.

2. Diagramme de Voronoï discret – algorithme séquentiel
```bash
python voronoi_discret_sequentiel.py
```
Affiche un diagramme coloré avec **Matplotlib**.

3. Approximation d’image – Voronoï force brute
```bash
python approximation_image_voronoi_brute.py
```
Produit une approximation mosaïque à partir de l’image source `image_source_chat.jpg`.

4. Approximation d’image – Voronoï adaptatif
```bash
python approximation_image_voronoi_adaptatif.py
```
Améliore progressivement l’approximation de l’image `image_source_chat.jpg` en ajoutant de nouveaux germes dans les zones non homogènes.

5. Alpha-shape avec triangulation de Delaunay
```bash
python alpha_forme_delaunay.py
```
Génère un nuage de points, trace la triangulation de Delaunay, le contour convexe et l’alpha-shape.

## Résultats

Les figures générées par les scripts sont enregistrées dans le dossier `images/`.  
Elles montrent notamment :
- Les diagrammes de Voronoï obtenus
- L’évolution de l’approximation d’image
- Les contours générés via alpha-shape

### Auteur

Nom : Amil SEBO  
Contact : amilsebo@gmail.com
