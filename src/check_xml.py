#!/usr/bin/python3
import argparse
import sys
import textwrap

from argo_probe_xml.exceptions import XMLParseException, WarningException, \
    CriticalException, TechnicalException
from argo_probe_xml.nagios import Nagios
from argo_probe_xml.xml import XML

NOTE = """
notes:
  The format for the warning and critical range is as follows:
  10 - raises alert when value is outside of [0, 10] range
  10: - raises alert when value is outside of [10, Inf] range
  10:20 - raises alert when value is outside of [10, 20] range
""" + "  @10:20 - negation of the above, i.e. raises alert when value is " \
      "inside of [10, 20] range"


USAGE = """
  Probe that checks the value of elements in given XML using XPath
    -u URL -t TIMEOUT -x XPATH [--ok OK | [[-w WARNING] [-c CRITICAL]]] [-h]
"""


def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        usage=USAGE,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(NOTE)
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument(
        "-u", "--url", dest="url", type=str, required=True,
        help="The URL that holds the XML we wish to test"
    )
    required.add_argument(
        "-t", "--timeout", dest="timeout", type=float, required=True,
        default=30, help="Seconds before the connection times out (default 30)"
    )
    required.add_argument(
        "-x", "--xpath", dest="xpath", type=str, required=True,
        help="XPath of the required child node(s)"
    )
    optional.add_argument(
        "--ok",  dest="ok", type=str,
        help="Value to result in OK status; each other value will result in "
             "CRITICAL; must not be used with -w or -c"
    )
    optional.add_argument(
        "-w", "--warning", type=str, dest="warning",
        help="Warning range; if the inspected value is not in the given range, "
             "the probe will result in WARNING status; "
             "must not be used with --ok"
    )
    optional.add_argument(
        "-c", "--critical", type=str, dest="critical",
        help="Critical range; if the inspected value is not in this range, "
             "the probe will result in CRITICAL status; "
             "must not be used with --ok"
    )
    optional.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="Show this help message and exit"
    )

    args = parser.parse_args()

    if args.ok and (args.warning or args.critical):
        parser.error("Arguments '--ok' and '-w' | '-c' are mutually exclusive")
        sys.exit(2)

    nagios = Nagios()

    xml = XML(url=args.url, timeout=args.timeout)

    try:
        if args.critical or args.warning:
            if args.critical:
                xml.critical(xpath=args.xpath, threshold=args.critical)

            if args.warning:
                xml.warning(xpath=args.xpath, threshold=args.warning)

        elif args.ok:
            if xml.equal(xpath=args.xpath, value=args.ok):
                nagios.ok(f"All the node(s) values equal to '{args.ok}'")

            else:
                if xml.equal(xpath=args.xpath, value=args.ok, hard=False):
                    nagios.warning(
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

    except (XMLParseException, CriticalException, TechnicalException) as e:
        nagios.critical(str(e))

    except WarningException as e:
        nagios.warning(str(e))

    print(nagios.get_msg())
    sys.exit(nagios.get_code())


if __name__ == "__main__":
    main()
