# bAieux

Description du projet.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x : https://www.python.org/downloads/

## Installation

1. Clonez le repository :

   ```shell
   git clone https://github.com//phenakistiscope/bAieux.git
   cd bAieux
   ```
   
2. Créer et activer un environnement virutel :

Avec conda
  ```shell
  conda create -n baieux python=3.x
  conda activate baieux
   ```

Avec venv
  ```shell
  python -m baieux venv
  source venv/bin/baieux
  ```

3. Installer les dépendances :

   ```shell
   pip install -r requirements.txt
   ```

4. Exécutez le script en utilisant la ligne de commande :

   ```shell
   streamlit run display_bAIeux.py
   ```
