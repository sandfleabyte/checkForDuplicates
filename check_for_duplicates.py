# This program is licensed under the MIT License.
# See the LICENSE file for details.

import os
import argparse

from get_list_of_files import get_list_of_files
from get_list_of_files import store_list_of_files
from get_list_of_files import load_list_of_files
from find_duplicates import find_duplicates
from move_duplicate_files import move_duplicate_files


# file extensions to be considerd for comparison, should be in small caps, if empty all files are checked
valid_file_extensions = ['jpg','mp4','avi','mpg','mov']


def main():
    parser = argparse.ArgumentParser(description="Scan a single directory or compare two directories including subfolders for duplicate files and move those to an extra folder")
    parser.add_argument('--folder_new_files', type=str, required=False, help="Directory containing new files, duplicate new files will be moved to duplication folder")
    parser.add_argument('--folder_existing_files', type=str, required=False, help="Directory containing existing files")
    parser.add_argument('--json_existing_files', type=str, required=False, help="Use a json file to store and load informations of existing files. This is usefull when large folders on network drives are scanned.")
    parser.add_argument('--json_new_files', type=str, required=False, help="Use a json file to store and load informations of new files. This is usefull when large folders on network drives are scanned.")
    parser.add_argument('--folder_for_duplicates', type=str, required=False, help="Directory to which duplicate new files will be moved")
    parser.add_argument('--find_duplicates_among_existing', type=bool, default=False, help="Check for duplicate files among files in exsisting file folder")

    args = parser.parse_args()

    
    existing_files = None
    existing_files_dir = None
    new_files = None
    new_files_dir = None

    # load data from json file with information on existing files, if it is passed as an argument and existing
    if args.json_existing_files is not None and os.path.isfile(args.json_existing_files):
        existing_files_dir, existing_files = load_list_of_files(args.json_existing_files, args.folder_existing_files)

    
    # generate list of files in folder of existing files if argument is provided and nothing has been loaded from json file
    if existing_files is None and args.folder_existing_files is not None:
        existing_files_dir = args.folder_existing_files
        existing_files = get_list_of_files(args.folder_existing_files, valid_file_extensions, "existing")
        if args.json_existing_files is not None:
            store_list_of_files(args.json_existing_files, args.folder_existing_files, valid_file_extensions, existing_files)


    # load data from json file with information on new files, if it is passed as an argument and existing
    if args.json_new_files is not None and os.path.isfile(args.json_new_files):
        new_files_dir, new_files = load_list_of_files(args.json_new_files, args.folder_new_files)
        

    # generate list of new files if argument for folder with new files is provided and nothing has been loaded from json file
    if new_files is None and args.folder_new_files is not None:
        new_files_dir = args.folder_new_files
        new_files = get_list_of_files(args.folder_new_files, valid_file_extensions, "new")
        if args.json_new_files is not None:
            store_list_of_files(args.json_new_files, args.folder_new_files, valid_file_extensions, new_files)

    # if new files and existing files are collected, check for duplicates
    if existing_files is not None and (new_files is not None or args.find_duplicates_among_existing):
        duplicate_files = find_duplicates(existing_files, new_files, args.find_duplicates_among_existing)
        
    
    # if folder for duplicates is specified, move duplicate files there
    if args.folder_for_duplicates:            
        moved_files = move_duplicate_files(duplicate_files, args.folder_for_duplicates,
                                           {"new":new_files_dir, "existing":existing_files_dir}, args.find_duplicates_among_existing)


if __name__ == "__main__":
    main()