import hashlib
import csv
import sys
from pathlib import Path

def calculate_sha256(file_path):
    """Calcule le hash SHA-256 d'un fichier."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def verify_checksums(csv_file="checksums.csv"):
    """Vérifie les checksums et met à jour le fichier CSV avec le statut (valide/invalide)."""
    try:
        rows = []
        all_ok = True

        # Lire le fichier CSV existant
        with open(csv_file, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames + ["statut"] if "statut" not in reader.fieldnames else reader.fieldnames

            for row in reader:
                file_name = row["filename"]
                expected_checksum = row["sha256"]
                file_path = Path(file_name)
                
                if not file_path.exists():
                    row["statut"] = "fichier introuvable"
                    print(f"❌ {file_name} : fichier introuvable.")
                    all_ok = False
                else:
                    actual_checksum = calculate_sha256(file_path)
                    if actual_checksum == expected_checksum:
                        row["statut"] = "valide"
                        print(f"✔ {file_name} : correspond.")
                    else:
                        row["statut"] = "invalide"
                        print(f"⚠ {file_name} : checksum incorrect.")
                        all_ok = False
                
                rows.append(row)

        # Réécrire le fichier CSV avec la colonne mise à jour
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        if all_ok:
            print("\n✅ Tous les fichiers sont intègres.")
        else:
            print("\n❌ Certains fichiers sont manquants ou altérés.")

    except FileNotFoundError:
        print(f"❌ Le fichier CSV {csv_file} est introuvable.")

if __name__ == "__main__":
    verify_checksums()
