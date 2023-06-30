import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import json
import requests
import zipfile
import os

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download&id=" + file_id

    session = requests.Session()
    response = session.get(URL, stream=True)

    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

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

# Example usage
#url1 = 'https://drive.google.com/file/d/1t23vz8K0WY4a9OqO_C38lwmxPRHQsUgr/view?usp=share_link'
#url2 = 'https://drive.google.com/file/d/1VMbOuJOSinQ2NFZOOHKoLWVsncNS1BVM/view?usp=share_link'
destination = 'materiel'

file_id1 = "1t23vz8K0WY4a9OqO_C38lwmxPRHQsUgr"
file_id2 = "1VMbOuJOSinQ2NFZOOHKoLWVsncNS1BVM"

# Download and extract the first file
file_path1 = destination + file_id1 + '.ext'
download_file_from_google_drive(file_id1, file_path1)
unzip_file(file_path1, destination)

# Download and extract the second file
file_path2 = destination + file_id2 + '.ext'
download_file_from_google_drive(file_id2, file_path2)
unzip_file(file_path2, destination)

# Remove the extracted files
os.remove(file_path1)
os.remove(file_path2)

folder_path_1 = 'materiel/bayeux_generate_out300623'
folder_path_2 = 'materiel/bayeux_prompt300623'

# Get a list of all files in folder 1
files_folder_1 = os.listdir(folder_path_1)

# Sort the files based on their numeric part
images = sorted(files_folder_1, key=lambda x: int(x.split('_')[0]))

# Get a list of all files in folder 2
files_folder_2 = os.listdir(folder_path_2)

# Sort the files based on their numeric part
captions = sorted(files_folder_2, key=lambda x: int(x.split('_')[0]))


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
