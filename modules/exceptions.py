class XMLProbeException(Exception):
    def __init__(self, msg):
        self.msg = msg


class WarningException(XMLProbeException):
    def __str__(self):
        return str(self.msg)


class CriticalException(XMLProbeException):
    def __str__(self):
        return str(self.msg)
