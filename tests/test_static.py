"""
Helper, Property and Static method tests for pyrtcm.rtcmMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCM_DATA_FIELDS, RTCMMessage
import pyrtcm.rtcmtypes_core as rtt
from pyrtcm.rtcmhelpers import (
    hextable,
    calc_crc24q,
    get_bit,
    bits2val,
    crc2bytes,
    len2bytes,
    datasiz,
    datascale,
    datadesc,
    attsiz,
    atttyp,
    tow2utc,
    att2idx,
    att2name,
    escapeall,
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

    def testgetbit(self):  # test getbit
        val = 0b1011010110001
        bits = val.to_bytes(2, "big")
        print(f"{val:016b} {bits}")
        res = get_bit(bits, 1)
        self.assertEqual(res, 0)
        res = get_bit(bits, 3)
        self.assertEqual(res, 1)
        res = get_bit(bits, 5)
        self.assertEqual(res, 1)
        res = get_bit(bits, 10)
        self.assertEqual(res, 1)
        res = get_bit(bits, 12)
        self.assertEqual(res, 0)

    def testbits2val(self):  # test bits2val for all data types
        # b = b"\xaa\xbb\xcc"
        # bitfield = getbits(b, 0, len(b) * 8)  # get_bitarray(b)
        # res = bits2val("UNT008", 1, bitfield)  # UINT
        # res2 = int.from_bytes(b, "big")
        # self.assertEqual(res, 11189196)
        # self.assertEqual(res, res2)
        res = bits2val(rtt.INTS5, 0.1, 0b00101)  # +ve INTS with scaling 0.1
        self.assertEqual(res, 0.5)
        res = bits2val(rtt.INTS5, 0.01, 0b10101)  # -ve INTS with scaling 0.01
        self.assertEqual(res, -0.05)
        res = bits2val(rtt.CHAR8, 1, 0b01000001)  # CHAR8
        self.assertEqual(res, "A")
        res = bits2val(rtt.INT8, 1, 0b01111111)  # +ve 2's comp INT
        self.assertEqual(res, 127)
        res = bits2val(rtt.INT8, 1, 0b10000001)  # -ve 2's comp INT
        self.assertEqual(res, -127)
        res = bits2val(rtt.INT8, 1, 0b00101101)  # +ve 2's comp INT
        self.assertEqual(res, 45)
        res = bits2val(rtt.INT8, 1, 0b11010011)  # -ve 2's comp INT
        self.assertEqual(res, -45)

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
        for _, res, _ in RTCM_DATA_FIELDS.values():
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

    def testatt2idx(self):  # test att2idx
        EXPECTED_RESULT = [4, 16, 101, 0]
        atts = ["DF389_04", "DF406_16", "DF406_101", "DF396"]
        for i, att in enumerate(atts):
            res = att2idx(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testatt2name(self):  # test att2name
        EXPECTED_RESULT = ["DF389", "DF406", "DF406", "DF396"]
        atts = ["DF389_04", "DF406_16", "DF406_101", "DF396"]
        for i, att in enumerate(atts):
            res = att2name(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testescapeall(self):
        EXPECTED_RESULT = "b'\\x68\\x65\\x72\\x65\\x61\\x72\\x65\\x73\\x6f\\x6d\\x65\\x63\\x68\\x61\\x72\\x73'"
        val = b"herearesomechars"
        res = escapeall(val)
        print(res)
        self.assertEqual(res, EXPECTED_RESULT)

    def testismsm(self):
        msg1077 = RTCMMessage(
            payload=b"CP\x000\xab\x88\xa6\x00\x00\x05GX\x02\x00\x00\x00\x00 \x00\x80\x00\x7f\x7fZZZ\x8aB\x1a\x82Z\x92Z8\x00\x00\x00\x00\x00\r\x11\xe1\xa4tf:f\xe3L,\xb1~\x9d\xf6\x87\xaf\xa0\xee\xff\x98\x14(B!A\xfc\xa9\xfaX\x96\n\x89K\x91\x971\x19c\xb6\x04\xa9\xe1F9l\xc3\x8ee\xd8\xe1\xaas\xa5\x1f?\xe9yc\x97\x98\xc6\x1f`)\xc9\xdck\xa5\x8e\xbcZ\x02SP\x82Yu\x06ex\x06Y\x00x\x10N\xf8T\x00\x05\xb0\xfa\x83\x90\xa2\x83\x89\xdc\xfc\xf1l|\xfeW~\\\xdb~h\x1c\x06\xc3\x82\x07#\x07\xfa\xe6pz\xf0\x03\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xa9:\xaa\xaa\xaa\xa0\x00\x0bB`\xac'\t\xc2P\xb4.\x0b\x82p\x88-\t\x81\xf0\xb4.\nB\xdf\x8d\xc1k\xef\xf7\xde\xb7\xfa\xf0\x18\x13'\xf5/\xea\xa2J\xe4\x99\"T\x04\xb8\x19\xec\xb5Y\xdes\xbc\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        msg1007 = RTCMMessage(payload=b">\xf4\xd2\x03ABC\xea")
        msg4072 = RTCMMessage(
            payload=b"\xfe\x80\x01\x00\x00\x00\x13\n\xb8\x8a@\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01\xff\x9f\x00\x16\x02\x00\xfe\\\x00\x19\x02\x01\xfe\xdd\x00\x1d\x03\x00\x02\x86\x00\x13\x05\x00\x00\x00\x01\x90\x06\x00\x03\xf7\x00\x1a\x06\x01\x04%\x00\x1e"
        )
        self.assertTrue(msg1077.ismsm)
        self.assertFalse(msg1007.ismsm)
        self.assertFalse(msg4072.ismsm)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
