"""
rtcmfile.py

This example illustrates a simple example implementation of a
RTCMMessage binary logfile reader using the
RTCMReader iterator functions and an external error handler.

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


def read(stream, errorhandler, quitonerror, validate):
    """
    Reads and parses RTCM message data from stream.
    """

    msgcount = 0
    ubr = RTCMReader(
        stream, errorhandler=errorhandler, quitonerror=quitonerror, validate=validate
    )
    for _, parsed_data in ubr:
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":
    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")

    print("Enter fully qualified name of file containing binary RTCM data: ", end="")
    filename = input().strip('"')
    print(
        "How do you want to handle protocol errors?",
        "(0 = ignore, 1 = log and continue, 3 = raise and stop) (1) ",
        end="",
    )
    val = input() or "1"
    iquitonerror = int(val)
    print("Do you want to validate the message checksums (y/n)? (y) ", end="")
    val = input() or "y"
    ivalidate = val in YES

    print(f"Opening file {filename}...")
    with open(filename, "rb") as fstream:
        read(fstream, errhandler, iquitonerror, ivalidate)
    print("Test Complete")
