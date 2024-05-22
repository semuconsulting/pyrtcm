"""
Test for errors in datafield and payload definitions

Created on 19 Feb 2022

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(os.path.join(ROOT, "src"))

from pyrtcm import RTCM_PAYLOADS_GET, RTCM_DATA_FIELDS


class DefinitionTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    # def testpayloaddfs(
    #     self,
    # ):  # test all payload datafields are defined in RTCM_DATA_FIELDS
    #     for _, pdict in RTCM_PAYLOADS_GET.items():
    #         for df, _ in pdict.items():
    #             if df[0:3] not in ("gro", "opt"):
    #                 self.assertIn(df, RTCM_DATA_FIELDS)

    # def testdfres(self):  # test all size and resolution values are int or float
    #     for _, (_, siz, res, _) in RTCM_DATA_FIELDS.items():
    #         self.assertIsInstance(siz, (int, float))
    #         self.assertIsInstance(res, (int, float))
