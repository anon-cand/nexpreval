import sys
import logging
import argparse

from logging.config import fileConfig

from calculator import ExpressionCalculator


def main():
    """
    Driver function that collects user inputs and passes it to the underlying engine
    :returns integer indicating success or failure
    """
    logger = logging.getLogger(__name__)

    logger.debug('Parsing arguments passed to the program')
    parser = argparse.ArgumentParser(description='Process a set of expression files in a directory.')
    parser.add_argument('source', help='source directory for input files')
    parser.add_argument('target', help='destination directory for output files')
    args = parser.parse_args()

    logger.info('Initializing the application engine')
    application = ExpressionCalculator(args.source, args.target, '.xml')
    logger.info('Initiating processing')
    application.process()

    return 0


if __name__ == '__main__':
    fileConfig('logging.ini')
    sys.exit(main())
