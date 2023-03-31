"""
Test special cases and methods 

Created on 7 Jul 2022 

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from collections import namedtuple

from pyrtcm import RTCMMessage, RTCMReader, RTCMTypeError
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

    def testsat2prn_synthetic(
        self,
    ):  # test sat2prn helper method with synthetic messages
        MSM = namedtuple("MSM", ["identity", "DF394", "DF395", "DF396"])
        EXPECTED_RESULTS_SAT = [
            {1: "001", 2: "003", 3: "007", 4: "063"},
            {1: "002", 2: "003", 3: "007", 4: "063"},
            {1: "003", 2: "007", 3: "063", 4: "Reserved"},
            {1: "193", 2: "195", 3: "196", 4: "199"},
            {1: "120", 2: "121", 3: "122", 4: "123", 5: "126"},
        ]
        EXPECTED_RESULTS_CELL = [
            {
                1: ("001", "1P"),
                2: ("003", "1C"),
                3: ("007", "1C"),
                4: ("007", "1P"),
                5: ("063", "1C"),
                6: ("063", "1P"),
            },
            {1: ("002", "1W"), 2: ("003", "1P"), 3: ("003", "1W")},
            {1: ("007", "2X"), 2: ("063", "2X"), 3: ("Reserved", "2X")},
            {
                1: ("193", "1C"),
                2: ("193", "1S"),
                3: ("193", "1L"),
                4: ("193", "1X"),
                5: ("195", "1C"),
                6: ("195", "1S"),
                7: ("195", "1L"),
                8: ("195", "1X"),
                9: ("196", "1C"),
                10: ("196", "1S"),
                11: ("196", "1L"),
                12: ("196", "1X"),
                13: ("199", "1C"),
                14: ("199", "1S"),
                15: ("199", "1L"),
                16: ("199", "1X"),
            },
            {
                1: ("120", "5I"),
                2: ("120", "5Q"),
                3: ("120", "5X"),
                4: ("121", "5X"),
                5: ("122", "5I"),
                6: ("122", "5X"),
                7: ("123", "1C"),
                8: ("123", "5I"),
                9: ("126", "1C"),
                10: ("126", "5Q"),
            },
        ]
        msgs = [
            MSM(
                "1077",
                0b1010001000000000000000000000000000000000000000000000000000000010,
                0b01100000000000000000000000000000,
                0b01101111,
            ),
            MSM(
                "1077",
                0b0110001000000000000000000000000000000000000000000000000000000010,
                0b00110000000000000000000000000000,
                0b01110000,
            ),
            MSM(
                "1127",
                0b0010001000000000000000000000000000000000000000000000000000000011,
                0b00010000000000000000000000000000,
                0b0111,
            ),
            MSM(
                "1117",
                0b1011001000000000000000000000000000000000000000000000000000000000,
                0b01000000000000000000000000000111,
                0b1111111111111111,
            ),
            MSM(
                "1107",
                0b1111001000000000000000000000000000000000000000000000000000000000,
                0b01000000000000000000011100000000,
                0b01110001010111001010,
            ),
        ]
        for i, msg in enumerate(msgs):
            res = sat2prn(msg)
            self.assertEqual(res, EXPECTED_RESULTS_SAT[i])
        for i, msg in enumerate(msgs):
            res = cell2prn(msg)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULTS_CELL[i])

    def testsat2prn(self):  # test sat2prn helper method
        EXPECTED_RESULT = [
            "{1: '006', 2: '011', 3: '012', 4: '017', 5: '019', 6: '020', 7: '024', 8: '025'}",
            "{1: '002', 2: '009', 3: '015', 4: '016', 5: '017', 6: '018', 7: '019'}",
            "{1: '002', 2: '010', 3: '011', 4: '012', 5: '024', 6: '025', 7: '036'}",
        ]

        rtr = RTCMReader(self.streamMSM3)
        idx = 0
        for raw, parsed in rtr:
            if raw is not None:
                if parsed.identity in ["1073", "1083", "1093", "1103", "1123"]:
                    res = str(sat2prn(parsed))
                    # print(f'"{res}",')
                    self.assertEqual(res, EXPECTED_RESULT[idx])
                    idx += 1

    def testsat2prnerr(self):  # test sat2prn helper method with invalid message
        EXPECTED_ERROR = "Invalid RTCM3 message type - must be MSM message."
        with self.assertRaisesRegex(RTCMTypeError, EXPECTED_ERROR):
            rtr = RTCMReader(self.streamRTCM3)
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
        with self.assertRaisesRegex(RTCMTypeError, EXPECTED_ERROR):
            for raw, parsed in rtr:
                if raw is not None:
                    if parsed.identity in ["1230"]:
                        res = str(cell2prn(parsed))

    def testunknown(self):  # test (synthetic) unknown messages
        EXPECTED_RESULTS = [
            "<RTCM(4062, DF002=4062, Not_Yet_Implemented)>",
            "<RTCM(999, DF002=999, Not_Yet_Implemented)>",
        ]
        PAYLOADS = [
            b"\xfd\xe1\x81\xc9\x84\x00\x08\xc2\xb8\x88\x00\x38\x80\x09\xd0\x46\x00\x28",
            b"\x3e\x71\x81\xc9\x84\x00\x08\xc2\xb8\x88\x00\x38\x80\x09\xd0\x46\x00\x28",
        ]
        for i, pay in enumerate(PAYLOADS):
            msg = RTCMMessage(payload=pay)
            self.assertEqual(str(msg), EXPECTED_RESULTS[i])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
