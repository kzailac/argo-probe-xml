import io

from argo_probe_xml.exceptions import XMLParseException
from lxml import etree
from lxml.etree import XMLSyntaxError


class XML:
    def __init__(self, xml):
        self.xml = xml
        try:
            self.tree = etree.parse(io.BytesIO(xml))

        except XMLSyntaxError as e:
            raise XMLParseException(f"Unable to parse xml: {str(e)}")

    def parse(self, xpath):
        elements = self.tree.xpath(xpath)

        if len(elements) == 0:
            raise XMLParseException(
                f"Unable to find element with XPath {xpath}"
            )

        elif len(elements) == 1:
            return elements[0].text

        else:
            return [item.text for item in elements]

    def check_value(self, xpath, value):
        element_value = self.parse(xpath)

        if isinstance(element_value, list):
            return [item == value for item in element_value]

        else:
            return element_value == value
