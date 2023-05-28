def check_attributes_for_similarity(file, file_list, duplicate_list):
    """
    Add a file to list of duplicate files if file is contained in a list of files

    Args:
    file (Dict):           File to be checked
    file_list (List):      List of files to be checked against
    duplicate_list (List): List of duplicate files in which file will be added in case of duplication
    """

    for file_in_list in file_list:
        if file_in_list['size'] == file['size']:
            if file['category'] == "new":
                duplicate_list.append(file)
                #print(f"  duplicate found: {file['name']} category: {file['category']} {file['relative_path']}")
                break


def find_duplicates(existing_files, new_files):
    """
    Compares List of new files and list of existing files and returns list of duplicate files contained in both lists

    Args:
    existing_files (List):  List of existing files
    new_files (List):       List of new files

    Returns:
    List: List of dplicate files
    """

    # Check input lists for consistency
    if type(existing_files) is not list or type(new_files) is not list:
        raise ValueError(f"The input parameter provided are not of type list.")

    # List to hold duplicate files
    duplicate_files = []
    # Dictionary to hold lists of files with same filename
    all_files = {}

    print('checking for duplicates')

    for file in existing_files+new_files:
        id = file.get("name")
        # if file with similar filename is already in dictionary, check in detail for duplication
        if all_files.get(id):
            check_attributes_for_similarity(file, all_files[id], duplicate_files)
            all_files[id].append(file)
        else:
            all_files[id] = [file]

    print(f"  {len(duplicate_files)} duplicates among new files found")

    return duplicate_files
