#!/usr/bin/env python
"""
Script for checking if a submission to the global data science challenge adheres to the interface specifications.
"""

__author__ = "Saad Gondal, Daniel Kuehlwein"
__version__ = "0.1"
__email__ = "saad-abdullah.gondal@capgemini.com"

import argparse
import logging
import subprocess
import sys
import os
from time import time


def get_submission_main_file(model_dir):
    """
    Checks whether GDSC_recommendation_model.py or GDSC_recommendation_model.R exists in model_dir.

    :param model_dir: The directory where to search for the files
    :return: True and the respective file name and type iff exactly one of the files is found; else False
    """
    model_dir = os.path.realpath(model_dir)
    file_name_r = "GDSC_recommendation_model.R"
    file_path_r = os.path.join(model_dir, file_name_r)
    file_name_py = "GDSC_recommendation_model.py"
    file_path_py = os.path.join(model_dir, file_name_py)

    r_exists = os.path.exists(file_path_r)
    py_exists = os.path.exists(file_path_py)

    if r_exists and py_exists:
        logging.error("Found an R and a Python model file. Not clear which one to use.")
        return False, "", ""
    if not (r_exists or py_exists):
        logging.error("Found neither an R nor a Python model file. Check the model directory %s." % model_dir)
        return False, "", ""
    if r_exists:
        logging.info("Found R model at %s" % file_path_r)
        return True, file_path_r, "Rscript"
    if py_exists:
        logging.info("Found Python model at %s" % file_path_py)
        return True, file_path_py, "python"


def main():
    """
    Main loop for model validation tests. Checks whether a model adheres to the interface specification of the
    global data science challenge. All errors are reported to the console and logged in validate_model.log

    :return: True iff no errors are found, else False.
    """
    # Set up logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # Init parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-model_dir', '--model_dir', type=str,
                        help='Directory containing GDSC_recommendation_model.* file. Use "" if name has space.')
    args = parser.parse_args()
    ret_val = True  # init return value

    # Testing submission structure
    found_main_file, main_file_path, model_type = get_submission_main_file(args.model_dir)
    if not found_main_file:
        return False

    # Test if requirements.txt exists
    if not os.path.exists(os.path.join(args.model_dir, 'requirements.txt')):
        logging.warning("Could not find requirements.txt in directory %s" % os.path.realpath(args.model_dir))

    # Load ppt list
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join('data/references.txt')) as ppt_list_file:
        ppt_list = ppt_list_file.read().splitlines()

    # Test model behaviour for different inputs
    start_time = time()
    test_query = 'SAP implementation in Germany'
    result_output = subprocess.Popen([model_type, main_file_path, test_query],
                                     stdout=subprocess.PIPE, cwd=args.model_dir).communicate()[0]
    run_time = round(time() - start_time, 2)
    result_output = result_output.decode('UTF-8')
    result_output = result_output.splitlines()

    if run_time > 2:
        logging.warning("Prediction time is %s sec. You might want to improve the recommendation speed." % run_time)

    # Models should return exactly 10 recommendations
    if len(result_output) != 10:
        ret_val = False
        logging.error("The model did not return 10 recommendations: %s recommendations" % len(result_output))

    # All recommendations should be in of the ppt_list
    for ref in result_output:
        if not (ref in ppt_list):
            logging.error("Unknown reference: %s" % ref)
            ret_val = False

    if ret_val:
        logging.info("All tests successful.")
    return ret_val


if __name__ == '__main__':
    main()
