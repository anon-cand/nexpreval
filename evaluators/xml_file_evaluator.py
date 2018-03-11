import xml.etree.ElementTree as ET


class XMLFileEvaluator:

    def __init__(self, operations):
        self.operations = operations

    def process(self, file_path):
        result_xml = None
        with open(file_path) as file:
            results = {}
            tree = ET.parse(file)
            root = tree.getroot()
            for child in root:
                ops = self.process_node(ET.tostring(child, encoding="unicode"))
                results[child.attrib['id']] = ops.evaluate()
            if len(results) > 0:
                result_xml = self.serialize(results)
        return result_xml

    def process_node(self, nodeText):
        node = ET.fromstring(nodeText)
        ops_type = self.operations.setdefault(node.tag, self.operations['constant'])
        ops = ops_type()
        if len(node) > 0:
            for sc in node:
                if len(sc) > 0:
                    child = list(sc)[0]
                    ops.add_operand(self.process_node(ET.tostring(child, encoding="unicode")), sc.tag)
                else:
                    ops.add_operand(self.process_node(ET.tostring(sc, encoding="unicode")), sc.tag)
        else:
            ops.add_operand(node.text, node.tag)
        return ops

    def serialize(self, results):
        root = ET.Element('expressions')
        for k, v in results.items():
            item = ET.SubElement(root, 'result', {'id': k})
            item.text = str(v)
        return ET.tostring(root, encoding="unicode")