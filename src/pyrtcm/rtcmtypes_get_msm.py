"""
RTCM Protocol MSM payload definitions

Information sourced from RTCM STANDARD 10403.3 © 2016 RTCM

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyrtcm.rtcmtypes_core import NCELL, NSAT

# *************************************************************
# MSM MESSAGE SUB-SECTION DEFINITIONS
# *************************************************************
MSM_HDR1 = {
    "DF002": "Message number",
    "DF003": "Reference station ID",
}

MSM_HDR2 = {
    "DF393": "Multiple Message Bit",
    "DF409": "IODS - Issue of Data Station",
    "DF001_7": "Reserved",
    "DF411": "Clock Steering Indicator",
    "DF412": "External Clock Indicator",
    "DF417": "GNSS Divergence-free Smoothing Indicator",
    "DF418": "GNSS Smoothing Interval",
    "DF394": "GNSS Satellite Mask",  # NSAT = num of set bits
    "DF395": "GNSS Signal Mask",  # NSIG = num of set bits
    "DF396": "GNSS Cell Mask",  # size = NSAT * NSIG; NCELL = num of set bits
}

MSM_SAT_123 = {
    "groupsat0": (
        NSAT,
        {
            "PRN": "GNSS Satellite PRN",  # derived by pyspartn
        },
    ),
    "groupsat1": (
        NSAT,
        {
            "DF398": "GNSS Satellite rough ranges modulo 1 millisecond",
        },
    ),
}

MSM_SAT_46 = {
    "groupsat0": (
        NSAT,
        {
            "PRN": "GNSS Satellite PRN",  # derived by pyspartn
        },
    ),
    "groupsat1": (
        NSAT,
        {
            "DF397": "Number of int millisecs in GNSS Satellite roughranges",
        },
    ),
    "groupsat2": (
        NSAT,
        {
            "DF398": "GNSS Satellite rough ranges modulo 1 millisecond",
        },
    ),
}


MSM_SAT_57 = {
    "groupsat0": (
        NSAT,
        {
            "PRN": "GNSS Satellite PRN",  # derived by pyspartn
        },
    ),
    "groupsat1": (
        NSAT,
        {
            "DF397": "The number of integer milliseconds in GNSS Satellite rough ranges",
        },
    ),
    "groupsat2": (
        NSAT,
        {
            "ExtSatInfo": "Extended Satellite Information",  # Reserved for future use
        },
    ),
    "groupsat3": (
        NSAT,
        {
            "DF398": "GNSS Satellite rough ranges modulo 1 millisecond",
        },
    ),
    "groupsat4": (
        NSAT,
        {
            "DF399": "GNSS Satellite rough PhaseRangeRates",
        },
    ),
}

MSM_SAT_57_GLONASS = {
    "groupsat0": (
        NSAT,
        {
            "PRN": "GNSS Satellite PRN",  # derived by pyspartn
        },
    ),
    "groupsat1": (
        NSAT,
        {
            "DF397": "The number of integer milliseconds in GNSS Satellite rough ranges",
        },
    ),
    "groupsat2": (
        NSAT,
        {
            "DF419": "Satellite Frequency Channel Number",
        },
    ),
    "groupsat3": (
        NSAT,
        {
            "DF398": "GNSS Satellite rough ranges modulo 1 millisecond",
        },
    ),
    "groupsat4": (
        NSAT,
        {
            "DF399": "GNSS Satellite rough PhaseRangeRates",
        },
    ),
}

MSM_SIG_1 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF400": "GNSS signal fine Pseudoranges",
        },
    ),
}

MSM_SIG_2 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF401": "GNSS signal fine PhaseRange data",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF402": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF420",
            "Half-cycle ambiguity indicator",
        },
    ),
}

MSM_SIG_3 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF400": "GNSS signal fine Pseudoranges",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF401": "GNSS signal fine PhaseRange data",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF402": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig4": (
        NCELL,
        {
            "DF420": "Half-cycle ambiguity indicator",
        },
    ),
}

MSM_SIG_4 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF400": "GNSS signal fine Pseudoranges",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF401": "GNSS signal fine PhaseRange data",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF402": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig4": (
        NCELL,
        {
            "DF420": "Half-cycle ambiguity indicator",
        },
    ),
    "groupsig5": (
        NCELL,
        {
            "DF403": "GNSS signal CNRs",
        },
    ),
}

MSM_SIG_5 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF400": "GNSS signal fine Pseudoranges",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF401": "GNSS signal fine PhaseRange data",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF402": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig4": (
        NCELL,
        {
            "DF420": "Half-cycle ambiguity indicator",
        },
    ),
    "groupsig5": (
        NCELL,
        {
            "DF403": "GNSS signal CNRs",
        },
    ),
    "groupsig6": (
        NCELL,
        {
            "DF404": "GNSS signal fine PhaseRangeRates",
        },
    ),
}

MSM_SIG_6 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF405": "GNSS signal fine",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF406": "GNSS signal fine PhaseRange data with extended resolution",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF407": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig4": (
        NCELL,
        {
            "DF420": "Half-cycle ambiguity indicator",
        },
    ),
    "groupsig5": (
        NCELL,
        {
            "DF408": "GNSS signal CNRs with extended resolution",
        },
    ),
}

MSM_SIG_7 = {
    "groupsig0": (
        NCELL,
        {
            "CELLPRN": "GNSS Satellite PRN ",  # derived by pyspartn
            "CELLSIG": "GNSS Satellite Signal ID",  # derived by pyspartn
        },
    ),
    "groupsig1": (
        NCELL,
        {
            "DF405": "GNSS signal fine",
        },
    ),
    "groupsig2": (
        NCELL,
        {
            "DF406": "GNSS signal fine PhaseRange data with extended resolution",
        },
    ),
    "groupsig3": (
        NCELL,
        {
            "DF407": "GNSS PhaseRange Lock",
        },
    ),
    "groupsig4": (
        NCELL,
        {
            "DF420": "Half-cycle ambiguity indicator",
        },
    ),
    "groupsig5": (
        NCELL,
        {
            "DF408": "GNSS signal CNRs with extended resolution",
        },
    ),
    "groupsig6": (
        NCELL,
        {
            "DF404": "GNSS signal fine PhaseRangeRates",
        },
    ),
}

# *************************************************************
# RTCM3 MSM MESSAGE PAYLOAD DEFINITIONS
# *************************************************************
RTCM_PAYLOADS_GET_MSM = {
    # concatenate MSM sections in to a single dict
    # NB: Python >=3.9 supports the more intuitive | (union)
    # operation for this, but earlier versions don't.
    # GPS
    "1071": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1072": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1073": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1074": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1075": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1076": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1077": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
    # GLONASS
    "1081": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1082": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1083": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1084": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1085": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_57_GLONASS,
        **MSM_SIG_5,
    },
    "1086": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1087": {
        **MSM_HDR1,
        "DF416": "GLONASS Day Of Week",
        "DF034": "GLONASS Epoch Time (tk)",
        **MSM_HDR2,
        **MSM_SAT_57_GLONASS,
        **MSM_SIG_7,
    },
    # Galileo
    "1091": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1092": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1093": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1094": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1095": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1096": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1097": {
        **MSM_HDR1,
        "DF248": "Galileo Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
    # SBAS
    "1101": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1102": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1103": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1104": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1105": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1106": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1107": {
        **MSM_HDR1,
        "DF004": "GPS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
    # QZSS
    "1111": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1112": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1113": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1114": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1115": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1116": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1117": {
        **MSM_HDR1,
        "DF428": "QZSS Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
    # BeiDou
    "1121": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1122": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1123": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1124": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1125": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1126": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1127": {
        **MSM_HDR1,
        "DF427": "BeuDou Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
    # IRNSS (NavIC)
    "1131": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_1,
    },
    "1132": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_2,
    },
    "1133": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_123,
        **MSM_SIG_3,
    },
    "1134": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_4,
    },
    "1135": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_5,
    },
    "1136": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_46,
        **MSM_SIG_6,
    },
    "1137": {
        **MSM_HDR1,
        "DF546": "NavIC Epoch Time (TOW)",
        **MSM_HDR2,
        **MSM_SAT_57,
        **MSM_SIG_7,
    },
}
