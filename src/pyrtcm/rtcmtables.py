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

GPS_SIG_MAP = {
    2: ("L1", "1C"),
    3: ("L1", "1P"),
    4: ("L1", "1W"),
    8: ("L2", "2C"),
    9: ("L2", "2P"),
    10: ("L2", "2W"),
    15: ("L2", "2S"),
    16: ("L2", "2L"),
    17: ("L2", "2X"),
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
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

GLONASS_SIG_MAP = {
    2: ("G1", "1C"),
    3: ("G1", "1P"),
    8: ("G2", "2C"),
    9: ("G2", "2P"),
}

#################################################
# GALILEO
#################################################

GALILEO_PRN_MAP = {}
for i in range(1, 51):
    GALILEO_PRN_MAP[i] = f"{i:03d}"
GALILEO_PRN_MAP[51] = "GIOVE-A"
GALILEO_PRN_MAP[52] = "GIOVE-B"

GALILEO_SIG_MAP = {
    2: ("E1", "1C"),
    3: ("E1", "1A"),
    4: ("E1", "1B"),
    5: ("E1", "1X"),
    6: ("E1", "1Z"),
    8: ("E6", "6C"),
    9: ("E6", "6A"),
    10: ("E6", "6B"),
    11: ("E6", "6X"),
    12: ("E6", "6Z"),
    14: ("E5B", "7I"),
    15: ("E5B", "7Q"),
    16: ("E5B", "7X"),
    18: ("E5AB", "8I"),
    19: ("E5AB", "8Q"),
    20: ("E5AB", "8X"),
    22: ("E5A", "5I"),
    23: ("E5A", "5Q"),
    24: ("E5A", "5X"),
}

#################################################
# SBAS
#################################################

SBAS_PRN_MAP = {}
for i in range(1, 40):
    SBAS_PRN_MAP[i] = f"{i+119:03d}"

SBAS_SIG_MAP = {
    2: ("L1", "1C"),
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
}

#################################################
# QZSS
#################################################

QZSS_PRN_MAP = {}
for i in range(1, 11):
    QZSS_PRN_MAP[i] = f"{i+192:03d}"

QZSS_SIG_MAP = {
    2: ("L1", "1C"),
    9: ("LEX", "6S"),
    10: ("LEX", "6L"),
    11: ("LEX", "6X"),
    15: ("L2", "2S"),
    16: ("L2", "2L"),
    17: ("L2", "2X"),
    22: ("L5", "5I"),
    23: ("L5", "5Q"),
    24: ("L5", "5X"),
    30: ("L1", "1S"),
    31: ("L1", "1L"),
    32: ("L1", "1X"),
}

#################################################
# BEIDOU
#################################################

BEIDOU_PRN_MAP = GPS_PRN_MAP

BEIDOU_SIG_MAP = {
    2: ("B1", "2I"),
    3: ("B1", "2Q"),
    4: ("B1", "2X"),
    8: ("B3", "6I"),
    9: ("B3", "6Q"),
    10: ("B3", "6X"),
    14: ("B2", "7I"),
    15: ("B2", "7Q"),
    16: ("B2", "7X"),
    22: ("B2A", "5D"),
    23: ("B2A", "5P"),
    24: ("B2A", "5X"),
    25: ("B2A", "7D"),
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

IRNSS_SIG_MAP = {
    22: ("L5", "5A"),
}

# {identity[0:3]: (prnmap, sigmap)}
PRNSIGMAP = {
    "107": (GPS_PRN_MAP, GPS_SIG_MAP),
    "108": (GLONASS_PRN_MAP, GLONASS_SIG_MAP),
    "109": (GALILEO_PRN_MAP, GALILEO_SIG_MAP),
    "110": (SBAS_PRN_MAP, SBAS_SIG_MAP),
    "111": (QZSS_PRN_MAP, QZSS_SIG_MAP),
    "112": (BEIDOU_PRN_MAP, BEIDOU_SIG_MAP),
    "113": (IRNSS_PRN_MAP, IRNSS_SIG_MAP),
}
