import os
import zipfile

# 📌 Configuration
SOURCE_DIR = "./python"  # Dossier contenant les dépendances
ZIP_PREFIX = "lambda_part"  # Nom des fichiers ZIP
MAX_SIZE_MB = 45  # Taille maximale par ZIP
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # Conversion en octets

def create_zip(parts, files):
    """Crée un fichier ZIP contenant une liste de fichiers."""
    zip_name = f"{ZIP_PREFIX}{parts}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            arcname = os.path.relpath(file, SOURCE_DIR)  # Nom relatif
            zipf.write(file, arcname)
    print(f"✅ Créé : {zip_name} ({os.path.getsize(zip_name) / (1024*1024):.2f} MB)")

def split_and_zip():
    """Divise les fichiers en plusieurs ZIP de taille max 45 Mo."""
    all_files = []
    
    # Récupérer tous les fichiers à zipper
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            all_files.append(os.path.join(root, file))

    # Diviser en parties
    parts = 1
    current_size = 0
    current_files = []

    for file in all_files:
        file_size = os.path.getsize(file)
        
        # Si ajouter ce fichier dépasse la taille, on crée un ZIP et on recommence
        if current_size + file_size > MAX_SIZE_BYTES:
            create_zip(parts, current_files)
            parts += 1
            current_files = []
            current_size = 0
        
        # Ajouter le fichier à la liste
        current_files.append(file)
        current_size += file_size

    # Si des fichiers restent, créer le dernier ZIP
    if current_files:
        create_zip(parts, current_files)

# 📌 Exécuter la fonction
split_and_zip()
