import os
import sys
import xml.etree.ElementTree as ET
from functools import reduce


def main():
    operators = {
        'addition': lambda **kwargs: reduce(lambda x, y: x + y, kwargs['item']),
        'subtraction': lambda **kwargs: kwargs['minuend'].pop() - kwargs['subtrahend'].pop(),
        'multiplication': lambda **kwargs: reduce(lambda x, y: x * y, kwargs['factor']),
        'division': lambda **kwargs: kwargs['dividend'].pop() // kwargs['divisor'].pop()
    }

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    in_path = os.path.abspath(in_dir)
    out_path = os.path.abspath(out_dir)

    results = {}
    for name in os.listdir(in_dir):
        path = os.path.join(in_path, name)
        with open(path) as file:
            tree = ET.parse(file)
            root = tree.getroot()
            for child in root:
                kwargs = {}
                for sc in child:
                    kwargs.setdefault(sc.tag, []).append(int(sc.text))
                results[child.attrib['id']] = operators[child.tag](**kwargs)

    root = ET.Element('expressions')
    for k, v in results.items():
        item = ET.SubElement(root, 'result', {'id': k})
        item.text = str(v)
    ET.dump(root)

if __name__ == '__main__':
    main()
