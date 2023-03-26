"""
Test special cases and methods 

Created on 7 Jul 2022 

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(os.path.join(ROOT, "src"))

from pyrtcm import RTCMReader, RTCMMessage
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt
from pyrtcm.rtcmhelpers import cell2prn, sat2prn, id2prnsigmap


class SpecialTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.streamMSM3 = open(os.path.join(dirname, "pygpsdata-RTCMMSM3.log"), "rb")
        self.streamRTCM3 = open(os.path.join(dirname, "pygpsdata-RTCM3.log"), "rb")

    def tearDown(self):
        self.streamMSM3.close()
        self.streamRTCM3.close()

    def testid2prnsigmap(self):  # test id2prnsigmap helper method
        idx = 0
        for ident in ["1077", "1087", "1097", "1107", "1117", "1127", "1110"]:
            res = str(id2prnsigmap(ident))
            idx += 1
        self.assertEqual(idx, 7)

    def testid2prnsigmaperr(self):  # test id2prnsigmap helper method with invalid ident
        EXPECTED_ERROR = "6666"
        with self.assertRaisesRegex(KeyError, EXPECTED_ERROR):
            res = id2prnsigmap("6666")

    def testsat2prn(self):  # test sat2prn helper method
        EXPECTED_RESULT = [
            "{1: '005', 2: '007', 3: '009', 4: '013', 5: '014', 6: '015', 7: '017', 8: '019', 9: '020', 10: '030'}",
            "{1: '003', 2: '004', 3: '005', 4: '013', 5: '014', 6: '015', 7: '023'}",
            "{1: '007', 2: '008', 3: '021', 4: '027', 5: '030'}",
            "{1: '007', 2: '009', 3: '010', 4: '020', 5: '023', 6: '028', 7: '032', 8: '037', 9: '040', 10: '043'}",
        ]

        rtr = RTCMReader(self.streamRTCM3)
        idx = 0
        for raw, parsed in rtr:
            if raw is not None:
                if parsed.identity in ["1077", "1087", "1097", "1107", "1127"]:
                    res = str(sat2prn(parsed))
                    # print(res)
                    self.assertEqual(res, EXPECTED_RESULT[idx])
                    idx += 1

    def testsat2prnerr(self):  # test sat2prn helper method with invalid message
        EXPECTED_ERROR = "Invalid RTCM3 message type - must be MSM message."
        rtr = RTCMReader(self.streamRTCM3)
        with self.assertRaisesRegex(rte.RTCMTypeError, EXPECTED_ERROR):
            for raw, parsed in rtr:
                if raw is not None:
                    if parsed.identity in ["1230"]:
                        res = str(sat2prn(parsed))

    def testcell2prn(self):  # test cell2prn helper method
        EXPECTED_RESULT = [
            "{1: ('006', '1C'), 2: ('006', '2X'), 3: ('006', '5X'), 4: ('011', '1C'), 5: ('011', '2X'), 6: ('011', '5X'), 7: ('012', '1C'), 8: ('012', '2X'), 9: ('017', '1C'), 10: ('017', '2X'), 11: ('019', '1C'), 12: ('019', '2W'), 13: ('020', '1C'), 14: ('020', '2W'), 15: ('024', '1C'), 16: ('024', '2X'), 17: ('024', '5X'), 18: ('025', '1C'), 19: ('025', '2X'), 20: ('025', '5X')}",
            "{1: ('002', '1C'), 2: ('002', '2C'), 3: ('009', '1C'), 4: ('009', '2C'), 5: ('015', '1C'), 6: ('015', '2C'), 7: ('016', '1C'), 8: ('016', '2C'), 9: ('017', '1C'), 10: ('017', '2C'), 11: ('018', '1C'), 12: ('018', '2C'), 13: ('019', '1C'), 14: ('019', '2C')}",
            "{1: ('002', '1X'), 2: ('002', '6X'), 3: ('002', '8X'), 4: ('010', '1X'), 5: ('010', '6X'), 6: ('010', '8X'), 7: ('011', '1X'), 8: ('011', '6X'), 9: ('011', '8X'), 10: ('012', '1X'), 11: ('012', '6X'), 12: ('012', '8X'), 13: ('024', '1X'), 14: ('024', '6X'), 15: ('024', '8X'), 16: ('025', '1X'), 17: ('025', '6X'), 18: ('025', '8X'), 19: ('036', '1X'), 20: ('036', '6X'), 21: ('036', '8X')}",
        ]

        rtr = RTCMReader(self.streamMSM3)
        idx = 0
        for raw, parsed in rtr:
            if raw is not None:
                if parsed.identity in ["1073", "1083", "1093", "1103", "1123"]:
                    res = str(cell2prn(parsed))
                    # print(f'"{res}",')
                    self.assertEqual(res, EXPECTED_RESULT[idx])
                    idx += 1

    def testcell2prnerr(self):  # test cell2prn helper method with invalid message
        EXPECTED_ERROR = "Invalid RTCM3 message type - must be MSM message."
        rtr = RTCMReader(self.streamRTCM3)
        with self.assertRaisesRegex(rte.RTCMTypeError, EXPECTED_ERROR):
            for raw, parsed in rtr:
                if raw is not None:
                    if parsed.identity in ["1230"]:
                        res = str(cell2prn(parsed))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
