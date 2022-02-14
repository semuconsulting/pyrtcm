"""
Helper, Property and Static method tests for pyrtcm.rtcmMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

# from pyrtcm import RTCMMessage, RTCMReader
# import pyrtcm.rtcmtypes_core as rtt
# import pyrtcm.rtcmtypes_get as rtg
# from pyrtcm.rtcmhelpers import (
#     hextable,
#     calc_crc24q,
#     get_bit,
#     get_bitarray,
#     bits_2_val,
# )


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)

    def tearDown(self):
        self.streamNAV.close()

    # def testhextable(self):  # test hextable*( method)
    #     EXPECTED_RESULT = "000: 2447 4e47 4c4c 2c35 3332 372e 3034 3331  | b'$GNGLL,5327.0431' |\n016: 392c 532c 3030 3231 342e 3431 3339 362c  | b'9,S,00214.41396,' |\n032: 452c 3232 3332 3332 2e30 302c 412c 412a  | b'E,223232.00,A,A*' |\n048: 3638 0d0a                                | b'68\\r\\n' |\n"
    #     res = hextable(b"$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n", 8)
    #     self.assertEqual(res, EXPECTED_RESULT)

    # def testcrc24q(self):  # test crc24q calculation on RTCM3 message
    #     msgcrc = b"\xd3\x00\x04L\xe0\x00\x80\xed\xed\xd6"  # msg with crc
    #     msg = msgcrc[0:-3]  # message without crc
    #     crc1 = calc_crc24q(msgcrc)
    #     crc2 = calc_crc24q(msg)
    #     self.assertEqual(crc1, 0)
    #     self.assertEqual(crc2, 0xEDEDD6)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
