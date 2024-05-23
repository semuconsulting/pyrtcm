"""
Helper, Property and Static method tests for pyrtcm.rtcmMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCM_DATA_FIELDS, RTCMMessage, RTCMReader
import pyrtcm.rtcmtypes_core as rtt
from pyrtcm.rtcmhelpers import (
    hextable,
    calc_crc24q,
    get_bit,
    crc2bytes,
    len2bytes,
    datadesc,
    tow2utc,
    att2idx,
    att2name,
    escapeall,
    parse_msm,
    parse_4076_201,
)


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def testdatafields(self):  # check datafield types are correct
        for nam, siz, res, _ in RTCM_DATA_FIELDS.values():
            self.assertTrue(isinstance(nam, str))
            self.assertTrue(isinstance(siz, int))
            self.assertTrue(siz >= 0)
            self.assertTrue(isinstance(res, (int, float)))

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

    def testtow2utc(self):  # test tow2utc
        res = str(tow2utc(387092000))
        self.assertEqual(res, "11:31:14")

    def testatt2idx(self):  # test att2idx
        EXPECTED_RESULT = [4, 16, 101, 0, (3, 6), 0]
        atts = ["svid_04", "gnssId_16", "cno_101", "gmsLon", "gnod_03_06", "dodgy_xx"]
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

    def testparsemsm(self):
        EXPECTED_RESULT = (
            {
                "identity": "1077",
                "gnss": "GPS",
                "station": 0,
                "epoch": 204137001,
                "sats": 10,
                "cells": 17,
            },
            [
                {
                    "PRN": "005",
                    "DF397": 75,
                    "DF398": 0.005859375,
                    "DF399": -178,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "007",
                    "DF397": 75,
                    "DF398": 0.5341796875,
                    "DF399": -304,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "009",
                    "DF397": 81,
                    "DF398": 0.7626953125,
                    "DF399": -643,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "013",
                    "DF397": 72,
                    "DF398": 0.138671875,
                    "DF399": 477,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "014",
                    "DF397": 67,
                    "DF398": 0.5498046875,
                    "DF399": -52,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "015",
                    "DF397": 80,
                    "DF398": 0.11328125,
                    "DF399": 645,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "017",
                    "DF397": 75,
                    "DF398": 0.8037109375,
                    "DF399": 529,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "019",
                    "DF397": 82,
                    "DF398": 0.1025390625,
                    "DF399": 643,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "020",
                    "DF397": 75,
                    "DF398": 0.521484375,
                    "DF399": -428,
                    "ExtSatInfo": 0,
                },
                {
                    "PRN": "030",
                    "DF397": 71,
                    "DF398": 0.345703125,
                    "DF399": -181,
                    "ExtSatInfo": 0,
                },
            ],
            [
                {
                    "CELLPRN": "005",
                    "CELLSIG": "1C",
                    "DF404": -0.9231,
                    "DF405": 0.00014309026300907135,
                    "DF406": 0.00014193402603268623,
                    "DF407": 341,
                    "DF408": 45.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "005",
                    "CELLSIG": "2L",
                    "DF404": -0.9194,
                    "DF405": 0.00014183297753334045,
                    "DF406": 0.00014339853078126907,
                    "DF407": 341,
                    "DF408": 38.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "007",
                    "CELLSIG": "1C",
                    "DF404": -0.8321000000000001,
                    "DF405": 0.0003883279860019684,
                    "DF406": 0.00039040297269821167,
                    "DF407": 341,
                    "DF408": 43.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "007",
                    "CELLSIG": "2L",
                    "DF404": -0.8326,
                    "DF405": 0.00038741156458854675,
                    "DF406": 0.00038743019104003906,
                    "DF407": 341,
                    "DF408": 39.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "009",
                    "CELLSIG": "1C",
                    "DF404": -0.4107,
                    "DF405": -0.0004838351160287857,
                    "DF406": -0.0004843934439122677,
                    "DF407": 341,
                    "DF408": 39.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "009",
                    "CELLSIG": "2L",
                    "DF404": -0.4072,
                    "DF405": -0.00046883709728717804,
                    "DF406": -0.00046825408935546875,
                    "DF407": 341,
                    "DF408": 37.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "013",
                    "CELLSIG": "1C",
                    "DF404": 0.2451,
                    "DF405": 0.0003478657454252243,
                    "DF406": 0.0003473707474768162,
                    "DF407": 341,
                    "DF408": 45.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "014",
                    "CELLSIG": "1C",
                    "DF404": -0.0693,
                    "DF405": 0.0002196934074163437,
                    "DF406": 0.00021758908405900002,
                    "DF407": 341,
                    "DF408": 46.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "014",
                    "CELLSIG": "2L",
                    "DF404": -0.0684,
                    "DF405": 0.00021521002054214478,
                    "DF406": 0.00021597417071461678,
                    "DF407": 341,
                    "DF408": 46.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "015",
                    "CELLSIG": "1C",
                    "DF404": 0.9390000000000001,
                    "DF405": -0.00018852390348911285,
                    "DF406": -0.00018658116459846497,
                    "DF407": 341,
                    "DF408": 39.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "015",
                    "CELLSIG": "2L",
                    "DF404": 0.9417000000000001,
                    "DF405": -0.00018319115042686462,
                    "DF406": -0.00018350128084421158,
                    "DF407": 341,
                    "DF408": 34.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "017",
                    "CELLSIG": "1C",
                    "DF404": 0.2384,
                    "DF405": -0.00010087713599205017,
                    "DF406": -9.993184357881546e-05,
                    "DF407": 341,
                    "DF408": 45.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "017",
                    "CELLSIG": "2L",
                    "DF404": 0.2416,
                    "DF405": -9.844452142715454e-05,
                    "DF406": -9.724870324134827e-05,
                    "DF407": 341,
                    "DF408": 38.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "019",
                    "CELLSIG": "1C",
                    "DF404": 0.6636000000000001,
                    "DF405": 0.00047875382006168365,
                    "DF406": 0.0004128236323595047,
                    "DF407": 295,
                    "DF408": 31.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "020",
                    "CELLSIG": "1C",
                    "DF404": -0.9556,
                    "DF405": 0.00043664872646331787,
                    "DF406": 0.0004355977289378643,
                    "DF407": 341,
                    "DF408": 45.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "030",
                    "CELLSIG": "1C",
                    "DF404": -0.21480000000000002,
                    "DF405": -0.0003105681389570236,
                    "DF406": -0.0003112703561782837,
                    "DF407": 341,
                    "DF408": 46.0,
                    "DF420": 0,
                },
                {
                    "CELLPRN": "030",
                    "CELLSIG": "2L",
                    "DF404": -0.2174,
                    "DF405": -0.00030865520238876343,
                    "DF406": -0.00030898721888661385,
                    "DF407": 341,
                    "DF408": 41.0,
                    "DF420": 0,
                },
            ],
        )
        msg1077 = RTCMMessage(
            payload=b"CP\x000\xab\x88\xa6\x00\x00\x05GX\x02\x00\x00\x00\x00 \x00\x80\x00\x7f\x7fZZZ\x8aB\x1a\x82Z\x92Z8\x00\x00\x00\x00\x00\r\x11\xe1\xa4tf:f\xe3L,\xb1~\x9d\xf6\x87\xaf\xa0\xee\xff\x98\x14(B!A\xfc\xa9\xfaX\x96\n\x89K\x91\x971\x19c\xb6\x04\xa9\xe1F9l\xc3\x8ee\xd8\xe1\xaas\xa5\x1f?\xe9yc\x97\x98\xc6\x1f`)\xc9\xdck\xa5\x8e\xbcZ\x02SP\x82Yu\x06ex\x06Y\x00x\x10N\xf8T\x00\x05\xb0\xfa\x83\x90\xa2\x83\x89\xdc\xfc\xf1l|\xfeW~\\\xdb~h\x1c\x06\xc3\x82\x07#\x07\xfa\xe6pz\xf0\x03\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xa9:\xaa\xaa\xaa\xa0\x00\x0bB`\xac'\t\xc2P\xb4.\x0b\x82p\x88-\t\x81\xf0\xb4.\nB\xdf\x8d\xc1k\xef\xf7\xde\xb7\xfa\xf0\x18\x13'\xf5/\xea\xa2J\xe4\x99\"T\x04\xb8\x19\xec\xb5Y\xdes\xbc\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        res = parse_msm(msg1077)
        # print(res)
        self.assertEqual(res, EXPECTED_RESULT)
        msg1005 = RTCMReader.parse(
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        self.assertEqual(parse_msm(msg1005), None)

    def testparse4076_201(self):
        EXPECTED_RESULT = {
            0: {
                "Layer Height": 450,
                "Cosine Coefficients": [
                    35.36,
                    2.34,
                    -12.18,
                    -2.09,
                    2.91,
                    0.43,
                    -0.23500000000000001,
                    0.9550000000000001,
                    0.17,
                    -0.78,
                    -0.14,
                    0.28,
                    0.14,
                    18.145,
                    0.745,
                    -1.705,
                    -0.6,
                    1.01,
                    -0.645,
                    -0.245,
                    0.39,
                    -0.01,
                    -0.38,
                    0.04,
                    0.23500000000000001,
                    2.5100000000000002,
                    0.61,
                    0.01,
                    -0.24,
                    0.075,
                    0.145,
                    0.07,
                    0.06,
                    -0.035,
                    -0.07,
                    -0.055,
                    -1.25,
                    -0.16,
                    -0.41000000000000003,
                    0.215,
                    0.035,
                    -0.12,
                    -0.04,
                    0.135,
                    0.015,
                    -0.005,
                    -0.22,
                    -0.195,
                    0.445,
                    0.17500000000000002,
                    -0.42,
                    -0.185,
                    0.26,
                    0.06,
                    -0.22,
                    0.095,
                    0.03,
                    -0.1,
                    0.07,
                    0.02,
                    -0.015,
                    -0.005,
                    -0.06,
                    -0.065,
                    0.125,
                    -0.03,
                    -0.035,
                    0.03,
                    0.06,
                    -0.03,
                    0.36,
                    0.07,
                    -0.005,
                    0.045,
                    0.025,
                    -0.03,
                    -0.09,
                    -0.005,
                    0.06,
                    -0.035,
                    -0.05,
                    -0.165,
                    -0.01,
                    0.02,
                    0.04,
                    0.1,
                    0.025,
                    0.05,
                    0.075,
                    0.01,
                    0.005,
                ],
                "Sine Coefficients": [
                    2.15,
                    0.375,
                    -1.945,
                    -0.12,
                    1.115,
                    0.1,
                    -0.8250000000000001,
                    0.34500000000000003,
                    0.19,
                    -0.375,
                    0.42,
                    0.26,
                    -3.5100000000000002,
                    -0.195,
                    0.99,
                    0.33,
                    -0.495,
                    -0.03,
                    -0.08,
                    -0.06,
                    0.0,
                    -0.215,
                    -0.055,
                    1.36,
                    0.12,
                    -0.615,
                    -0.06,
                    0.28,
                    0.145,
                    -0.095,
                    -0.105,
                    0.08,
                    0.11,
                    0.0,
                    -0.02,
                    -0.21,
                    -0.1,
                    0.035,
                    0.075,
                    -0.1,
                    -0.09,
                    0.055,
                    -0.775,
                    -0.08,
                    0.105,
                    -0.015,
                    -0.14,
                    0.005,
                    0.16,
                    -0.035,
                    -0.03,
                    -0.005,
                    0.05,
                    -0.02,
                    0.085,
                    0.02,
                    -0.025,
                    0.315,
                    0.035,
                    0.01,
                    -0.015,
                    0.015,
                    -0.015,
                    0.06,
                    0.015,
                    -0.075,
                    -0.03,
                    0.05,
                    0.05,
                    -0.025,
                    0.09,
                    0.005,
                    -0.015,
                    -0.03,
                    0.02,
                    -0.06,
                    -0.015,
                    0.04,
                ],
            }
        }
        msg = RTCMMessage(
            payload=b'\xfe\xc7\x92\x0e\xcb\x8c\x00\x00\x00\x00\x05\xb7ct\x00:\x9e\xcf\x9f\xcb\xc0H\xc0\n\xdf\xfa \x17\xe0\x04_\xec\x9f\xfc\x80\x07\x00\x03\x81\xc5\xa0\x12\xbf\xd5\x7f\xf1\x00\x19_\xef\xff\xf9\xe0\t\xdf\xff\xdf\xf6\x80\x01\x00\x05\xe0>\xc0\x0f@\x00_\xfa\x00\x01\xe0\x03\xa0\x01\xc0\x01\x9f\xff?\xfe_\xfe\xbf\xe0\xdf\xfc\x1f\xf5\xc0\x05`\x00\xff\xfd\x1f\xff\x00\x03`\x00\x7f\xff\xff\xfa\x9f\xfb \x0b \x04\x7f\xf5\x9f\xfb`\x06\x80\x01\x9f\xfa\x80\x02`\x00\xdf\xfd\x80\x01\xc0\x00\x9f\xff\xbf\xff\xff\xfe\x9f\xfe`\x03?\xff_\xff \x00\xc0\x01\x9f\xff@\t\x00\x01\xdf\xff\xe0\x01 \x00\xbf\xff_\xfd\xdf\xff\xe0\x01\x9f\xff?\xfe\xdf\xfb\xff\xff\xc0\x00\x80\x01\x00\x02\x80\x00\xa0\x01@\x01\xe0\x00@\x00 5\xc0\t\x7f\xcf\x7f\xfd\x00\x1b\xe0\x02\x9f\xeb`\x08\xa0\x04\xdf\xf6\xa0\n\x80\x06\x9f\xa8_\xfb \x18\xc0\x08_\xf3\xbf\xff_\xfe\x1f\xfe\x80\x00\x1f\xfa\xbf\xfe\xa0"\x00\x03\x1f\xf0\xbf\xfe\x80\x07\x00\x03\xbf\xfd\xbf\xfd`\x02\x00\x02\xc0\x00\x1f\xff\x9f\xfa\xdf\xfd\x80\x00\xe0\x01\xff\xfd\x9f\xfd\xc0\x01\x7f\xec\xbf\xfe\x00\x02\xbf\xff\xbf\xfc\x80\x00 \x04\x1f\xff?\xff_\xff\xe0\x01_\xff\x80\x02 \x00\x9f\xff`\x07\xe0\x00\xe0\x00_\xff\xa0\x00\x7f\xff\xa0\x01\x80\x00\x7f\xfe?\xff@\x01@\x01_\xff`\x02@\x00?\xff\xbf\xff@\x00\x9f\xfe\x9f\xff\xa0\x01\x00'
        )
        res = parse_4076_201(msg)
        # print(res)
        self.assertEqual(res, EXPECTED_RESULT)
        msg1005 = RTCMReader.parse(
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        self.assertEqual(parse_4076_201(msg1005), None)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
