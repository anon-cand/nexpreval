import xml.etree.ElementTree as ET
from itertools import chain
from itertools import islice

class XMLSpecParser:

    def __init__(self, operations):
        self.operations = operations

    def parse(self, spec: str) -> str:
        with open(spec, 'rb') as file:
            parser = ET.XMLPullParser(['end'])
            for chunk in self.read_spec(file):
               for data in chunk:
                    parser.feed(data)
                    for event, element in parser.read_events():
                        if element.tag in self.operations and 'id' in element.attrib:
                            self.parse_subops(element.attrib['id'], ET.tostring(element, encoding='unicode'))
        return ''

    def parse_subops(self, ops_id, ops_spec):
        print(ops_spec)
        parser = ET.XMLPullParser(['end'])
        print("Ops Id: ", ops_id)
        for chunk in self.read_spec(ops_spec):
            for data in chunk:
                parser.feed(data)
                for event, element in parser.read_events():
                    if element.tag in self.operations and 'id' not in element.attrib:
                        if len(element) > 0:
                            sc = list(element)[0]
                            if sc.tag in self.operations:
                                self.parse_subops(ops_id, ET.tostring(sc, encoding='unicode'))
                                print('\t', ET.tostring(sc, encoding='unicode'))

    def read_spec(self, spec, size = 1024):
        iterator = iter(spec)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    def parse1(self, spec: str) -> str:
        """
        Parses the given
        :param spec: path to the XML spec file
        :return: results as an XML string
        """
        result_xml = None
        with open(spec) as file:
            results = {}
            tree = ET.parse(file)
            root = tree.getroot()
            for child in root:
                node_xml = ET.tostring(child, encoding='unicode')
                ops = self.process_node(node_xml)
                results[child.attrib['id']] = ops.evaluate()
            if len(results) > 0:
                result_xml = self.serialize(results)
        return result_xml

    def process_node(self, node_xml):
        node = ET.fromstring(node_xml)
        ops_type = self.operations.setdefault(node.tag, self.operations['default'])
        ops = ops_type()
        if len(node) > 0:
            for sc in node:
                if len(sc) > 0:
                    child = list(sc)[0]
                    ops.add_operand(self.process_node(ET.tostring(child, encoding='unicode')), sc.tag)
                else:
                    ops.add_operand(self.process_node(ET.tostring(sc, encoding='unicode')), sc.tag)
        else:
            ops.add_operand(node.text, node.tag)
        return ops

    def serialize(self, results):
        root = ET.Element('expressions')
        for k, v in results.items():
            item = ET.SubElement(root, 'result', {'id': k})
            item.text = str(v)
        return ET.tostring(root, encoding='unicode')