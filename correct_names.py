from pathlib import Path

# List of dataset folders
dataset_folders = [
    "asap", "ballroom", "beatles", "candombe", "filosax", "groove_midi", 
    "gtzan", "guitarset", "hainsworth", "harmonix", "hjdb", "jaah", 
    "rwc", "simac", "smc", "tapcorrect"
]

# Files to rename
files_to_rename = [
    "_8-fold.folds",
    "_single.split",
    "_info.json"
]

# Base directory
base_dir = Path.cwd()

# for folder in dataset_folders:
#     folder_path = base_dir / folder
#     for file_suffix in files_to_rename:
#         old_file_name = folder + file_suffix
#         new_file_name = file_suffix[1:]  # Remove the leading underscore
#         old_file_path = folder_path / old_file_name
#         new_file_path = folder_path / new_file_name
        
#         if old_file_path.exists():
#             old_file_path.rename(new_file_path)
#             print(f"Renamed {old_file_path} to {new_file_path}")
#         else:
#             print(f"File {old_file_path} does not exist")

# print("Renaming completed.")

for folder in dataset_folders:
    folder_path = base_dir / folder
    old_file_name = "8-fold.folds"
    new_file_name = "8-folds.split"
    old_file_path = folder_path / old_file_name
    new_file_path = folder_path / new_file_name
    
    if old_file_path.exists():
        old_file_path.rename(new_file_path)
        print(f"Renamed {old_file_path} to {new_file_path}")
    else:
        print(f"File {old_file_path} does not exist")

print("Renaming completed.")