import unittest

from argo_probe_xml.exceptions import XMLParseException
from argo_probe_xml.xml import XML

xml1 = b"<aris>" \
         b"<lastUpdate>1659507301</lastUpdate>" \
         b"<partition>" \
         b"<running_jobs>59</running_jobs>" \
         b"<queued_jobs>122</queued_jobs>" \
         b"<allocated_cpus>4640</allocated_cpus>" \
         b"<allocated_nodes>232</allocated_nodes>" \
         b"<free_cpus>3580</free_cpus>" \
         b"<free_nodes>179</free_nodes>" \
         b"<total_nodes>411</total_nodes>" \
         b"<total_cpus>8220</total_cpus>" \
         b"<name>compute</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>4</running_jobs>" \
         b"<queued_jobs>0</queued_jobs>" \
         b"<allocated_cpus>13</allocated_cpus>" \
         b"<allocated_nodes>3</allocated_nodes>" \
         b"<free_cpus>867</free_cpus>" \
         b"<free_nodes>41</free_nodes>" \
         b"<total_nodes>44</total_nodes>" \
         b"<total_cpus>880</total_cpus>" \
         b"<name>gpu</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>5</running_jobs>" \
         b"<queued_jobs>1</queued_jobs>" \
         b"<allocated_cpus>784</allocated_cpus>" \
         b"<allocated_nodes>20</allocated_nodes>" \
         b"<free_cpus>336</free_cpus>" \
         b"<free_nodes>10</free_nodes>" \
         b"<total_nodes>30</total_nodes>" \
         b"<total_cpus>1120</total_cpus>" \
         b"<name>fat</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>1</running_jobs>" \
         b"<queued_jobs>0</queued_jobs>" \
         b"<allocated_cpus>4</allocated_cpus>" \
         b"<allocated_nodes>1</allocated_nodes>" \
         b"<free_cpus>1196</free_cpus>" \
         b"<free_nodes>9</free_nodes>" \
         b"<total_nodes>10</total_nodes>" \
         b"<total_cpus>1200</total_cpus>" \
         b"<name>taskp</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>0</running_jobs>" \
         b"<queued_jobs>0</queued_jobs>" \
         b"<allocated_cpus>0</allocated_cpus>" \
         b"<allocated_nodes>0</allocated_nodes>" \
         b"<free_cpus>40</free_cpus>" \
         b"<free_nodes>2</free_nodes>" \
         b"<total_nodes>2</total_nodes>" \
         b"<total_cpus>40</total_cpus>" \
         b"<name>viz</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>0</running_jobs>" \
         b"<queued_jobs>0</queued_jobs>" \
         b"<allocated_cpus>0</allocated_cpus>" \
         b"<allocated_nodes>0</allocated_nodes>" \
         b"<free_cpus>360</free_cpus>" \
         b"<free_nodes>16</free_nodes>" \
         b"<total_nodes>16</total_nodes>" \
         b"<total_cpus>360</total_cpus>" \
         b"<name>short</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"<partition>" \
         b"<running_jobs>3</running_jobs>" \
         b"<queued_jobs>2</queued_jobs>" \
         b"<allocated_cpus>6</allocated_cpus>" \
         b"<allocated_nodes>1</allocated_nodes>" \
         b"<free_cpus>34</free_cpus>" \
         b"<free_nodes>0</free_nodes>" \
         b"<total_nodes>1</total_nodes>" \
         b"<total_cpus>40</total_cpus>" \
         b"<name>ml</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>" \
         b"</aris>"

xml2 = \
    b'<?xml version="1.0" encoding="UTF-8"?>' \
    b'<OAI-PMH>' \
    b'<responseDate>2002-02-08T12:00:01Z</responseDate>' \
    b'<request verb="Identify">http://memory.loc.gov/cgi-bin/oai</request>' \
    b'<Identify> ' \
    b'<repositoryName>Library of Congress Open Archive Initiative ' \
    b'Repository 1</repositoryName>' \
    b'<baseURL>http://memory.loc.gov/cgi-bin/oai</baseURL>' \
    b'<protocolVersion>2.0</protocolVersion>' \
    b'<adminEmail>somebody@loc.gov</adminEmail>' \
    b'<adminEmail>anybody@loc.gov</adminEmail>' \
    b'<earliestDatestamp>1990-02-01T12:00:00Z</earliestDatestamp>' \
    b'<deletedRecord>transient</deletedRecord>' \
    b'<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>' \
    b'<compression>deflate</compression>' \
    b'</Identify>' \
    b'</OAI-PMH>'

xml3 = b"<aris>" \
         b"<lastUpdate>1659507301</lastUpdate>" \
         b"<partition>" \
         b"<running_jobs>59</running_jobs>" \
         b"<queued_jobs>122</queued_jobs>" \
         b"<allocated_cpus>4640</allocated_cpus>" \
         b"<allocated_nodes>232</allocated_nodes>" \
         b"<free_cpus>3580</free_cpus>" \
         b"<free_nodes>179</free_nodes>" \
         b"<total_nodes>411</total_nodes>" \
         b"<total_cpus>8220</total_cpus>" \
         b"<name>compute</name>" \
         b"<state_up>up</state_up>" \
         b"</partition>"


class XMLParseTests(unittest.TestCase):
    def setUp(self):
        self.xml1 = XML(xml1)
        self.xml2 = XML(xml2)

    def test_parse(self):
        self.assertEqual(
            self.xml1.parse("/aris/partition/state_up"),
            ["up", "up", "up", "up", "up", "up", "up"]
        )
        self.assertEqual(
            self.xml2.parse("/OAI-PMH/Identify/granularity"),
            "YYYY-MM-DDThh:mm:ssZ"
        )
        self.assertEqual(
            self.xml2.parse("/OAI-PMH/Identify/adminEmail"),
            ["somebody@loc.gov", "anybody@loc.gov"]
        )

    def test_parse_if_missing_element(self):
        with self.assertRaises(XMLParseException) as context:
            self.xml1.parse("/aris/partition/nonexisting")

        self.assertEqual(
            context.exception.__str__(),
            "Unable to find element with XPath /aris/partition/nonexisting"
        )

    def test_parse_if_wrong_format(self):
        with self.assertRaises(XMLParseException) as context:
            XML(xml3)

        self.assertEqual(
            context.exception.__str__(),
            "Unable to parse xml: "
            "Premature end of data in tag aris line 1, line 1, column 223 "
            "(<string>, line 1)"
        )

    def test_check_value(self):
        self.assertEqual(
            self.xml1.check_value("/aris/partition/state_up", "up"),
            [True, True, True, True, True, True, True]
        )
        self.assertTrue(
            self.xml2.check_value(
                "/OAI-PMH/Identify/granularity", "YYYY-MM-DDThh:mm:ssZ"
            )
        )
        self.assertEqual(
            self.xml2.check_value(
                "/OAI-PMH/Identify/adminEmail", "somebody@loc.gov"
            ),
            [True, False]
        )
