class XMLException(Exception):
    def __init__(self, msg):
        self.msg = msg


class XMLParseException(XMLException):
    def __str__(self):
        return str(self.msg)


class RequestException(XMLException):
    def __str__(self):
        return str(self.msg)


class WarningException(XMLException):
    def __str__(self):
        return str(self.msg)


class CriticalException(XMLException):
    def __str__(self):
        return str(self.msg)
