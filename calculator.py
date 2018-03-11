import argparse
import os
import sys
from pathlib import Path

import logging
from logging.config import fileConfig

from operations import *
from evaluators import XMLFileEvaluator


def main():
    """
    Driver function that accepts and validates user arguments
    and passes the path to individual files to the expression parser
    :returns integer indicating success or failure
    """
    logger = logging.getLogger()

    # Parse user arguments
    parser = argparse.ArgumentParser(description='Process a set of expression files in a directory.')
    parser.add_argument('source', help='source directory for input files')
    parser.add_argument('target', help='destination directory for output files')
    args = parser.parse_args()

    source_path = Path(args.source)  # Path to source directory
    target_path = Path(args.target)  # Path to destination directory

    # Validate arguments and log error message (if any)
    if not (source_path.exists() and source_path.is_dir()):
        logger.error('Given path to source directory is not valid.')
        return 1

    if not (target_path.exists() and target_path.is_dir()):
        logger.error('Given path to target directory is not valid.')
        return 1

    source = source_path.resolve()
    target = target_path.resolve()

    # Check if directories are accessible
    if not (os.access(source, os.R_OK)):
        logger.error('Read permissions on source directory is missing.')
        return 1

    if not (os.access(target, os.R_OK | os.W_OK)):
        logger.error('Read/write permissions on target directory are missing.')
        return 1

    # Process files in the source directory
    logger.info('Source path: %s', source)
    logger.info('Target path: %s', target)

    # Import all the operations available
    operations = {sc.TAG: sc for sc in Operation.__subclasses__()}
    evaluator = XMLFileEvaluator(operations)

    # Start processing
    with os.scandir(source) as it:
        for entry in it:
            logger.info("Processing file: %s", entry.name)
            result = evaluator.process(entry.path)
            logger.info("Result: \n%s", result)

if __name__ == '__main__':
    fileConfig('logging.ini')
    main()
