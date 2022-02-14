"""
Test suite for pyrtcm

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

import os
import sys
import unittest
from importlib import import_module

# inject local copy to avoid testing the installed version instead of the one in the repo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
currdir = os.path.dirname(__file__)
import pyrtcm  # pylint: disable=wrong-import-position

print(f"Testing Local Version: {pyrtcm.version}")

# find files and the tests in them
mainsuite = unittest.TestSuite()
for modulename in [
    os.path.splitext(x)[0]
    for x in os.listdir(currdir or ".")
    if x != __file__ and x.startswith("test_") and x.endswith(".py")
]:
    try:
        module = import_module(modulename)
    except ImportError as err:
        print(f"skipping {modulename}, {err}")
    else:
        testsuite = unittest.findTestCases(module)
        print(f"found {testsuite.countTestCases()} tests in {modulename}")
        mainsuite.addTest(testsuite)

VERBOSITY = 1
if "-v" in sys.argv[1:]:
    VERBOSITY = 2
print("-" * 70)

# run the collected tests
testRunner = unittest.TextTestRunner(verbosity=VERBOSITY)
# ~ testRunner = unittest.ConsoleTestRunner(verbosity=verbosity)
result = testRunner.run(mainsuite)

# set exit code accordingly to test results
sys.exit(not result.wasSuccessful())
