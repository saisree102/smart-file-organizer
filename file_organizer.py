import os
import shutil
import hashlib
from datetime import datetime

# Ask user for folder path
folder_path = input("Enter folder path to organize: ")

# Check folder exists
if not os.path.exists(folder_path):
    print("❌ Folder not found.")
    exit()

print("📂 Scanning folder:", folder_path)

# File categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Programs": [".exe", ".msi"],
    "Archives": [".zip", ".rar"]
}

file_hashes = {}
moved_files = 0
duplicate_files = 0
total_size = 0


def get_hash(file_path):
    """Create hash for duplicate detection"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


# Scan all folders
for root, dirs, files in os.walk(folder_path):

    for file in files:

        file_path = os.path.join(root, file)

        try:
            size = os.path.getsize(file_path)
            total_size += size

            # Duplicate detection
            file_hash = get_hash(file_path)

            if file_hash in file_hashes:
                dup_folder = os.path.join(folder_path, "Duplicates")
                os.makedirs(dup_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(dup_folder, file))
                print("🔁 Duplicate moved:", file)
                duplicate_files += 1
                continue
            else:
                file_hashes[file_hash] = file

            extension = os.path.splitext(file)[1].lower()

            timestamp = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(timestamp)

            year = str(date.year)
            month = date.strftime("%B")

            moved = False

            for folder, extensions in file_types.items():

                if extension in extensions:

                    destination = os.path.join(folder_path, folder, year, month)
                    os.makedirs(destination, exist_ok=True)

                    shutil.move(file_path, os.path.join(destination, file))

                    print(f"📁 Moved {file} → {folder}/{year}/{month}")
                    moved_files += 1
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(folder_path, "Others", year, month)
                os.makedirs(other_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(other_folder, file))

                print(f"📁 Moved {file} → Others/{year}/{month}")
                moved_files += 1

        except Exception as e:
            print("⚠ Error processing:", file, "|", e)


print("\n----- SUMMARY -----")
print("Files organized:", moved_files)
print("Duplicates found:", duplicate_files)
print("Total data processed:", round(total_size/1024/1024, 2), "MB")
print("✅ Organization completed!")
