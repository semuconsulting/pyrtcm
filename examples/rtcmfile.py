"""
rtcmfile.py

This example illustrates a simple example implementation of a
rtcmMessage and/or NMEAMessage binary logfile reader using the
rtcmReader iterator functions and an external error handler.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyrtcm import RTCMReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def read(stream):
    """
    Reads and parses rtcm message data from stream.
    """

    msgcount = 0

    ubr = RTCMReader(stream)
    for (_, parsed_data) in ubr:
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")

    print("Enter fully qualified name of file containing binary rtcm data: ", end="")
    filename = input().strip('"')

    print(f"Opening file {filename}...")
    with open(filename, "rb") as fstream:
        read(fstream)
    print("Test Complete")
