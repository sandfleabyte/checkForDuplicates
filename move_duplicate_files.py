import os
import sys
import shutil


def safely_move_file(source_name,target_name):
    target_path = os.path.dirname(target_name)
    # Create the directories including subdirectories if it does not exist
    try:
        if not os.path.exists(target_path):
            os.makedirs(target_path)
    except Exception as e:
        print(f"Exception {e} while creating target directories for {target_path}. Aborting program.")
        sys.exit(1)

    # move the file from source to target
    try:
        shutil.move(source_name, target_name)
    except Exception as e:
        print(f"Exception {e} while moving file {source_name}. Aborting program.")
        sys.exit(1)


def move_duplicate_files(duplicate_files, folder_for_duplicates, folders_per_category, find_duplicates_among_existing):
    # List to hold files that were moved
    moved_files = []

    print(f'moving duplicate files to {folder_for_duplicates}')
    
    for file in duplicate_files:
        root_path = folders_per_category[file['category']]
        source_path = os.path.join(root_path, file['relative_path'])
        source_name = os.path.join(source_path, file['name'])
        source_name = os.path.normpath(source_name)
        target_path = os.path.join(folder_for_duplicates, file['relative_path'])
        target_name = os.path.join(target_path, file['name'])
        target_name = os.path.normpath(target_name)

        if file['category'] != "new" and not find_duplicates_among_existing:
            print(f"Inconsistency in list of files to be moved. No existing files shall be moved, but file '{file['name']}' is among existing files. Aborting program.")
            sys.exit(2)

        #safely_move_file(source_name,target_name)
        moved_files.append(file)

    print(f"  {len(moved_files)} duplicates among new files have been moved.")

    return moved_files
