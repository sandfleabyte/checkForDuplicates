import os
import json


def load_list_of_files(json_file, folder_with_files):
    list_of_files = []
    with open(json_file, 'r') as f:
        loaded_dictionary = json.load(f)
        # in case a folder for files has been specified, check if json file was created for this folder
        if folder_with_files is not None:
            if folder_with_files != loaded_dictionary['folder_with_files']:
                raise ValueError(f"json file '{json_file}' refers to a different directory than the supplied argument for files directory '{folder_with_files}'")
        list_of_files = loaded_dictionary['list_of_files']
    print(f"Loaded list of {len(list_of_files)} files from {json_file}")
    return loaded_dictionary['folder_with_files'], list_of_files


def store_list_of_files(json_file, folder_with_files, valid_file_extensions, list_of_files):
    # store list of files
    with open(json_file, 'w') as f:
        json.dump({
            'folder_with_files': folder_with_files,
            'valid_file_extensions': valid_file_extensions,
            'list_of_files': list_of_files
        }, f)
    print(f"Storing list of {len(list_of_files)} files in {json_file}")


def get_list_of_files(directory, valid_file_extensions, category):
    """
    Collects names and attribtes of files in a directory and its sbdirectories and returns list of files.

    Args:
    directory (str):                Path of the directory
    valid_file_extensions (List):   List of file extensions to be considered
    category (str):                 Category of the files, either "existing" or "new"

    Returns:
    List: List of filenames with their relative path and fileseize is returned
    """

    # List to hold info on all files
    file_data = []
    
    # check if directory exists and is accesible
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist or is not accessible.")

    print(f"collecting {category} files")

    file_counter = 0
    valid_file_counter = 0

    # Walk the directory to gather info on files
    for root, dirs, files in os.walk(directory):
        for file in files:

            file_counter += 1

            # check file extension
            if len(valid_file_extensions)>0:
                _, file_extension = os.path.splitext(file)
                file_extension = file_extension.lstrip('.').lower()
                if not file_extension in valid_file_extensions:
                    #print(f"File {file} excluded as extension {file_extension} is not among list of valid extensions.")
                    continue

            valid_file_counter += 1

            # Get the relative path by removing the initial directory from root
            relative_path = os.path.relpath(root, directory)

            file_size = os.path.getsize(os.path.join(root, file))

            # Add the file and some attributes to the file_data structure
            file_data.append({
                "category": category,
                "name": file,
                "relative_path": relative_path,
                "size": file_size
            })

            print(f"  {valid_file_counter} files with valid extension among {file_counter} files found.", end='\r')

    print("")

    return file_data