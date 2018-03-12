import xml.etree.ElementTree as ET
from itertools import chain
from itertools import islice


class XMLSpecParser:
    """
    Parser for spec files written in XML
    """
    __slots__ = 'operations'

    def __init__(self, operations):
        self.operations = operations

    def parse(self, spec: str) -> dict:
        """
        Parses the given spec in a non-blocking manner
        :param spec: path to the XML spec file
        :return: a dictionary of id -> operations
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

    def process_node(self, node_xml: str):
        """
        Parses a top-level operation node
        :param node_xml: node information as an XML string
        :return: an object representing the serialized operation
        """
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
    def serialize(results: dict, root_tag: str, elem_tag: str):
        """
        Utility method to create a result XML
        :param results: a mapping of operation id and its corresponding result
        :param root_tag: root tag in the result file
        :param elem_tag: tag for each result
        :return: xml string representing the serialized result
        """
        if len(results) > 0:
            root = ET.Element(root_tag)
            for k, v in results.items():
                item = ET.SubElement(root, elem_tag, {'id': k})
                item.text = str(v)
            return ET.tostring(root, encoding='unicode')

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