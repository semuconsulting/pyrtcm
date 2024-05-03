"""
msmparser.py

Usage:

python3 msmparser.py infile="../tests/pygpsdata-RTCM3.log"


Each RTCM3 MSM message contains data for multiple satellites and cells
(combination of satellite and signal). The mapping between each
data item and its corresponding satellite PRN or signal ID can be performed
by pyrtcm helper functions `sat2prn` and `cell2prn`.

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

from pyrtcm import ATT_NCELL  # list of all sat attribute names
from pyrtcm import ATT_NSAT  # list of all cell attribute names
from pyrtcm import RTCM_MSGIDS, RTCMMessage, RTCMReader, cell2prn, sat2prn

# map of msg identity to GNSS name, epoch attribute name
GNSSMAP = {
    "107": ("GPS", "DF004"),
    "108": ("GLONASS", "DF034"),
    "109": ("GALILEO", "DF248"),
    "110": ("SBAS", "DF004"),
    "111": ("QZSS", "DF428"),
    "112": ("BEIDOU", "DF427"),
    "113": ("NAVIC", "DF546"),
}


def process_msm(msg: RTCMMessage) -> tuple:
    """
    Process individual MSM message.

    :return: tuple of (metadata, sat data array, cell data array)
    :rtype: tuple
    """

    satmap = sat2prn(msg)  # maps indices to satellite PRNs
    cellmap = cell2prn(msg)  # maps indices to cells (satellite PRN, signal ID)
    meta = {}
    gmap = GNSSMAP[msg.identity[0:3]]
    meta["identity"] = msg.identity
    meta["gnss"] = gmap[0]
    meta["station"] = msg.DF003
    meta["epoch"] = getattr(msg, gmap[1])
    meta["sats"] = msg.NSat
    meta["cells"] = msg.NCell
    msmsats = []
    for i in range(1, msg.NSat + 1):  # iterate through satellites
        sats = {}
        sats["PRN"] = satmap[i]
        for attr in ATT_NSAT:
            if hasattr(msg, f"{attr}_{i:02d}"):
                sats[attr] = getattr(msg, f"{attr}_{i:02d}")
        msmsats.append(sats)
    msmcells = []
    for i in range(1, msg.NCell + 1):  # iterate through cells (satellite/signal)
        cells = {}
        cells["PRN"], cells["SIGNAL"] = cellmap[i]
        for attr in ATT_NCELL:
            if hasattr(msg, f"{attr}_{i:02d}"):
                cells[attr] = getattr(msg, f"{attr}_{i:02d}")
        msmcells.append(cells)

    return (meta, msmsats, msmcells)


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
                    if "MSM" in RTCM_MSGIDS[parsed.identity]:
                        # print(parsed)
                        msmarray = process_msm(parsed)
                        print(msmarray)

                        # to then iterate through a specific data item,
                        # e.g. the satellite DF398 (rough range) value:
                        for sat in msmarray[1]:  # satellite data array
                            print(f'PRN {sat["PRN"]}: {sat["DF398"]}')
                except KeyError:
                    pass  # unimplemented message type


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
