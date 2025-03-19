import os
import zipfile
import shutil

# 📌 Configuration
SOURCE_DIR = "./python"  # Dossier contenant les dépendances
OUTPUT_DIR = "./packages"  # Dossier où seront créés les sous-dossiers et ZIP
ZIP_PREFIX = "lambda_part"  # Nom des fichiers ZIP
MIN_SIZE_MB = 40  # Taille minimale d'un ZIP
MAX_SIZE_MB = 45  # Taille maximale d'un ZIP
MIN_SIZE_BYTES = MIN_SIZE_MB * 1024 * 1024
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def create_zip(folder, zip_name):
    """Créer un fichier ZIP à partir d'un dossier."""
    zip_path = os.path.join(OUTPUT_DIR, zip_name)
    shutil.make_archive(zip_path, 'zip', folder)
    size = os.path.getsize(zip_path + ".zip") / (1024 * 1024)
    print(f"✅ Créé : {zip_path}.zip ({size:.2f} MB)")

def split_and_zip():
    """Divise les fichiers en sous-dossiers et les zippe."""
    all_files = []
    
    # Récupérer tous les fichiers à zipper
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            all_files.append(os.path.join(root, file))

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    part_num = 1
    current_size = 0
    current_files = []
    current_folder = os.path.join(OUTPUT_DIR, f"part{part_num}")

    if not os.path.exists(current_folder):
        os.makedirs(current_folder)

    for file in all_files:
        file_size = os.path.getsize(file)

        # Si le fichier actuel dépasse la limite, on crée un ZIP et on passe au suivant
        if current_size + file_size > MAX_SIZE_BYTES and current_size >= MIN_SIZE_BYTES:
            create_zip(current_folder, f"{ZIP_PREFIX}{part_num}")
            part_num += 1
            current_folder = os.path.join(OUTPUT_DIR, f"part{part_num}")
            os.makedirs(current_folder)
            current_size = 0
            current_files = []

        # Déplacer le fichier dans le dossier en cours
        shutil.move(file, os.path.join(current_folder, os.path.basename(file)))
        current_size += file_size

    # Si des fichiers restent, on les zippe aussi
    if current_size > 0:
        create_zip(current_folder, f"{ZIP_PREFIX}{part_num}")

# 📌 Exécuter la fonction
split_and_zip()
