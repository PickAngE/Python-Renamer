import os
import random
import string

MIN_LEN = 50      # Minimum length of the name
MAX_LEN = 230     # Maximum length of the name
INCLUDE_DIGITS = True  # Set to True to include digits (0-9)

def generate_random_name(length, include_digits):
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    return ''.join(random.choices(chars, k=length))

def rename_files():
    folder = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)

    if os.name == 'nt' and not folder.startswith("\\\\?\\"):
        target_folder = "\\\\?\\" + os.path.abspath(folder)
    else:
        target_folder = folder

    print(f"Starting to rename files in: {folder}")

    used_names = set()
    files_to_rename = []

    with os.scandir(target_folder) as it:
        for entry in it:
            if entry.is_file() and entry.name != script_name:
                files_to_rename.append((entry.path, entry.name))
                used_names.add(entry.name)

    for old_path, old_name in files_to_rename:
        ext = os.path.splitext(old_name)[1]
        while True:
            base = generate_random_name(random.randint(MIN_LEN, MAX_LEN), INCLUDE_DIGITS)
            new_name = base + ext
            if new_name not in used_names:
                break
        new_path = os.path.join(target_folder, new_name)

        try:
            os.rename(old_path, new_path)
            used_names.remove(old_name)
            used_names.add(new_name)
            print(f"Renamed: {old_name} -> {new_name}")
        except OSError as e:
            print(f"Error renaming {old_name}: {e}")

    print("Finished renaming files.")

if __name__ == "__main__":
    rename_files()
