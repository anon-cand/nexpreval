import xml.etree.ElementTree as ET
from itertools import chain
from itertools import islice


class XMLSpecParser:

    def __init__(self, operations):
        self.operations = operations

    def parse(self, spec: str) -> dict:
        """
        Parses the given spec in a non-blocking manner
        :param spec: path to the XML spec file
        :return: results as an XML string
        """
        results = {}
        with open(spec, 'rb') as file:
            parser = ET.XMLPullParser(['end'])
            for chunk in self.read_spec(file):
               for data in chunk:
                    parser.feed(data)
                    for event, element in parser.read_events():
                        if element.tag in self.operations and 'id' in element.attrib:
                            node_xml = ET.tostring(element, encoding='unicode')
                            ops = self.process_node(node_xml)
                            results[element.attrib['id']] = ops
        return results

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

    @staticmethod
    def read_spec(spec, size=1024):
        """
        Reads a given spec in 'size' chunks
        :param spec:
        :param size: chunk size (default: 1024)
        :return:
        """
        iterator = iter(spec)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))