"""
Steve Nieve - A Naive Reference Recommendation Engine

Selects references at random based on hash of user query provided
Created for the Capgemini Global Dat Science Challenge IV by Tom Kochuyt

Version: 1.1, February 5th, 2018
"""


import hashlib
import os
import plac
import random
import sys


def load_model(model_file):
    """
    Load recommendation model from file

    :param model_file: string, name of model file to load

    :return: list of strings, names of reference files
    """
    file = os.path.join(os.path.dirname(__file__), model_file)
    with open(file, mode='rt', encoding='utf-8') as model:
        references = model.read().splitlines()
    return references


def output_matches(matches, single=False, verbose=False, query=None):
    """
    Output matches in expected format: one line per reference file

    :param matches: list of matched references
    :param single: boolean, prints all on single line if True
    :param verbose: boolean, prints query if True
    :param query: string, query given by user

    :return: None
    """

    # Assume standard output: one line per match, no tabs, no separators
    start_match = ''
    end_match = ''
    line_end = '\n'

    # Do we need to include query in output, then use tab at start of each match
    if verbose:
        start_match = '\t'

    # Do we need to print all on single line
    if single:
        start_match = ''
        end_match = ';'
        line_end = ''

    # Print the query and matches
    if verbose:
        print('{0}|'.format(query, ), end=line_end, file=sys.stdout)
    for match in matches:
        print('{0}{1}{2}'.format(start_match, match, end_match), end=line_end, file=sys.stdout)


@plac.annotations(
    query=("Search query", "positional", None, str),
    results=("Number of results to return, default is 10", "option", "r", int),
    single=("Provide single-line output, default is False", "flag", "s", bool),
    verbose=("Provide query in output, default is False", "flag", "v", bool))
def main(query, results=10, single=False, verbose=False):
    """
    Steve Nieve - A naive GDSC Reference Recommendation Engine
    """

    # Load model: pre-trained on list of reference files
    model = 'GDSC_trained_model.snm'
    try:
        references = load_model(model)
    except FileNotFoundError:
        print('Sorry, file {0} is not found or is not a valid model file.'.format(model))
        sys.exit(1)

    # Process query: seed random function with hash of query
    random.seed(int(hashlib.sha256(query.encode('utf-8')).hexdigest(), 16))

    # Match references: sample references randomly and output the results
    output_matches(random.sample(references, results), single, verbose, query)


if __name__ == "__main__":
    plac.call(main)
