import os
import openai
from config import OPENAI_API_KEY
from scraper import get_page_content, SCRAPER_LINKS
import random

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_caption(text):
    """Génère une description Instagram engageante en français avec emojis et hashtags."""
    
    prompt = f"""
    Crée une légende Instagram engageante basée sur ce texte : {text}
    
    **Format attendu :** 
    - Commence par un titre accrocheur avec emojis, par ex : "✨ Découvrez notre service de Broyage ! ✨"
    - Suivi d'un paragraphe concis et percutant qui met en avant les avantages du service ou produit (max 3 phrases).
    - Ajoute 3 à 4 puces explicatives en utilisant des emojis pour structurer le message.
    
    **À insérer obligatoirement à la fin, sans modification :**  
    📍 Adresse  
    📌 Polygroup SA  
    📍 Route de la Brasserie 8, 1963 Vétroz  

    📞 Téléphone  
    📲 +41 78 792 03 36  

    📧 Email  
    📩 info@polygroupsa.ch  

    🌍 Site internet  
    🔗 www.polygroupsa.ch  

    **Ajoute ensuite 10 hashtags pertinents en français, sous ce format :**  
    #Polygroup #NomDuService #Secteur #Valais #Suisse #Écologie #Innovation #Service #Entreprise #DéveloppementDurable  
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def get_random_content():
    """Récupère un texte et une image d'un site sélectionné au hasard."""
    random_url = random.choice(SCRAPER_LINKS)
    print(f"URL sélectionnée : {random_url}")

    text, images, selected_image = get_page_content(random_url)

    if text:
        return selected_image, text
    else:
        return None, None

if __name__ == "__main__":
    image, text = get_random_content()
    if text:
        print(f"Image sélectionnée: {image}")
        print("Légende générée:")
        print(generate_caption(text))
    else:
        print("Aucun contenu trouvé.")
