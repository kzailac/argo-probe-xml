class Args:
    def __init__(self, args):
        self.args = args

    def _find_arg(self, name, items):
        if items:
            if len(self.args["xpath"]) > 1:
                for item in items:
                    if item.startswith(f"{name}:"):
                        return ":".join(item.split(":")[1:])

            else:
                return items[0]

        return None

    def check_mutually_exclusive(self):
        for xpath in self.args["xpath"]:
            node_name = xpath.split("/")[-1]
            opt = {
                "ok": self._find_arg(name=node_name, items=self.args["ok"]),
                "warning": self._find_arg(
                    name=node_name, items=self.args["warning"]
                ),
                "critical": self._find_arg(
                    name=node_name, items=self.args["critical"]
                ),
                "age": self._find_arg(name=node_name, items=self.args["age"])
            }

            if (opt["ok"] and
                (opt["warning"] or opt["critical"] or opt["age"])) or \
                    (opt["ok"] and opt["age"]) or \
                    ((opt["warning"] or opt["critical"]) and opt["age"]):
                return False

        return True

    def check_validity(self):
        node_names = [item.split("/")[-1] for item in self.args["xpath"]]
        if len(node_names) > 1:
            for arg in [
                self.args["ok"], self.args["warning"], self.args["critical"],
                self.args["age"]
            ]:
                if arg:
                    for item in arg:
                        if not item.startswith(tuple(node_names)):
                            return False

        return True

    def _arg4node(self, arg, name):
        return self._find_arg(name, self.args[arg])

    def ok4node(self, name):
        return self._arg4node("ok", name)

    def warning4node(self, name):
        return self._arg4node("warning", name)

    def critical4node(self, name):
        return self._arg4node("critical", name)

    def age4node(self, name):
        return self._arg4node("age", name)
