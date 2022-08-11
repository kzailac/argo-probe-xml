import unittest

from argo_probe_xml.nagios import Nagios


class NagiosTests(unittest.TestCase):
    def setUp(self):
        self.nagios = Nagios()

    def test_ok(self):
        self.nagios.ok("Everything is ok")
        self.nagios.ok("The other stuff is also ok")
        self.nagios.set_final_msg("All in all - ok")
        self.assertEqual(
            self.nagios.get_msg(),
            "OK - All in all - ok\nEverything is ok\nThe other stuff is also ok"
        )
        self.assertEqual(self.nagios.get_code(), 0)

    def test_ok_single_msg(self):
        self.nagios.ok("Everything is ok")
        self.assertEqual(self.nagios.get_msg(), "OK - Everything is ok")
        self.assertEqual(self.nagios.get_code(), 0)

    def test_ok_no_msg(self):
        self.assertEqual(self.nagios.get_msg(), "OK")
        self.assertEqual(self.nagios.get_code(), 0)

    def test_warning(self):
        self.nagios.warning("This is the final warning")
        self.nagios.warning("This is the final final warning")
        self.nagios.set_final_msg("You have been warned")
        self.assertEqual(
            self.nagios.get_msg(),
            "WARNING - You have been warned\nThis is the final warning\n"
            "This is the final final warning"
        )
        self.assertEqual(self.nagios.get_code(), 1)

    def test_warning_single_message(self):
        self.nagios.warning("You have been warned")
        self.assertEqual(
            self.nagios.get_msg(), "WARNING - You have been warned"
        )
        self.assertEqual(self.nagios.get_code(), 1)

    def test_critical(self):
        self.nagios.critical("Something is wrong")
        self.nagios.critical("Yet another thing is wrong")
        self.nagios.set_final_msg("I shall say this only once")
        self.assertEqual(
            self.nagios.get_msg(),
            "CRITICAL - I shall say this only once\nSomething is wrong\n"
            "Yet another thing is wrong"
        )
        self.assertEqual(self.nagios.get_code(), 2)

    def test_critical_single_msg(self):
        self.nagios.critical("I shall say this only once")
        self.assertEqual(
            self.nagios.get_msg(), "CRITICAL - I shall say this only once"
        )
        self.assertEqual(self.nagios.get_code(), 2)

    def test_unknown(self):
        self.nagios.unknown("So confused")
        self.nagios.unknown("I don't know what is happening")
        self.nagios.set_final_msg("WOW")
        self.assertEqual(
            self.nagios.get_msg(),
            "UNKNOWN - WOW\nSo confused\nI don't know what is happening"
        )
        self.assertEqual(self.nagios.get_code(), 3)

    def test_unknown_single_msg(self):
        self.nagios.unknown("So confused")
        self.assertEqual(self.nagios.get_msg(), "UNKNOWN - So confused")
        self.assertEqual(self.nagios.get_code(), 3)

    def test_mixed_ok_warning(self):
        self.nagios.ok("First thing ok")
        self.nagios.warning("Beware")
        self.nagios.ok("Third thing ok")
        self.nagios.set_final_msg("This is the final warning")
        self.assertEqual(
            self.nagios.get_msg(),
            "WARNING - This is the final warning\nFirst thing ok\nBeware\n"
            "Third thing ok"
        )
        self.assertEqual(self.nagios.get_code(), 1)

    def test_mixed_ok_critical(self):
        self.nagios.ok("First thing ok")
        self.nagios.critical("This is not good")
        self.nagios.ok("Third thing ok")
        self.nagios.set_final_msg("Everything is falling apart")
        self.assertEqual(
            self.nagios.get_msg(),
            "CRITICAL - Everything is falling apart\nFirst thing ok\n"
            "This is not good\nThird thing ok"
        )
        self.assertEqual(self.nagios.get_code(), 2)

    def test_mixed_ok_warning_critical(self):
        self.nagios.ok("First thing ok")
        self.nagios.warning("Beware")
        self.nagios.critical("Everything is falling apart")
        self.nagios.ok("Third thing ok")
        self.nagios.set_final_msg("This is not good")
        self.assertEqual(
            self.nagios.get_msg(),
            "CRITICAL - This is not good\nFirst thing ok\nBeware\n"
            "Everything is falling apart\nThird thing ok"
        )
        self.assertEqual(self.nagios.get_code(), 2)

    def test_mixed_ok_warning_critical_unknown(self):
        self.nagios.ok("First thing ok")
        self.nagios.warning("Beware")
        self.nagios.critical("Everything is falling apart")
        self.nagios.unknown("Something weird is happening")
        self.nagios.ok("Third thing ok")
        self.nagios.set_final_msg("So confused")
        self.assertEqual(
            self.nagios.get_msg(),
            "UNKNOWN - So confused\nFirst thing ok\nBeware\n"
            "Everything is falling apart\nSomething weird is happening\n"
            "Third thing ok"
        )
        self.assertEqual(self.nagios.get_code(), 3)
