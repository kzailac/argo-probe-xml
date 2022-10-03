class Nagios:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self._code = self.OK
        self._msgs = []
        self._final_msg = ""
        self.statuses = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]

    def ok(self, msg):
        self._msgs.append(msg)

    def warning(self, msg):
        self._msgs.append(msg)
        if self._code not in [self.CRITICAL, self.WARNING]:
            self._code = self.WARNING

    def critical(self, msg):
        self._msgs.append(msg)
        if self._code != self.UNKNOWN:
            self._code = self.CRITICAL

    def unknown(self, msg):
        self._msgs.append(msg)
        self._code = self.UNKNOWN

    def set_final_msg(self, msg):
        self._final_msg = msg

    def get_code(self):
        return self._code

    def get_msg(self):
        if self._final_msg:
            final_msg = f"{self.statuses[self._code]} - {self._final_msg}"

        elif len(self._msgs) == 1 and not self._final_msg:
            final_msg = f"{self.statuses[self._code]} - {self._msgs[0]}"

        else:
            final_msg = self.statuses[self._code]

        if len(self._msgs) != 1:
            for msg in self._msgs:
                final_msg = f"{final_msg}\n{msg}"

        return final_msg
