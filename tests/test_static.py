"""
Helper, Property and Static method tests for pyrtcm.rtcmMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCMMessage, RTCMReader, RTCM_DATA_FIELDS
import pyrtcm.rtcmtypes_core as rtt
import pyrtcm.rtcmtypes_get as rtg
from pyrtcm.rtcmhelpers import (
    hextable,
    calc_crc24q,
    get_bit,
    get_bitarray,
    bits2val,
    crc2bytes,
    len2bytes,
    datasiz,
    datascale,
    datadesc,
    attsiz,
    atttyp,
    tow2utc,
    num_setbits,
)


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def testhextable(self):  # test hextable*( method)
        EXPECTED_RESULT = "000: 2447 4e47 4c4c 2c35 3332 372e 3034 3331  | b'$GNGLL,5327.0431' |\n016: 392c 532c 3030 3231 342e 3431 3339 362c  | b'9,S,00214.41396,' |\n032: 452c 3232 3332 3332 2e30 302c 412c 412a  | b'E,223232.00,A,A*' |\n048: 3638 0d0a                                | b'68\\r\\n' |\n"
        res = hextable(b"$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n", 8)
        self.assertEqual(res, EXPECTED_RESULT)

    def testcrc24q(self):  # test crc24q calculation on RTCM3 message
        msgcrc = b"\xd3\x00\x04L\xe0\x00\x80\xed\xed\xd6"  # msg with crc
        msg = msgcrc[0:-3]  # message without crc
        crc1 = calc_crc24q(msgcrc)
        crc2 = calc_crc24q(msg)
        self.assertEqual(crc1, 0)
        self.assertEqual(crc2, 0xEDEDD6)

    def testget_bit(self):  # test get_bit
        EXPECTED_RESULT = [
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            1,
            1,
            0,
            0,
        ]
        b = b"\xaa\xbb\xcc"
        for i in range(len(b) * 8):
            res = get_bit(b, i)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testget_bitarray(self):  # test get_bitarray
        EXPECTED_RESULT = [
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            1,
            1,
            0,
            0,
        ]
        b = b"\xaa\xbb\xcc"
        res = get_bitarray(b)
        self.assertEqual(res, EXPECTED_RESULT)

    def testbits2val(self):  # test bits2val for all data types
        b = b"\xaa\xbb\xcc"
        bitfield = get_bitarray(b)
        res = bits2val("UNT008", 1, bitfield)  # UINT
        res2 = int.from_bytes(b, "big")
        self.assertEqual(res, 11189196)
        self.assertEqual(res, res2)
        res = bits2val(rtt.INTS5, 0.1, [0, 0, 1, 0, 1])  # +ve INTS with scaling 0.1
        self.assertEqual(res, 0.5)
        res = bits2val(rtt.INTS5, 0.01, [1, 0, 1, 0, 1])  # -ve INTS with scaling 0.01
        self.assertEqual(res, -0.05)
        res = bits2val(rtt.CHAR8, 1, [0, 1, 0, 0, 0, 0, 0, 1])  # CHAR8
        self.assertEqual(res, "A")
        res = bits2val(rtt.INT8, 1, [0, 1, 1, 1, 1, 1, 1, 1])  # +ve 2's comp INT
        self.assertEqual(res, 127)
        res = bits2val(rtt.INT8, 1, [1, 0, 0, 0, 0, 0, 0, 1])  # -ve 2's comp INT
        self.assertEqual(res, -127)
        res = bits2val(rtt.INT8, 1, [0, 0, 1, 0, 1, 1, 0, 1])  # +ve 2's comp INT
        self.assertEqual(res, 45)
        res = bits2val(rtt.INT8, 1, [1, 1, 0, 1, 0, 0, 1, 1])  # -ve 2's comp INT
        self.assertEqual(res, -45)

    def testnum_setbits(self):  # test num_setbits
        res = num_setbits([1, 0, 1, 0, 1, 1, 0, 1])
        self.assertEqual(res, 5)
        res = num_setbits([0, 0, 0, 0, 1, 1, 0, 1])
        self.assertEqual(res, 3)
        res = num_setbits([0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(res, 0)

    def testcrc2bytes(self):  # test crc2bytes
        raw = (
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        content = raw[0:-3]
        crc1 = calc_crc24q(raw)
        crc2 = crc2bytes(content)
        self.assertEqual(crc1, 0)
        self.assertEqual(crc2, b"Z\xd7\xf7")

    def testlen2bytes(self):  # test len2bytes
        raw = (
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        payload = raw[3:-3]
        l = len(payload)
        res = len2bytes(payload)
        self.assertEqual(l, 19)
        self.assertEqual(res, b"\x00\x13")

    def testdatasiz(self):  # test datasiz
        dtw = ["DF024", "DF002", "DF054", "DF037"]
        EXPECTED_RESULT = [1, 12, 8, 3]
        for i, dt in enumerate(dtw):
            ds = datasiz(dt)
            self.assertEqual(ds, EXPECTED_RESULT[i])

    def testdatascale(self):  # test datascale
        dtw = ["DF034", "DF156", "DF185"]
        EXPECTED_RESULT = [
            1,
            0.001,
            0.000000011,
        ]
        for i, dt in enumerate(dtw):
            ds = datascale(dt)
            self.assertEqual(ds, EXPECTED_RESULT[i])
        # double check all the defined res are numbers
        for (_, res, _) in RTCM_DATA_FIELDS.values():
            self.assertIsInstance(res, (int, float))

    def testdatadesc(self):  # test datadesc
        dtw = ["DF054", "DF037", "DF001_01"]
        EXPECTED_RESULT = [
            "Leap Seconds, GPS-UTC",
            "GLONASS Smoothing Interval",
            "Reserved Field",
        ]
        for i, dt in enumerate(dtw):
            ds = datadesc(dt)
            self.assertEqual(ds, EXPECTED_RESULT[i])

    def testattsiz(self):  # test attsiz
        ats = [rtt.BIT8, rtt.INT23, rtt.UINT16, rtt.INTS32]
        EXPECTED_RESULT = [8, 23, 16, 32]
        for i, at in enumerate(ats):
            s = attsiz(at)
            self.assertEqual(s, EXPECTED_RESULT[i])

    def testatttyp(self):  # test atttyp
        ats = [rtt.BIT8, rtt.INT23, rtt.UINT16, rtt.INTS32]
        EXPECTED_RESULT = ["BIT", "INT", "UNT", "SNT"]
        for i, at in enumerate(ats):
            t = atttyp(at)
            self.assertEqual(t, EXPECTED_RESULT[i])

    def testtow2utc(self):  # test tow2utc
        res = str(tow2utc(387092000))
        self.assertEqual(res, "11:31:14")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
