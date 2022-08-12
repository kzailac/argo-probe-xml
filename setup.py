from distutils.core import setup


NAME = "argo-probe-xml"


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author="SRCE",
    author_email="kzailac@srce.hr",
    description="ARGO probe that checks the value of elements in given XML "
                "using XPath",
    url="https://github.com/ARGOeu-Metrics/argo-probe-xml",
    package_dir={'argo_probe_xml': 'modules'},
    packages=['argo_probe_xml'],
    data_files=[('/usr/libexec/argo/probes/xml', ['src/check_xml'])]
)
