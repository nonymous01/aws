import os
import shutil

# 📌 Configuration
SOURCE_DIR = "./pasck"  # Dossier contenant les sous-dossiers à traiter (main1, main2, ...)
OUTPUT_DIR = "./packages"  # Dossier où seront créés les fichiers ZIP
ZIP_PREFIX = "lambda_part"  # Nom des fichiers ZIP
MIN_SIZE_MB = 100  # Taille minimale d'un ZIP (en Mo)
MAX_SIZE_MB = 110  # Taille maximale d'un ZIP (en Mo)
MIN_SIZE_BYTES = MIN_SIZE_MB * 1024 * 1024
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def move_folder(src_folder, dest_folder):
    """Déplace un dossier et son contenu sans supprimer le dossier source."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Parcours tous les fichiers et dossiers du dossier source
    for item in os.listdir(src_folder):
        source_item = os.path.join(src_folder, item)
        destination_item = os.path.join(dest_folder, item)

        if os.path.isdir(source_item):
            # Si c'est un sous-dossier, on le déplace aussi
            shutil.move(source_item, destination_item)
        else:
            # Si c'est un fichier, on le déplace
            shutil.move(source_item, destination_item)

def create_zip(folder, zip_name):
    """Créer un fichier ZIP à partir d'un dossier."""
    zip_path = os.path.join(OUTPUT_DIR, zip_name)
    shutil.make_archive(zip_path, 'zip', folder)
    size = os.path.getsize(zip_path + ".zip") / (1024 * 1024)
    print(f"✅ Créé : {zip_path}.zip ({size:.2f} Mo)")

def check_and_move_folders():
    """Vérifie les sous-dossiers, les regroupe et les compresse si la taille est correcte."""
    all_main_folders = []

    # Récupérer tous les sous-dossiers (main1, main2, etc.)
    for root, dirs, _ in os.walk(SOURCE_DIR):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            total_size = 0

            # Calculer la taille totale du dossier
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path)

            all_main_folders.append((dir_name, dir_path, total_size))

    current_size = 0
    current_folders = []
    part_num = 1

    for dir_name, dir_path, size in all_main_folders:
        if current_size + size <= MAX_SIZE_BYTES:
            # Ajouter ce dossier à la combinaison en cours
            current_folders.append((dir_name, dir_path))
            current_size += size
        else:
            # Si la taille combinée atteint ou dépasse 100 Mo, créer un ZIP
            if MIN_SIZE_BYTES <= current_size <= MAX_SIZE_BYTES:
                # Créer un dossier temporaire pour les dossiers à compresser
                temp_folder = os.path.join(OUTPUT_DIR, f"temp_part{part_num}")
                if not os.path.exists(temp_folder):
                    os.makedirs(temp_folder)

                # Déplacer les dossiers dans le dossier temporaire
                for _, folder_path in current_folders:
                    move_folder(folder_path, temp_folder)

                # Créer un fichier ZIP avec les dossiers déplacés
                create_zip(temp_folder, f"{ZIP_PREFIX}{part_num}")

                # Nettoyer et passer à la combinaison suivante
                part_num += 1
                current_folders = [(dir_name, dir_path)]  # Démarre une nouvelle combinaison avec le dossier actuel
                current_size = size

    # Si des dossiers restent dans current_folders, les compresser aussi
    if MIN_SIZE_BYTES <= current_size <= MAX_SIZE_BYTES:
        temp_folder = os.path.join(OUTPUT_DIR, f"temp_part{part_num}")
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        for _, folder_path in current_folders:
            move_folder(folder_path, temp_folder)

        create_zip(temp_folder, f"{ZIP_PREFIX}{part_num}")

# 📌 Exécuter la fonction
check_and_move_folders()
