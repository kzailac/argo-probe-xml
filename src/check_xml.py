#!/usr/bin/python3
import argparse
import sys

from argo_probe_xml.exceptions import XMLParseException
from argo_probe_xml.nagios import Nagios
from argo_probe_xml.xml import XML


def main():
    parser = argparse.ArgumentParser(
        "Probe that checks the value of elements in given xml using XPath",
        add_help=False
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument(
        "-u", "--url", dest="url", type=str, required=True, help="url with XML"
    )
    required.add_argument(
        "-t", "--timeout", dest="timeout", type=float, required=True,
        default=30, help="timeout"
    )
    required.add_argument(
        "-x", "--xpath", dest="xpath", type=str, required=True,
        help="XPath of the required child node(s)"
    )
    optional.add_argument(
        "--ok",  dest="ok", type=str,
        help="OK value of the node with given XPath"
    )
    optional.add_argument(
        "--hard", action="store_true", dest="hard",
        help="if requested node is a list, all the elements will have to be "
             "equal to the given value to return OK; by default it is enough "
             "to have one element equal to the given value to return OK"
    )
    optional.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="Show this help message and exit"
    )

    args = parser.parse_args()
    nagios = Nagios()

    xml = XML(url=args.url, timeout=args.timeout)

    try:
        if args.ok:
            if xml.equal(xpath=args.xpath, value=args.ok, hard=args.hard):
                if args.hard:
                    nagios.ok(f"All the node(s) values equal to '{args.ok}'")

                else:
                    nagios.ok(f"There are node(s) values equal to '{args.ok}'")

            else:
                if args.hard:
                    nagios.critical(
                        f"Not all node(s) values equal to '{args.ok}'"
                    )

                else:
                    nagios.critical(
                        f"None of the node(s) values are equal to '{args.ok}'"
                    )

        else:
            node = xml.parse(xpath=args.xpath)

            if node:
                nagios.ok(f"Node with XPath '{args.xpath}' found")

            else:
                nagios.warning(
                    f"Node with XPath '{args.xpath}' found but not defined"
                )

    except XMLParseException as e:
        nagios.critical(str(e))

    print(nagios.get_msg())
    sys.exit(nagios.get_code())


if __name__ == "__main__":
    main()
