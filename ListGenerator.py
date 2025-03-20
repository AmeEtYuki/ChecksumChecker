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

def generate_checksums(file_list, output_csv="checksums.csv"):
    """Calcule les checksums et les stocke dans un CSV."""
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "sha256"])
        
        for file in file_list:
            file_path = Path(file)
            checksum = calculate_sha256(file_path)
            if checksum:
                writer.writerow([file_path.name, checksum])
                print(f"✔ {file_path.name} → {checksum}")
            else:
                print(f"❌ {file_path.name} introuvable.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilisation : python3 generate_sha256.py fichier1 fichier2 ...")
        sys.exit(1)
    
    generate_checksums(sys.argv[1:])
