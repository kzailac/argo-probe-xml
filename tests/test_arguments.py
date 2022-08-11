import unittest

from argo_probe_xml.arguments import Args


class ArgsTests(unittest.TestCase):
    def setUp(self):
        self.ok_args = Args(
            args={
                "xpath": ["/mock/path1", "/mock/path2", "/mock/path3"],
                "ok": ["path1:bla"],
                "warning": ["path2:10", "path3:10:20"],
                "critical": ["path2:20", "path3:20:30"],
                "age": None
            }
        )
        self.mutually_exclusive = Args(
            args={
                "xpath": ["/mock/path1", "/mock/path2", "/mock/path3"],
                "ok": ["path1:bla"],
                "warning": ["path2:10", "path3:10:20"],
                "critical": ["path2:20", "path3:20:30"],
                "age": ["path2:3"]
            }
        )
        self.no_optional_args = Args(
            args={
                "xpath": ["/mock/path1", "/mock/path2", "/mock/path3"],
                "ok": None,
                "warning": None,
                "critical": None,
                "age": None
            }
        )
        self.entries_without_node = Args(
            args={
                "xpath": ["/mock/path1", "/mock/path2", "/mock/path3"],
                "ok": ["bla"],
                "warning": ["path2:10", "path3:10:20"],
                "critical": ["path2:20", "path3:20:30"],
                "age": None
            }
        )
        self.single_xpath = Args(
            args={
                "xpath": ["/mock/path1"],
                "ok": None,
                "warning": ["10"],
                "critical": ["20"],
                "age": None
            }
        )

    def test_check_mutually_exclusive_arguments(self):
        self.assertTrue(self.ok_args.check_mutually_exclusive())
        self.assertFalse(self.mutually_exclusive.check_mutually_exclusive())
        self.assertTrue(self.no_optional_args.check_mutually_exclusive())
        self.assertTrue(self.single_xpath.check_mutually_exclusive())

    def test_validity(self):
        self.assertTrue(self.ok_args.check_validity())
        self.assertTrue(self.mutually_exclusive.check_validity())
        self.assertTrue(self.no_optional_args.check_validity())
        self.assertFalse(self.entries_without_node.check_validity())
        self.assertTrue(self.single_xpath.check_validity())

    def test_arg4node(self):
        self.assertEqual(self.ok_args.ok4node("path1"), "bla")
        self.assertEqual(self.ok_args.ok4node("path2"), None)
        self.assertEqual(self.ok_args.ok4node("path3"), None)
        self.assertEqual(self.single_xpath.ok4node("path1"), None)

        self.assertEqual(self.ok_args.warning4node("path1"), None)
        self.assertEqual(self.ok_args.warning4node("path2"), "10")
        self.assertEqual(self.ok_args.warning4node("path3"), "10:20")
        self.assertEqual(self.single_xpath.warning4node("path1"), "10")

        self.assertEqual(self.ok_args.critical4node("path1"), None)
        self.assertEqual(self.ok_args.critical4node("path2"), "20")
        self.assertEqual(self.ok_args.critical4node("path3"), "20:30")
        self.assertEqual(self.single_xpath.critical4node("path1"), "20")

        self.assertEqual(self.ok_args.age4node("path1"), None)
        self.assertEqual(self.ok_args.age4node("path2"), None)
        self.assertEqual(self.ok_args.age4node("path3"), None)
        self.assertEqual(self.single_xpath.age4node("path1"), None)
