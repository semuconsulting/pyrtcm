"""
Stream method tests using actual receiver binary outputs for pyrtcm.rtcmReader 

Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCMReader, RTCMMessage
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self._raw1005 = (
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        self._raw1007 = b"\xd3\x00\x08>\xf4\xd2\x03ABC\xeapo\xc7"
        # 00111110 11110100 11010010 00000011 01000001 01000010 01000011 11101010
        self._payload1007 = self._raw1007[3:-3]

    def tearDown(self):
        pass

    def testMIXEDRTCM(
        self,
    ):  # test mixed stream of NMEA, UBX & RTCM messages TODO when fully implemented
        EXPECTED_RESULTS = (
            "<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=44440308028, DF142=1, DF001_1=0, DF026=30856712349, DF001_2=0, DF027=33666582560)>",
            "<RTCM(4072, DF002=4072, status=Not_Yet_Implemented)>",
            "<RTCM(1077, DF002=1077, status=Not_Yet_Implemented)>",
            "<RTCM(1087, DF002=1087, status=Not_Yet_Implemented)>",
            "<RTCM(1097, DF002=1097, status=Not_Yet_Implemented)>",
            "<RTCM(1127, DF002=1127, status=Not_Yet_Implemented)>",
            "<RTCM(1230, DF002=1230, status=Not_Yet_Implemented)>",
            "<RTCM(1007, DF002=1007, DF003=1234, DF029=3, DF030_01=A, DF030_02=B, DF030_03=C, DF031=234)>",
        )
        dirname = os.path.dirname(__file__)
        stream = open(os.path.join(dirname, "pygpsdata-RTCM3.log"), "rb")
        i = 0
        raw = 0
        rtr = RTCMReader(stream)
        for (raw, parsed) in rtr.iterate():
            if raw is not None:
                print(parsed)
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
        stream.close()

    def testSerialize(self):  # test serialize()
        payload = self._raw1005[3:-3]
        msg1 = RTCMReader.parse(self._raw1005)
        msg2 = RTCMMessage(payload)
        res = msg1.serialize()
        self.assertEqual(res, self._raw1005)
        res1 = msg2.serialize()
        self.assertEqual(res, self._raw1005)

    def testsetattr(self):  # test immutability
        EXPECTED_ERROR = (
            "Object is immutable. Updates to DF002 not permitted after initialisation."
        )
        with self.assertRaisesRegex(rte.RTCMMessageError, EXPECTED_ERROR):
            msg = RTCMReader.parse(self._raw1005)
            msg.DF002 = 9999

    def testrepr(self):  # test repr, check eval recreates original object
        EXPECTED_RESULT = "RTCMMessage(b'>\\xd0\\x00\\x03\\x8aX\\xd9I<\\x87/4\\x10\\x9d\\x07\\xd6\\xafH ')"
        msg1 = RTCMReader.parse(self._raw1005)
        self.assertEqual(repr(msg1), EXPECTED_RESULT)
        msg2 = eval(repr(msg1))
        self.assertEqual(str(msg1), str(msg2))

    def testpayload(self):  # test payload getter
        msg = RTCMReader.parse(self._raw1005)
        payload = self._raw1005[3:-3]
        self.assertEqual(msg.payload, payload)

    def testgroups(self):  # test message with repeating group
        EXPECTED_RESULT = "<RTCM(1007, DF002=1007, DF003=1234, DF029=3, DF030_01=A, DF030_02=B, DF030_03=C, DF031=234)>"
        msg1 = RTCMMessage(self._payload1007)
        msg2 = RTCMReader.parse(self._raw1007)
        self.assertEqual(str(msg1), EXPECTED_RESULT)
        self.assertEqual(str(msg2), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
