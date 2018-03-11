import os
import sys
import xml.etree.ElementTree as ET
from functools import reduce

operators = \
    {
        'addition': lambda **kwargs: reduce(lambda x, y: x + y, kwargs['item']),
        'subtraction': lambda **kwargs: kwargs['minuend'].pop() - kwargs['subtrahend'].pop(),
        'multiplication': lambda **kwargs: reduce(lambda x, y: x * y, kwargs['factor']),
        'division': lambda **kwargs: kwargs['dividend'].pop() // kwargs['divisor'].pop()
    }

def expr_parser(filepath):
    results = {}
    with open(filepath) as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            if 'complex' in child.attrib and child.attrib['complex']:
                return False, results
            kwargs = {}
            for sc in child:
                kwargs.setdefault(sc.tag, []).append(int(sc.text))
            results[child.attrib['id']] = operators[child.tag](**kwargs)
    return True, results

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
        processed, results = expr_parser(path)
        if not processed:
            print("%s - This calculator does not support complex operations" % name)
            continue
        if len(results) > 0:
            result_xml = convert_to_xml(results)
            ET.dump(result_xml)

if __name__ == '__main__':
    main()


"""
Recursively iterate through the elements of the tree accumulating
a dictionary result.

:param tree: The XML element tree
:type tree: xml.etree.ElementTree
:param accum: Dictionary into which data is accumulated
:type accum: dict
:rtype: dict
"""

