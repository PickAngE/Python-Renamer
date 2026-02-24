import os
import random
import string

MIN_LEN = 50      # Minimum length of the name
MAX_LEN = 230     # Maximum length of the name
INCLUDE_DIGITS = True  # Set to True to include digits (0-9)

def generate_random_name(length, include_digits=False):
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    return ''.join(random.choices(chars, k=length))

def rename_files():
    folder = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)
    
    target_folder = folder
    if os.name == 'nt' and not folder.startswith("\\\\?\\"):
        target_folder = "\\\\?\\" + os.path.abspath(folder)

    print(f"Starting to rename files in: {folder}")

    for filename in os.listdir(target_folder):
        old_path = os.path.join(target_folder, filename)
        
        if not os.path.isfile(old_path) or filename == script_name:
            continue
            
        ext = os.path.splitext(filename)[1]
        
        while True:
            new_name = generate_random_name(random.randint(MIN_LEN, MAX_LEN), INCLUDE_DIGITS) + ext
            new_path = os.path.join(target_folder, new_name)
            if not os.path.exists(new_path):
                break

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        except OSError as e:
            print(f"Error renaming {filename}: {e}")
    print("Finished renaming files.")

if __name__ == "__main__":
    rename_files()