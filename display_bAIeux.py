"""
# bAIeux
"""

import streamlit as st
from PIL import Image
import requests
import zipfile
import os
import shutil

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download&id=" + file_id

    session = requests.Session()
    response = session.get(URL, stream=True)

    if "confirm" in response.url:
        confirm_token = get_confirm_token(response)
        if confirm_token:
            params = {'id': file_id, 'confirm': confirm_token}
            response = session.get(URL, params=params, stream=True)

    response.headers['Content-Disposition'] = 'attachment; filename="' + destination + '"'

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def unzip_file(file_path, destination):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination)
#https://drive.google.com/file/d/1qsdc9f6YvZgZ3yAF6e47yW_rgMd-evfO/view?usp=share_link
#https://drive.google.com/file/d/1AM_-yOFjvgsPZ8PDzo6MHpuxw-QKMf3k/view?usp=share_link
destination = 'materiel'
file_id1 = "1qsdc9f6YvZgZ3yAF6e47yW_rgMd-evfO"
file_id11 = "1AM_-yOFjvgsPZ8PDzo6MHpuxw-QKMf3k"
file_id2 = "1VMbOuJOSinQ2NFZOOHKoLWVsncNS1BVM"

# Téléchargement du premier fichier
file_path1 = os.path.join(destination, file_id1 + '.zip')
download_file_from_google_drive(file_id1, file_path1)

file_path11 = os.path.join(destination, file_id11 + '.zip')
download_file_from_google_drive(file_id11, file_path11)

# Téléchargement du deuxième fichier
file_path2 = os.path.join(destination, file_id2 + '.zip')
download_file_from_google_drive(file_id2, file_path2)

# Extraction des fichiers
unzip_file(file_path1, destination)
unzip_file(file_path11, destination)
unzip_file(file_path2, destination)

# Suppression des fichiers zip
os.remove(file_path1)
os.remove(file_path11)
os.remove(file_path2)

folder_path_1 = 'materiel/bayeux_generate_out300623_'
folder_path_11 = 'materiel/bayeux_generate_out300623_2'
folder_path_2 = 'materiel/bayeux_prompt300623'

destination_folder = 'materiel/merged_images'

# Créer le dossier de destination s'il n'existe pas déjà
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Copier les fichiers du premier dossier vers le dossier de destination
for filename in os.listdir(folder_path_1):
    src = os.path.join(folder_path_1, filename)
    dst = os.path.join(destination_folder, filename)
    shutil.copy(src, dst)

# Copier les fichiers du deuxième dossier vers le dossier de destination
for filename in os.listdir(folder_path_11):
    if not filename.startswith('.'):  # Ignorer les fichiers commençant par '.'
        src = os.path.join(folder_path_11, filename)
        dst = os.path.join(destination_folder, filename)
        shutil.copy(src, dst)

# Get a list of all files in folder 1
files_folder_1 = os.listdir(destination_folder)

# Sort the files based on their numeric part
images = sorted(files_folder_1, key=lambda x: int(x.split('_')[0]))

# Get a list of all files in folder 2
files_folder_2 = os.listdir(folder_path_2)

# Sort the files based on their numeric part
captions = sorted(captions, key=lambda x: int(x.split('_')[0]) if '_' in x else float('inf'))


# Affichage des images une par une avec légende et texte
for image, caption in zip(images, captions):
    img = Image.open(os.path.join(folder_path_1, image))
    caption_path = os.path.join(folder_path_2, caption)
    
    with open(caption_path, 'r') as file:
        caption_text = file.read()
    
    st.image(img, caption=(caption_text), use_column_width=True)
    

"""
# Un projet mené par l'Université de Genève, le projet Visual Contagions et l'HEAD
Avec la participation de Béatrice Joyeux-Prunel, Bokar N'Diaye, Marie Barras, Adéalide Quenson, Camille Sierro, Guillaume Aebi et Adrien Jeanrenaud
"""
