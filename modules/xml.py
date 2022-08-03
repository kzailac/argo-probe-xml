import io

import requests
from argo_probe_xml.exceptions import XMLParseException, RequestException
from lxml import etree
from lxml.etree import XMLSyntaxError


class XML:
    def __init__(self, url, timeout=60):
        self.url = url
        self.timeout = timeout

    def _get(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects
        ) as e:
            raise RequestException(str(e))

        else:
            return response.content

    def parse(self, xpath):
        try:
            tree = etree.parse(io.BytesIO(self._get()))

            elements = tree.xpath(xpath)

            if len(elements) == 0:
                raise XMLParseException(
                    f"Unable to find element with XPath {xpath}"
                )

            elif len(elements) == 1:
                return elements[0].text

            else:
                return [item.text for item in elements]

        except XMLSyntaxError as e:
            raise XMLParseException(f"Unable to parse xml: {str(e)}")
