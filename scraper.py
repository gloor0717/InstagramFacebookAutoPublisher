import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from config import SCRAPER_LINKS  # Import the list from config.py
import os

def get_page_content(url):
    try:
        # Effectuer la requête HTTP avec un User-Agent
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parser le contenu HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Essayer de trouver le conteneur principal du contenu
        main_content = soup.find(id="main-wrapper") or soup.find(id="main") or soup.find(id="theme-main")
        if not main_content:
            print("Aucun conteneur principal trouvé.")
            return None, None, None

        # Supprimer les scripts, styles et noscript
        for tag in main_content(["script", "style", "noscript"]):
            tag.decompose()

        # Extraire le texte visible dans le conteneur principal
        text = ' '.join(main_content.stripped_strings)

        # Récupérer les images, y compris celles en lazy load
        images = []
        for img in main_content.find_all("img"):
            img_url = img.get("data-src") or img.get("src")
            if img_url and not img_url.startswith("data:image"):  # Ignorer les images en Base64
                images.append(urljoin(url, img_url))

        # Sélectionner une image au hasard s'il y en a
        selected_image = random.choice(images) if images else None

        return text, images, selected_image

    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return None, None, None

def download_image(image_url, folder_path):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_path = os.path.join(folder_path, "image.jpeg")
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image téléchargée : {image_path}")
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")

# Sélectionner une URL aléatoire depuis SCRAPER_LINKS
random_url = random.choice(SCRAPER_LINKS)
print(f"URL sélectionnée : {random_url}")

# Scraper la page sélectionnée
text_content, all_images, selected_image = get_page_content(random_url)

# Affichage des résultats
if text_content:
    print("Texte récupéré :", text_content[:500], "...")  # Afficher 500 premiers caractères
    print("Toutes les images trouvées :", all_images)
    print("Image sélectionnée :", selected_image if selected_image else "Aucune image trouvée")
    if selected_image:
        # Télécharger l'image sélectionnée
        download_image(selected_image, os.path.dirname(__file__))
else:
    print("Aucun contenu récupéré.")
