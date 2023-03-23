"""
RTCM Lookup and Decode Tables

Created on 7 Jul 2022

Information sourced from RTCM STANDARD 10403.3 © 2016 RTCM

:author: semuadmin
"""

#################################################
# GPS
#################################################

GPS_PRN_MAP = {}
for i in range(1, 64):
    GPS_PRN_MAP[i] = f"{i:03d}"
GPS_PRN_MAP[64] = "Reserved"

GPS_SIG_MAP = {
    1: "Reserved",
    2: "1C",
    3: "1P",
    4: "1W",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "2C",
    9: "2P",
    10: "2W",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "2S",
    16: "2L",
    17: "2X",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "5I",
    23: "5Q",
    24: "5X",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "1S",
    31: "1L",
    32: "1X",
}

#################################################
# GLONASS
#################################################

GLONASS_PRN_MAP = {}
for i in range(1, 25):
    GLONASS_PRN_MAP[i] = f"{i:03d}"
for i in range(25, 65):
    GLONASS_PRN_MAP[i] = "Reserved"

GLONASS_SIG_MAP = {
    1: "Reserved",
    2: "1C",
    3: "1P",
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "2C",
    9: "2P",
    10: "Reserved",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "Reserved",
    16: "Reserved",
    17: "Reserved",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "Reserved",
    23: "Reserved",
    24: "Reserved",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "Reserved",
    31: "Reserved",
    32: "Reserved",
}

#################################################
# GALILEO
#################################################

GALILEO_PRN_MAP = {}
for i in range(1, 51):
    GALILEO_PRN_MAP[i] = f"{i:03d}"
GALILEO_PRN_MAP[51] = "GIOVE-A"
GALILEO_PRN_MAP[52] = "GIOVE-B"
for i in range(53, 65):
    GALILEO_PRN_MAP[i] = "Reserved"

GALILEO_SIG_MAP = {
    1: "Reserved",
    2: "1C",
    3: "1A",
    4: "1B",
    5: "1X",
    6: "1Z",
    7: "Reserved",
    8: "6C",
    9: "6A",
    10: "6B",
    11: "6X",
    12: "6Z",
    13: "Reserved",
    14: "7I",
    15: "7Q",
    16: "7X",
    17: "Reserved",
    18: "8I",
    19: "8Q",
    20: "8X",
    21: "Reserved",
    22: "5I",
    23: "5Q",
    24: "5X",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "Reserved",
    31: "Reserved",
    32: "Reserved",
}

#################################################
# SBAS
#################################################

SBAS_PRN_MAP = {}
for i in range(1, 40):
    SBAS_PRN_MAP[i] = f"{i+119:03d}"
for i in range(40, 65):
    SBAS_PRN_MAP[i] = "Reserved"

SBAS_SIG_MAP = {
    1: "Reserved",
    2: "1C",
    3: "Reserved",
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "Reserved",
    9: "Reserved",
    10: "Reserved",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "Reserved",
    16: "Reserved",
    17: "Reserved",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "5I",
    23: "5Q",
    24: "5X",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "Reserved",
    31: "Reserved",
    32: "Reserved",
}

#################################################
# QZSS
#################################################

QZSS_PRN_MAP = {}
for i in range(1, 11):
    QZSS_PRN_MAP[i] = f"{i+192:03d}"
for i in range(11, 65):
    QZSS_PRN_MAP[i] = "Reserved"

QZSS_SIG_MAP = {
    1: "Reserved",
    2: "1C",
    3: "Reserved",
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "Reserved",
    9: "6S",
    10: "6L",
    11: "6X",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "2S",
    16: "2L",
    17: "2X",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "5I",
    23: "5Q",
    24: "5X",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "1S",
    31: "1L",
    32: "1X",
}

#################################################
# BEIDOU
#################################################

BEIDOU_PRN_MAP = GPS_PRN_MAP

BEIDOU_SIG_MAP = {
    1: "Reserved",
    2: "2I",
    3: "2Q",
    4: "2X",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "6I",
    9: "6Q",
    10: "6X",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "7I",
    15: "7Q",
    16: "7X",
    17: "Reserved",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "5D",
    23: "5P",
    24: "5X",
    25: "7D",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "1D",
    31: "1P",
    32: "1X",
}

#################################################
# IRNSS
#################################################

IRNSS_PRN_MAP = {}
for i in range(1, 15):
    IRNSS_PRN_MAP[i] = f"{i:03d}"
for i in range(15, 65):
    IRNSS_PRN_MAP[i] = "Reserved"

IRNSS_SIG_MAP = {
    1: "Reserved",
    2: "Reserved",
    3: "Reserved",
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "Reserved",
    9: "Reserved",
    10: "Reserved",
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: "Reserved",
    16: "Reserved",
    17: "Reserved",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: "5A",
    23: "Reserved",
    24: "Reserved",
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: "Reserved",
    31: "Reserved",
    32: "Reserved",
}
