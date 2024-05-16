"""
msmparser.py

Usage:

python3 msmparser.py infile="../tests/pygpsdata-RTCM3.log"


Each RTCM3 MSM message contains data for multiple satellites and cells
(combination of satellite and signal).

pyrtcm parses MSM messages into a flat data structure, with repeating
element names suffixed by a 2-digit index (e.g. `DF405_02`) and
(optionally) labelled with their corresponding satellite PRN and signal ID
e.g. `DF405_02(005,2L)`. Note that indices start at 1, not 0.

It is sometimes more convenient to parse the data into one or more
iterable arrays, with each array element corresponding to a particular
satellite or cell.

This example illustrates how to parse MSM messages from a binary data log
into a series of iterable data arrays keyed on satellite PRN and signal ID.

The output data structure is a tuple containing:

(metadata, [satellite data array], [cell data array]).

Arrays could just as easily be numpy arrays if preferred.

Created on 18 Apr 2024

:author: semuadmin
:copyright: SEMU Consulting © 2024
:license: BSD 3-Clause
"""

from sys import argv

from pyrtcm import RTCMReader, parse_msm


def main(**kwargs):
    """
    Main routine.

    :param str fname: fully qualified path to input file
    """

    infile = kwargs.get("infile", "../tests/pygpsdata-RTCM3.log")
    with open(infile, "rb") as stream:

        rtr = RTCMReader(stream)
        for _, parsed in rtr:
            if parsed is not None:
                try:
                    msmarray = parse_msm(parsed)
                    if msmarray is not None:
                        print(msmarray)
                        # to then iterate through a specific data item,
                        # e.g. the satellite DF398 (rough range) value:
                        for sat in msmarray[1]:  # satellite data array
                            print(f'PRN {sat["PRN"]}: {sat["DF398"]}')
                except KeyError:
                    pass  # unimplemented message type


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
