import io
import math

import requests
from argo_probe_xml.exceptions import XMLParseException, RequestException, \
    WarningException, CriticalException, TechnicalException
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

    def equal(self, xpath, value, hard=True):
        node = self.parse(xpath=xpath)

        if isinstance(node, list):
            if hard:
                return False not in [item == value for item in node]

            else:
                return True in [item == value for item in node]

        else:
            return node == value

    def _validate_thresholds(self, xpath, threshold, warning=False):
        negate = False
        location = "outside"
        analysis = "critical"

        if warning:
            analysis = "warning"

        try:
            if threshold.startswith("@"):
                negate = True
                location = "inside"
                threshold = threshold.strip("@")

            if ":" not in threshold:
                lower = 0
                upper = float(threshold)
                rng = f"[0, {upper}]"

            else:
                if threshold.startswith(":"):
                    lower = -math.inf
                    upper = float(threshold.strip(":"))
                    rng = f"[-Inf, {upper}]"

                elif threshold.endswith(":"):
                    lower = float(threshold.strip(":"))
                    upper = math.inf
                    rng = f"[{lower}, Inf]"

                else:
                    limits = threshold.split(":")
                    lower = float(limits[0].strip())
                    upper = float(limits[1].strip())
                    rng = f"[{lower}, {upper}]"

        except ValueError:
            raise TechnicalException(f"Invalid format of {analysis} threshold")

        node = self.parse(xpath=xpath)

        try:
            if isinstance(node, list):
                if negate:
                    validation = [
                        not lower <= float(item) <= upper for item in node
                    ]

                else:
                    validation = [
                        lower <= float(item) <= upper for item in node
                    ]

                if False in validation:
                    indices = [
                        str(i) for i, x in enumerate(validation) if not x
                    ]
                    path_elements = xpath.split("/")
                    if len(indices) > 1:
                        name = f"{path_elements[-2].capitalize()}s"
                        node_name = path_elements[-1]

                    else:
                        name = f"{path_elements[-2].capitalize()}"
                        node_name = path_elements[-1]

                    exception_msg = f"{name} {', '.join(indices)} " \
                                    f"{node_name} {location} range {rng}"
                    if warning:
                        raise WarningException(exception_msg)

                    else:
                        raise CriticalException(exception_msg)

                else:
                    return "OK"

            else:
                if negate:
                    validation = not lower <= float(node) <= upper

                else:
                    validation = lower <= float(node) <= upper

                if validation:
                    return "OK"

                else:
                    exception_msg = f"Value {location} range {rng}"
                    if warning:
                        raise WarningException(exception_msg)

                    else:
                        raise CriticalException(exception_msg)

        except ValueError:
            raise TechnicalException("Node values are not numbers")

    def warning(self, xpath, threshold):
        return self._validate_thresholds(
            xpath=xpath, threshold=threshold, warning=True
        )

    def critical(self, xpath, threshold):
        return self._validate_thresholds(xpath=xpath, threshold=threshold)
