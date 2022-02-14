"""
Stream method tests using actual receiver binary outputs for pyrtcm.rtcmReader 

Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

# from pyrtcm import (
#     RTCMReader,
# )
# from pyrtcm.exceptions import RTCMStreamError, RTCMParseError
# import pyrtcm.rtcmtypes_core as rtt


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        # self.testdump = open(os.path.join(dirname, "testdump.log"), "wb")

    def tearDown(self):
        # self.testdump.close()
        pass

    # def testMIXEDRTCM(
    #     self,
    # ):  # test mixed stream of NMEA, rtcm & RTCM messages with protfilter = 7
    #     EXPECTED_RESULTS = (
    #         "<NMEA(GNGLL, lat=32.0658325, NS=N, lon=34.773819, EW=E, time=08:41:58, status=A, posMode=D)>",
    #         "<RTCM3(1005)>",
    #         "<RTCM3(4072)>",
    #         "<RTCM3(1077)>",
    #         "<RTCM3(1087)>",
    #         "<RTCM3(1097)>",
    #         "<RTCM3(1127)>",
    #         "<RTCM3(1230)>",
    #         "<rtcm(NAV-PVT, iTOW=08:41:59, year=2022, month=2, day=8, hour=8, min=41, second=59, validDate=1, validTime=1, fullyResolved=1, validMag=0, tAcc=21, nano=360400, fixType=5, gnssFixOk=1, difSoln=1, psmState=0, headVehValid=0, carrSoln=0, confirmedAvai=1, confirmedDate=1, confirmedTime=1, numSV=31, lon=34.773819, lat=32.0658325, height=72134, hMSL=54642, hAcc=685, vAcc=484, velN=0, velE=0, velD=0, gSpeed=0, headMot=290.13822, sAcc=10, headAcc=20.15693, pDOP=99.99, invalidLlh=0, lastCorrectionAge=0, reserved0=860200482, headVeh=0.0, magDec=0.0, magAcc=0.0)>",
    #         "<NMEA(GNRMC, time=08:41:59, status=A, lat=32.0658325, NS=N, lon=34.773819, EW=E, spd=0.0, cog=, date=2022-02-08, mv=, mvEW=, posMode=D, navStatus=V)>",
    #     )
    #     dirname = os.path.dirname(__file__)
    #     stream = open(os.path.join(dirname, "pygpsdata-MIXED-RTCM3.log"), "rb")
    #     i = 0
    #     raw = 0
    #     ubr = rtcmReader(stream, protfilter=7)
    #     for (raw, parsed) in ubr.iterate(quitonerror=ubt.ERR_RAISE):
    #         if raw is not None:
    #             self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
    #             i += 1
    #     stream.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
