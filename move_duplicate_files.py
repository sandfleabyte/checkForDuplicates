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


def move_duplicate_files(duplicate_files, folder_for_duplicates, folder_with_new_files, ):
    # List to hold files that were moved
    moved_files = []

    print(f'moving duplicates of new files to {folder_for_duplicates}')
    
    for file in duplicate_files:
        source_path = os.path.join(folder_with_new_files, file['relative_path'])
        source_name = os.path.join(source_path, file['name'])
        source_name = os.path.normpath(source_name)
        target_path = os.path.join(folder_for_duplicates, file['relative_path'])
        target_name = os.path.join(target_path, file['name'])
        target_name = os.path.normpath(target_name)

        if file['category'] != "new":
            print("this should not have happened.")
            sys.exit(2)

        safely_move_file(source_name,target_name)
        moved_files.append(file)

    print(f"  {len(moved_files)} duplicates among new files have been moved.")

    return moved_files
