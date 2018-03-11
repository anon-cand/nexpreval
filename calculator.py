import argparse
import logging
import os
import sys
import xml.etree.ElementTree as ET
from logging.config import fileConfig
from pathlib import Path

from operation import Operation
from addition import Addition
from constant import Constant
from division import Division
from multiplication import Multiplication
from subtraction import Subtraction

operations = {
    'addition': Addition,
    'subtraction': Subtraction,
    'multiplication': Multiplication,
    'division': Division
}

def ops_parser(node):
    typename = operations.setdefault(node.tag, Constant)
    obj = typename()
    if len(node) > 0:
        for sc in node:
            if len(sc) > 0:
                child = list(sc)[0]
                obj.add_operand(ops_parser(child), sc.tag)
            else:
                obj.add_operand(ops_parser(sc), sc.tag)
    else:
        obj.add_operand(node.text, node.tag)
    return obj

def file_parser(filepath):
    results = {}
    with open(filepath) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            ops = ops_parser(child)
            results[child.attrib['id']] = ops()
    return results

def convert(results):
    root = ET.Element('expressions')
    for k, v in results.items():
        item = ET.SubElement(root, 'result', {'id': k})
        item.text = str(v)
    return root

def main():
    """
    Driver function that accepts and validates user arguments
    and passes the path to individual files to the expression parser
    :returns integer indicating success or failure
    """

    # operations = {}
    # for sc in Operation.__subclasses__():
    #     operations[sc.key] = sc.__name__
    #
    # print(operations)
    # sys.exit(1)

    # Parse user arguments

    parser = argparse.ArgumentParser(description='Process a set of expression files in a directory.')
    parser.add_argument('source', help='source directory for input files')
    parser.add_argument('target', help='destination directory for output files')
    args = parser.parse_args()

    spath = Path(args.source)  # Path to source directory
    tpath = Path(args.target)  # Path to destination directory

    logger = logging.getLogger()

    # Validate arguments and log error message (if any)

    if not (spath.exists() and spath.is_dir()):
        logger.error('Given path to source directory is not valid.')
        return 1

    if not (tpath.exists() and tpath.is_dir()):
        logger.error('Given path to target directory is not valid.')
        return 1

    source = spath.resolve()
    target = tpath.resolve()

    if not (os.access(source, os.R_OK)):
        logger.error('Read permissions on source directory is missing.')
        return 1

    if not (os.access(target, os.R_OK | os.W_OK)):
        logger.error('Read/write permissions on target directory are missing.')
        return 1

    # Process files in the source directory

    logger.info('Source path: %s', source)
    logger.info('Target path: %s', target)

    with os.scandir(source) as it:
        for entry in it:
            logger.info("Processing file: %s", entry.name)
            results = file_parser(entry.path)
            if len(results) > 0:
                result_xml = convert(results)
                ET.dump(result_xml)


if __name__ == '__main__':
    fileConfig('logging.ini')
    main()
