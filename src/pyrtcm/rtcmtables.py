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
    2: ("L1", "1C"),
    3: ("L1", "1P"),
    4: ("L1", "1W"),
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: ("L2", "2C"),
    9: ("L2", "2P"),
    10: ("L2", "2W"),
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: ("L2", "2S"),
    16: ("L2", "2L"),
    17: ("L2", "2X"),
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: ("L1", "1S"),
    31: ("L1", "1L"),
    32: ("L1", "1X"),
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
    2: ("G1", "1C"),
    3: ("G1", "1P"),
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: ("G2", "2C"),
    9: ("G2", "2P"),
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
    2: ("E1", "1C"),
    3: ("E1", "1A"),
    4: ("E1", "1B"),
    5: ("E1", "1X"),
    6: ("E1", "1Z"),
    7: "Reserved",
    8: ("E6", "6C"),
    9: ("E6", "6A"),
    10: ("E6", "6B"),
    11: ("E6", "6X"),
    12: ("E6", "6Z"),
    13: "Reserved",
    14: ("E5B", "7I"),
    15: ("E5B", "7Q"),
    16: ("E5B", "7X"),
    17: "Reserved",
    18: ("E5AB", "8I"),
    19: ("E5AB", "8Q"),
    20: ("E5AB", "8X"),
    21: "Reserved",
    22: ("E5A", "5I"),
    23: ("E5A", "5Q"),
    24: ("E5A", "5X"),
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
    2: ("L1", "1C"),
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
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
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
    2: ("L1", "1C"),
    3: "Reserved",
    4: "Reserved",
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: "Reserved",
    9: ("LEX", "6S"),
    10: ("LEX", "6L"),
    11: ("LEX", "6X"),
    12: "Reserved",
    13: "Reserved",
    14: "Reserved",
    15: ("L2", "2S"),
    16: ("L2", "2L"),
    17: ("L2", "2X"),
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
    25: "Reserved",
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: ("L1", "1S"),
    31: ("L1", "1L"),
    32: ("L1", "1X"),
}

#################################################
# BEIDOU
#################################################

BEIDOU_PRN_MAP = GPS_PRN_MAP

BEIDOU_SIG_MAP = {
    1: "Reserved",
    2: ("B1", "2I"),
    3: ("B1", "2Q"),
    4: ("B1", "2X"),
    5: "Reserved",
    6: "Reserved",
    7: "Reserved",
    8: ("B3", "6I"),
    9: ("B3", "6Q"),
    10: ("B3", "6X"),
    11: "Reserved",
    12: "Reserved",
    13: "Reserved",
    14: ("B2", "7I"),
    15: ("B2", "7Q"),
    16: ("B2", "7X"),
    17: "Reserved",
    18: "Reserved",
    19: "Reserved",
    20: "Reserved",
    21: "Reserved",
    22: ("B2A", "5D"),
    23: ("B2A", "5P"),
    24: ("B2A", "5X"),
    25: ("B2A", "7D"),
    26: "Reserved",
    27: "Reserved",
    28: "Reserved",
    29: "Reserved",
    30: ("B1C", "1D"),
    31: ("B1C", "1P"),
    32: ("B1C", "1X"),
}

#################################################
# IRNSS (NavIC)
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
    22: ("L5", "5A"),
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
