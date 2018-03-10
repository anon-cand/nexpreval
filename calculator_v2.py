import argparse
import logging
import os
import sys
import xml.etree.ElementTree as ET
from functools import reduce
from logging.config import fileConfig
from pathlib import Path


def addition(node):
    items = []
    for sc in node:
        if len(sc) > 0:
            child = list(sc)[0]
            items.append(operators[child.tag](child))
        else:
            items.append(int(sc.text))
    return sum(items)

def subtraction(node):
    minuend, subtrahend = 0, 1
    for sc in node:
        if sc.tag == 'minuend':
            if len(sc) > 0:
                child = list(sc)[0]
                minuend = operators[child.tag](child)
            else:
                minuend = int(sc.text)
        elif sc.tag == 'subtrahend':
            if len(sc) > 0:
                child = list(sc)[0]
                subtrahend = operators[child.tag](child)
            else:
                subtrahend = int(sc.text)
    return minuend - subtrahend

def multiplication(node):
    factors = []
    for sc in node:
        if len(sc) > 0:
            child = list(sc)[0]
            factors.append(operators[child.tag](child))
        else:
            factors.append(int(sc.text))
    return reduce(lambda x, y: x * y, factors)

def division(node):
    dividend, divisor = 0, 1
    for sc in node:
        if sc.tag == 'dividend':
            if len(sc) > 0:
                child = list(sc)[0]
                dividend = operators[child.tag](child)
            else:
                dividend = int(sc.text)
        elif sc.tag == 'divisor':
            if len(sc) > 0:
                child = list(sc)[0]
                divisor = operators[child.tag](child)
            else:
                divisor = int(sc.text)
    return dividend // divisor

operators = {
    'addition': addition,
    'subtraction': subtraction,
    'multiplication' : multiplication,
    'division': division
}

def parse(filepath):
    results = {}
    with open(filepath) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            results[child.attrib['id']] = operators[child.tag](child)
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

    # Use argparse to parse user arguments

    parser = argparse.ArgumentParser(description = 'Process a set of expression files in a directory.')
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

    if not (os.access(target, os.R_OK|os.W_OK)):
        logger.error('Read/write permissions on target directory are missing.')
        return 1

    # Process files in the source directory

    logger.info('Source path: %s', source)
    logger.info('Target path: %s', target)

    with os.scandir(source) as it:
        for entry in it:
            logger.info("Processing file: %s", entry.name)
            results = parse(entry.path)
            if len(results) > 0:
                result_xml = convert(results)
                ET.dump(result_xml)

if __name__ == '__main__':
    fileConfig('logging.ini')
    main()