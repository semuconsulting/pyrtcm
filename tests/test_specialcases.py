"""
Test special cases and methods 

Created on 7 Jul 2022 

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCMReader, RTCMMessage
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt
from pyrtcm.rtcmhelpers import cell2prn, sat2prn, id2prnsigmap


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.streamRTCM3 = open(os.path.join(dirname, "pygpsdata-RTCM3.log"), "rb")

    def tearDown(self):
        self.streamRTCM3.close()
        pass

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
        for (raw, parsed) in rtr:
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
            for (raw, parsed) in rtr:
                if raw is not None:
                    if parsed.identity in ["1230"]:
                        res = str(sat2prn(parsed))

    def testcell2prn(self):  # test cell2prn helper method
        EXPECTED_RESULT = [
            "{1: ('005', '1C'), 2: ('005', '2L'), 3: ('007', '1C'), 4: ('007', '2L'), 5: ('009', '1C'), 6: ('009', '2L'), 7: ('013', '1C'), 8: ('013', None), 9: ('014', '1C'), 10: ('014', '2L'), 11: ('015', '1C'), 12: ('015', '2L'), 13: ('017', '1C'), 14: ('017', '2L'), 15: ('019', '1C'), 16: ('019', None), 17: ('020', '1C'), 18: ('020', None), 19: ('030', '1C'), 20: ('030', '2L')}",
            "{1: ('003', '1C'), 2: ('003', '2C'), 3: ('004', '1C'), 4: ('004', '2C'), 5: ('005', '1C'), 6: ('005', '2C'), 7: ('013', '1C'), 8: ('013', '2C'), 9: ('014', '1C'), 10: ('014', '2C'), 11: ('015', '1C'), 12: ('015', '2C'), 13: ('023', '1C'), 14: ('023', None)}",
            "{1: ('007', '1C'), 2: ('007', '7Q'), 3: ('008', '1C'), 4: ('008', '7Q'), 5: ('021', '1C'), 6: ('021', '7Q'), 7: ('027', '1C'), 8: ('027', '7Q'), 9: ('030', '1C'), 10: ('030', '7Q')}",
            "{1: ('007', None), 2: ('007', '7I'), 3: ('009', None), 4: ('009', '7I'), 5: ('010', '2I'), 6: ('010', '7I'), 7: ('020', '2I'), 8: ('020', None), 9: ('023', '2I'), 10: ('023', None), 11: ('028', '2I'), 12: ('028', None), 13: ('032', '2I'), 14: ('032', None), 15: ('037', '2I'), 16: ('037', None), 17: ('040', '2I'), 18: ('040', None), 19: ('043', '2I'), 20: ('043', None)}",
        ]

        rtr = RTCMReader(self.streamRTCM3)
        idx = 0
        for (raw, parsed) in rtr:
            if raw is not None:
                if parsed.identity in ["1077", "1087", "1097", "1107", "1127"]:
                    res = str(cell2prn(parsed))
                    # print(f"{idx} {parsed.identity} {res} {parsed.DF395:>032b}")
                    self.assertEqual(res, EXPECTED_RESULT[idx])
                    idx += 1

    def testcell2prnerr(self):  # test cell2prn helper method with invalid message
        EXPECTED_ERROR = "Invalid RTCM3 message type - must be MSM message."
        rtr = RTCMReader(self.streamRTCM3)
        with self.assertRaisesRegex(rte.RTCMTypeError, EXPECTED_ERROR):
            for (raw, parsed) in rtr:
                if raw is not None:
                    if parsed.identity in ["1230"]:
                        res = str(cell2prn(parsed))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
