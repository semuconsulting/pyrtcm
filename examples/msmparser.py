"""
msmparser.py

Each RTCM3 MSM message contains data for multiple satellites and cells
(combination of satellite and signal). The mapping between each
data item and its corresponding satellite PRN or signal ID can be performed
by pyrtcm helper functions `sat2prn` and `cell2prn`.

pyrtcm parses MSM messages into a flat data structure, with repeating
element names suffixed by a 2-digit index (e.g. `DF405_02`) and
(optionally) labelled with their corresponding satellite PRN and signal ID
e.g. `DF405_02(005,2L)` 

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

from pyrtcm import (
    ATT_NCELL,
    ATT_NSAT,
    RTCMMessage,
    RTCMReader,
    cell2prn,
    sat2prn,
)

# binary log of RTCM3 messages e.g. from NTRIP caster or ZED-F9P receiver
INFILE = "./tests/pygpsdata-RTCM3.log"

# map of GNSS name, epoch attribute name
GNSS = {
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

    satmap = sat2prn(msg)  # array of satellite PRN
    cellmap = cell2prn(msg)  # array of cells (satellite PRN, signal ID)
    meta = {}
    gmap = GNSS[msg.identity[0:3]]
    meta["identity"] = msg.identity
    meta["gnss"] = gmap[0]
    meta["station"] = msg.DF003
    meta["epoch"] = getattr(msg, gmap[1])
    meta["sats"] = msg.NSat
    meta["cells"] = msg.NCell
    msmsats = []
    for i in range(msg.NSat):  # iterate through satellites
        sats = {}
        sats["PRN"] = satmap[i + 1]
        for attr in ATT_NSAT:
            if hasattr(msg, f"{attr}_{i+1:02d}"):
                sats[attr] = getattr(msg, f"{attr}_{i+1:02d}")
        msmsats.append(sats)
    msmcells = []
    for i in range(msg.NCell):  # iterate through satellite/signal cells
        cells = {}
        cells["PRN"], cells["SIGNAL"] = cellmap[i + 1]
        for attr in ATT_NCELL:
            if hasattr(msg, f"{attr}_{i+1:02d}"):
                cells[attr] = getattr(msg, f"{attr}_{i+1:02d}")
        msmcells.append(cells)

    return (meta, msmsats, msmcells)


with open(INFILE, "rb") as stream:
    rtr = RTCMReader(stream)
    for raw, parsed in rtr:
        if parsed is not None:
            if parsed.ismsm:
                # print(parsed)
                msmarray = process_msm(parsed)
                print(msmarray)

                # to then iterate through a specific data item,
                # e.g. the satellite DF398 (rough range) value:
                for sat in msmarray[1]:  # satellite data array
                    print(f"PRN {sat["PRN"]}: {sat["DF398"]}")
