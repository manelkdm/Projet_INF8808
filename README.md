# INF8808 - Visualisation de données - Projet final

# Répertoire pour le projet de visualisation des observations d'OVNIS

L'application a été développée avec Dash, une librairie Python pour la création d'applications web interactives. L'application permet de visualiser de
différentes façons les observations d'OVNIS aux États-Unis entre 1969 et 2022 graçe aux jeu de données NUFORC. Les données proviennent de la
plateforme d'hébergement de données [data.world](https://data.world/timothyrenner/ufo-sightings).

### Le répertoire source (`/src`) est structuré comme suit:

```
.
├── assets                      # Contient les données brutes et traitées, ainsi que les images
├── components                  # Contient les composants de l'application (figures)
├── app.py                      # Contient le code source de l'application Dash
├── eda.py                      # Contient le code source de l'analyse exploratoire des données
├── preprocess_constants.py     # Contient les constantes utilisées pour le prétraitement des données
└── preprocess.py               # Contient le code source du prétraitement des données
```

## Configuration du répertoire :

Suivre cette procédure uniquement lors de la première configuration du répertoire.:

Exécuter la commande suivante pour vérifier la version installée de python.

    python --version                    # Regarder que la version installée est minimalement 3.11

Si python n'est pas installé, installer une version 3.11.xx à partir du lien suivant: https://www.python.org/downloads/

Une fois que python est installé, créer un environnement virtuel le nom suivant: `venv`

### Avec Linux/MacOS :

    python -m venv venv # Create a virtual environment
    source venv/bin/activate # Activate the virtual environment
    pip install -r requirements.txt # Install the required packages

### Avec Windows:

    python -m venv venv # Create a virtual environment
    .\phonia-env\Scripts\activate # Activate the virtual environment
    pip install -r requirements.txt # Install the required packages

## Pour exécuter l'application en local :

Exécuter la commande suivante pour lancer l'application Dash (à partir du répertoire `/src`):

    python app.py

Naviguer à l'adresse suivante dans un navigateur web:

    http://127.0.0.1:8050/
