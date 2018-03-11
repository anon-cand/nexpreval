import os
import sys
import argparse
from pathlib import Path

import logging
from logging.config import fileConfig

from operations import catalogue
from parsers import XMLSpecParser


def process(source: Path, target: Path, extension: str = '.xml') -> None:
    """
    Processes all expression files with given extension in source directory
    Assumes that all files with given extension are expression files
    :param source: Path to source directory
    :param target: Path to target directory
    :param extension: extension of the files to be processed (default: '.xml')
    :return: None
    """
    logger = logging.getLogger()

    logger.debug('Sourcing available operations')
    operations = catalogue()

    logger.debug('Initializing the spec parser')
    spec_parser = XMLSpecParser(operations)

    # For clarity do not use list comprehension
    entries = []
    logger.debug('Traversing the source directory')
    for root, _, names in os.walk(source):
        for name in names:
            if name.endswith(extension):
                full_path = os.path.join(root, name)
                entries.append(full_path)

    # Invoke the parser on each of the entries
    for spec in entries:
        logger.info("Processing file: %s", spec)
        result = spec_parser.parse(spec)
        logger.info("Result: \n%s", result)


def main() -> int:
    """
    Driver function that accepts and validates user arguments
    and passes the path to individual files to the expression parser
    :returns integer indicating success or failure
    """
    logger = logging.getLogger()

    logger.debug('Parsing arguments passed to the program')
    parser = argparse.ArgumentParser(description='Process a set of expression files in a directory.')
    parser.add_argument('source', help='source directory for input files')
    parser.add_argument('target', help='destination directory for output files')
    args = parser.parse_args()

    source_path = Path(args.source)  # Path to source directory
    target_path = Path(args.target)  # Path to destination directory

    logger.debug('Validating paths are valid and are directories')
    if not (source_path.exists() and source_path.is_dir()):
        logger.error('Given path to source directory is not valid.')
        return 1

    if not (target_path.exists() and target_path.is_dir()):
        logger.error('Given path to target directory is not valid.')
        return 1

    source = source_path.resolve()
    target = target_path.resolve()

    logger.debug('Checking if the directories are accessible to current user')
    if not (os.access(source, os.R_OK)):
        logger.error('Read permissions on source directory is missing.')
        return 1

    if not (os.access(target, os.R_OK | os.W_OK)):
        logger.error('Read/write permissions on target directory are missing.')
        return 1

    logger.info('Starting processing of XML files in source directory')
    logger.info('Source: %s', source)
    logger.info('Target: %s', target)
    process(source, target)

    return 0


if __name__ == '__main__':
    fileConfig('logging.ini')
    sys.exit(main())
