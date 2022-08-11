import datetime
import io
import math

import requests
from argo_probe_xml.exceptions import WarningException, CriticalException
from lxml import etree
from lxml.etree import XMLSyntaxError


def get_date_now():
    return datetime.datetime.utcnow()


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
            raise CriticalException(str(e))

        else:
            return response.content

    def parse(self, xpath):
        try:
            tree = etree.parse(io.BytesIO(self._get()))

            elements = tree.xpath(xpath)

            if len(elements) == 0:
                raise CriticalException(
                    f"Unable to find element with XPath {xpath}"
                )

            elif len(elements) == 1:
                return elements[0].text

            else:
                return [item.text for item in elements]

        except XMLSyntaxError as e:
            raise CriticalException(f"Unable to parse xml: {str(e)}")

    def equal(self, xpath, value, hard=True):
        node = self.parse(xpath=xpath)

        if isinstance(node, list):
            equal = [item == value for item in node]

            if False not in equal:
                return True

            else:
                if True in equal:
                    raise WarningException(
                        f"Not all nodes' values equal to '{value}'"
                    )

                else:
                    raise CriticalException(
                        f"None of the nodes' values equal to '{value}'"
                    )

        else:
            equal = node == value

            if equal:
                return True

            else:
                raise CriticalException(f"Node value not equal to '{value}'")

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
            raise CriticalException(f"Invalid format of {analysis} threshold")

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
            raise CriticalException("Node values are not numbers")

    def warning(self, xpath, threshold):
        return self._validate_thresholds(
            xpath=xpath, threshold=threshold, warning=True
        )

    def critical(self, xpath, threshold):
        return self._validate_thresholds(xpath=xpath, threshold=threshold)

    def check_if_younger(self, xpath, age, time_format):
        def calculate_timedelta(item):
            now = get_date_now()

            if time_format == "UNIX":
                dt = now - datetime.datetime.utcfromtimestamp(int(item))

            else:
                dt = now - datetime.datetime.strptime(item, time_format)

            return dt.seconds / 3600.

        node = self.parse(xpath=xpath)

        if isinstance(node, list):
            younger = [calculate_timedelta(item) < age for item in node]

            if False not in younger:
                return True

            else:
                if True in younger:
                    raise WarningException(
                        f"Some node(s) values are older than {age} hr"
                    )

                else:
                    raise CriticalException(
                        f"All node(s) values are older than {age} hr"
                    )

        else:
            younger = calculate_timedelta(node) < age

            if younger:
                return True

            else:
                raise CriticalException(f"Value older than {age} hr")
