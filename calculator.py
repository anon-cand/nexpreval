import argparse
import os
import sys
import logging
from pathlib import Path
from logging.config import fileConfig
import xml.etree.ElementTree as ET

from catalog import *


def ops_parser(operations, node):
    ops_type = operations.setdefault(node.tag, operations['constant'])
    ops = ops_type()
    if len(node) > 0:
        for sc in node:
            if len(sc) > 0:
                child = list(sc)[0]
                ops.add_operand(ops_parser(operations, child), sc.tag)
            else:
                ops.add_operand(ops_parser(operations, sc), sc.tag)
    else:
        ops.add_operand(node.text, node.tag)
    return ops


def file_parser(operations, file_path):
    results = {}
    with open(file_path) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            ops = ops_parser(operations, child)
            results[child.attrib['id']] = ops.evaluate()
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

    # Parse user arguments

    parser = argparse.ArgumentParser(description='Process a set of expression files in a directory.')
    parser.add_argument('source', help='source directory for input files')
    parser.add_argument('target', help='destination directory for output files')
    args = parser.parse_args()

    source_path = Path(args.source)  # Path to source directory
    target_path = Path(args.target)  # Path to destination directory

    logger = logging.getLogger()

    # Validate arguments and log error message (if any)

    if not (source_path.exists() and source_path.is_dir()):
        logger.error('Given path to source directory is not valid.')
        return 1

    if not (target_path.exists() and target_path.is_dir()):
        logger.error('Given path to target directory is not valid.')
        return 1

    source = source_path.resolve()
    target = target_path.resolve()

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

    with os.scandir(source) as it:
        for entry in it:
            logger.info("Processing file: %s", entry.name)
            results = file_parser(operations, entry.path)
            if len(results) > 0:
                result_xml = convert(results)
                ET.dump(result_xml)


if __name__ == '__main__':
    fileConfig('logging.ini')
    main()
