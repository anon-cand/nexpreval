import os
import sys
import xml.etree.ElementTree as ET
from functools import reduce

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

def expr_parser(filepath):
    results = {}
    with open(filepath) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            results[child.attrib['id']] = operators[child.tag](child)
    return results

def convert_to_xml(results):
    root = ET.Element('expressions')
    for k, v in results.items():
        item = ET.SubElement(root, 'result', {'id': k})
        item.text = str(v)
    return root

def main():

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    in_path = os.path.abspath(in_dir)
    out_path = os.path.abspath(out_dir)

    for name in os.listdir(in_dir):
        path = os.path.join(in_path, name)
        results = expr_parser(path)
        if len(results) > 0:
            result_xml = convert_to_xml(results)
            ET.dump(result_xml)

if __name__ == '__main__':
    main()