"""
Steve Nieve - A Naive Reference Recommendation Engine

Selects references at random based on hash of user query provided
Created for the Capgemini Global Dat Science Challenge IV by Tom Kochuyt

Version: 1.0, February 5th, 2018
"""


import pathlib
import os
import plac
import sys


def get_path(base_folder=None, sub_folder=None, create=False):
    """
    Checks if given folder exists under given path.
        If create flag is True, the folder will be created if not yet existing.

    Returns a path pointing to root or folder depending on folder existence and create flag.

    Raises
        NotADirectoryError if path is empty, does not exist or is pointing to a folder.
        ValueError if folder is empty

    :param base_folder: pathlib.Path object, pointing to an existing folder
    :param sub_folder: string, name of folder to check (and possibly create)
    :param create: boolean, create folder if not existing

    :return: pathlib.Path object
    """

    # Validate base_path points to an existing folder
    if not base_folder.is_dir():
        raise NotADirectoryError

    # Validate if a sub_folder is passed
    if sub_folder is None:
        raise ValueError('sub_folder cannot be empty')

    # Create path to the sub_folder
    folder_path = base_folder / sub_folder

    # Validate if sub_folder already exists, return path if it does
    if folder_path.is_dir():
        return folder_path

    # Validate if missing sub_folder is to be created, return path to it after creating it
    if create:
        folder_path.mkdir()
        return folder_path

    # Return path to base_folder if sub_folder not found and not created
    return base_folder


def build_model(references_path):
    """
    Create a list of names of reference files found

    :param references_path: pathlib.Path object pointing to folder containing reference files

    :return: list of names
    """
    references = []
    for child in references_path.iterdir():
        if child.is_file():
            references.append(child.name)
    return references


def save_model(model_file, model_data):
    """
    Write list of references to a file

    :param model_file: string, name of model file
    :param model_data: list of string, names of reference files

    :return: None
    """
    file = os.path.join(os.path.dirname(__file__), model_file)
    with open(file, mode='wt', encoding='utf-8') as model:
        model.write('\n'.join(model_data))


@plac.annotations(folder=("Folder containing reference files", "positional", None, str))
def main(folder=None):
    """
    Steve Nieve Model Creator
    """

    # Read reference files into a list
    try:
        references = build_model(get_path(pathlib.Path(folder), "Presentations", create=False))
    except NotADirectoryError:
        print('Sorry, folder {0} is not found or is not a valid folder.'.format(folder))
        sys.exit(1)

    # Write the list to a file
    model = 'GDSC_trained_model.snm'
    save_model(model, references)


if __name__ == "__main__":
    plac.call(main)
