import os
import shutil

# 📌 Configuration
SOURCE_DIR = "./python"  # Dossier contenant les dépendances
OUTPUT_DIR = "./packages"  # Dossier où seront créés les sous-dossiers et ZIP
ZIP_PREFIX = "lambda_part"  # Nom des fichiers ZIP
MIN_SIZE_MB = 100  # Taille minimale d'un ZIP (en Mo)
MAX_SIZE_MB = 110  # Taille maximale d'un ZIP (en Mo)
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

        # Vérifie si ajouter ce fichier respecte les limites de taille
        if current_size + file_size <= MAX_SIZE_BYTES:
            # Ajouter le fichier au dossier en cours
            shutil.move(file, os.path.join(current_folder, os.path.basename(file)))
            current_size += file_size
        else:
            # Si la taille actuelle est entre 100 Mo et 110 Mo, on compresse et recommence
            if current_size >= MIN_SIZE_BYTES:
                create_zip(current_folder, f"{ZIP_PREFIX}{part_num}")
                part_num += 1
                current_folder = os.path.join(OUTPUT_DIR, f"part{part_num}")
                os.makedirs(current_folder)
                current_size = 0
                shutil.move(file, os.path.join(current_folder, os.path.basename(file)))
                current_size += file_size
            else:
                # Si la taille est inférieure à 100 Mo, il faut essayer d'ajouter des fichiers
                remaining_files = all_files[all_files.index(file):]
                remaining_size = current_size

                # Ajouter des fichiers supplémentaires pour atteindre la taille minimale
                for next_file in remaining_files:
                    next_file_size = os.path.getsize(next_file)
                    if remaining_size + next_file_size <= MAX_SIZE_BYTES:
                        shutil.move(next_file, os.path.join(current_folder, os.path.basename(next_file)))
                        remaining_size += next_file_size

                # Compresser même si on n'atteint pas exactement 110 Mo
                create_zip(current_folder, f"{ZIP_PREFIX}{part_num}")
                part_num += 1
                current_folder = os.path.join(OUTPUT_DIR, f"part{part_num}")
                os.makedirs(current_folder)
                current_size = 0
                break  # sortir de la boucle après avoir compressé le dossier

    # Si des fichiers restent, on les zippe aussi
    if current_size >= MIN_SIZE_BYTES:
        create_zip(current_folder, f"{ZIP_PREFIX}{part_num}")

# 📌 Exécuter la fonction
split_and_zip()
