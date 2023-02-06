"""
RTCM Protocol payload definitions

Created on 14 Feb 2022

Information sourced from RTCM STANDARD 10403.3 © 2016 RTCM

:author: semuadmin
"""
# pylint: disable=too-many-lines, line-too-long


# attribute names holding size of MSM repeating groups
NSAT = "NSat"
NSIG = "NSig"
NCELL = "_NCell"
NBIAS = "_NBias"
# Number of Residuals groups in MT1023 and MT1024
NRES = 16

# *************************************************************
# MSM MESSAGE SUB-SECTION DEFINITIONS
# *************************************************************
MSM_HDR = {
    "DF002": "Message number",
    "DF003": "Reference station ID",
    "GNSSEpoch": "GNSS Epoch Time",
    "DF393": "Multiple Message Bit",
    "DF409": "IODS - Issue of Data Station",
    "DF001_7": "Reserved",
    "DF411": "Clock Steering Indicator",
    "DF412": "External Clock Indicator",
    "DF417": "GNSS Divergence-free Smoothing Indicator",
    "DF418": "GNSS Smoothing Interval",
    "DF394": "GNSS Satellite Mask",  # NSAT = num of set bits
    "DF395": "GNSS Signal Mask",  # NSIG = num of set bits
    "DF396": "GNSS Cell Mask",  # size = NCELL = NSAT * NSIG
}

MSM_SAT_123 = {
    "groupsat1": (
        NSAT,
        {
            "DF398": "GNSS Satellite rough ranges modulo 1 millisecond",
        },
    ),
}

MSM_SAT_46 = {
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
    "groupsat1": (
        NSAT,
        {
            "DF397": "The number of integer milliseconds in GNSS Satellite rough ranges",
        },
    ),
    "groupsat2": (
        NSAT,
        {
            "GNSSSpecific": "Extended Satellite Information",
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
    "groupsig1": (
        NCELL,
        {
            "DF400": "GNSS signal fine Pseudoranges",
        },
    ),
}

MSM_SIG_2 = {
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

# concatenate MSM sections in to a single dict
# NB: Python >=3.9 supports the more intuitive | (union)
# operation for this, but earlier versions don't.
MSM1 = {**MSM_HDR, **MSM_SAT_123, **MSM_SIG_1}
MSM2 = {**MSM_HDR, **MSM_SAT_123, **MSM_SIG_2}
MSM3 = {**MSM_HDR, **MSM_SAT_123, **MSM_SIG_3}
MSM4 = {**MSM_HDR, **MSM_SAT_46, **MSM_SIG_4}
MSM5 = {**MSM_HDR, **MSM_SAT_57, **MSM_SIG_5}
MSM6 = {**MSM_HDR, **MSM_SAT_46, **MSM_SIG_6}
MSM7 = {**MSM_HDR, **MSM_SAT_57, **MSM_SIG_7}
# *************************************************************

# *************************************************************
# RTCM3 MESSAGE GROUP HEADER DEFINITIONS
# *************************************************************
HDR_1001_1004 = {
    "DF002": "Message Number",
    "DF003": "Reference Station ID",
    "DF004": "GPS Epoch Time (TOW)",
    "DF005": "Synchronous GNSS Flag",
    "DF006": "No. of GPS Satellite Signals Processed",
    "DF007": "GPS Divergence-free Smoothing Indicator",
    "DF008": "GPS Smoothing Interval",
}

HDR_1005_1006 = {
    "DF002": "Message Number",
    "DF003": "Reference Station ID",
    "DF021": "Reserved for ITRF Realization Year",
    "DF022": "GPS Indicator",
    "DF023": "GLONASS Indicator",
    "DF024": "Reserved for Galileo Indicator",
    "DF141": "Reference-Station Indicator",
    "DF025": "Antenna Reference Point ECEF-X",
    "DF142": "Single Receiver Oscillator Indicator",
    "DF001_1": "Reserved",
    "DF026": "Antenna Reference Point ECEF-Y",
    "DF364": "Quarter Cycle Indicator",
    "DF027": "Antenna Reference Point ECEF-Z",
}

HDR_1009_1012 = {
    "DF002": "Message Number",
    "DF003": "Reference Station ID",
    "DF034": "GLONASS Epoch Time (tk)",
    "DF005": "Synchronous GNSS Flag",
    "DF035": "No. of GLONASS Satellite Signals Processed",
    "DF036": "GLONASS Divergence-free Smoothing Indicator",
    "DF037": "GLONASS Smoothing Interval",
}

HDR_1015_1017 = {
    "DF002": "Message Number",
    "DF059": "Network ID",
    "DF072": "Subnetwork ID",
    "DF065": "GPS Epoch Time (GPS TOW)",
    "DF066": "GPS Multiple Message Indicator",
    "DF060": "Master Reference Station ID",
    "DF061": "Auxiliary Reference Station ID",
    "DF067": "# of GPS Sats",
}

HDR_1037_1039 = {
    "DF002": "Message Number",
    "DF059": "Network ID",
    "DF072": "Subnetwork ID",
    "DF233": "GLONASS Network Epoch Time",
    "DF066": "Multiple Message Indicator",
    "DF060": "Master Reference Station ID",
    "DF061": "Auxiliary Reference Station ID",
    "DF234": "# of GLONASS Data Entries",
}

# *************************************************************
# RTCM3 MESSAGE PAYLOAD DEFINITIONS
# *************************************************************
RTCM_PAYLOADS_GET = {
    "1001": {
        **HDR_1001_1004,
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF010": "GPS L1 Code Indicator",
                "DF011": "GPS L1 Pseudorange",
                "DF012": "GPS L1 PhaseRange - L1 Pseudorange",
                "DF013": "GPS L1 Lock time Indicator",
            },
        ),
    },
    "1002": {
        **HDR_1001_1004,
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF010": "GPS L1 Code Indicator",
                "DF011": "GPS L1 Pseudorange",
                "DF012": "GPS L1 PhaseRange - L1 Pseudorange",
                "DF013": "GPS L1 Lock time Indicator",
                "DF014": "GPS Integer L1 Pseudorange Modulus Ambiguity",
                "DF015": "GPS L1 CNR",
            },
        ),
    },
    "1003": {
        **HDR_1001_1004,
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF010": "GPS L1 Code Indicator",
                "DF011": "GPS L1 Pseudorange",
                "DF012": "GPS L1 PhaseRange - L1 Pseudorange",
                "DF013": "GPS L1 Lock time Indicator",
                "DF016": "GPS L2 Code Indicator",
                "DF017": "GPS L2-L1 Pseudorange Difference",
                "DF018": "GPS L2 PhaseRange - L1 Pseudorange",
                "DF019": "GPS L2 Lock time Indicator",
            },
        ),
    },
    "1004": {
        **HDR_1001_1004,
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF010": "GPS L1 Code Indicator",
                "DF011": "GPS L1 Pseudorange",
                "DF012": "GPS L1 PhaseRange - L1 Pseudorange",
                "DF013": "GPS L1 Lock time Indicator",
                "DF014": "GPS Integer L1 Pseudorange Modulus Ambiguity",
                "DF015": "GPS L1 CNR",
                "DF016": "GPS L2 Code Indicator",
                "DF017": "GPS L2-L1 Pseudorange Difference",
                "DF018": "GPS L2 PhaseRange - L1 Pseudorange",
                "DF019": "GPS L2 Lock time Indicator",
                "DF020": "GPS L2 CNR",
            },
        ),
    },
    "1005": HDR_1005_1006,
    "1006": {**HDR_1005_1006, "DF028": "Antenna Height"},
    "1007": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF029": "Descriptor Counter N",
        "group": (
            "DF029",
            {
                "DF030": "Antenna Descriptor",
            },
        ),
        "DF031": "Antenna Setup ID",
    },
    "1008": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF029": "Descriptor Counter N",
        "group1": (
            "DF029",
            {
                "DF030": "Antenna Descriptor",
            },
        ),
        "DF031": "Antenna Setup ID",
        "DF032": "Serial Number Counter M",
        "group2": (
            "DF032",
            {
                "DF033": "Antenna Serial Number",
            },
        ),
    },
    "1009": {
        **HDR_1009_1012,
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF039": "GLONASS Code Indicator",
                "DF040": "GLONASS Satellite Frequency Channel Number",
                "DF041": "GLONASS L1 Pseudorange",
                "DF042": "GLONASS L1 PhaseRange - L1 Pseudorange",
                "DF043": "GLONASS L1 Lock time Indicator",
            },
        ),
    },
    "1010": {
        **HDR_1009_1012,
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF039": "GLONASS L1 Code Indicator",
                "DF040": "GLONASS Satellite Frequency Channel Number",
                "DF041": "GLONASS L1 Pseudorange",
                "DF042": "GLONASS L1 PhaseRange - L1 Pseudorange",
                "DF043": "GLONASS L1 Lock time Indicator",
                "DF044": "GLONASS Integer L1 Pseudorange Modulus Ambiguity",
                "DF045": "GLONASS L1 CNR",
            },
        ),
    },
    "1011": {
        **HDR_1009_1012,
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF039": "GLONASS L1 Code Indicator",
                "DF040": "GLONASS Satellite Frequency Channel Number",
                "DF041": "GLONASS L1 Pseudorange",
                "DF042": "GLONASS L1 PhaseRange - L1 Pseudorange",
                "DF043": "GLONASS L1 Lock time Indicator",
                "DF046": "GLONASS L2 Code Indicator",
                "DF047": "GLONASS L2-L1 Pseudorange Difference",
                "DF048": "GLONASS L2 PhaseRange - L1 Pseudorange",
                "DF049": "GLONASS L2 Lock time Indicator",
            },
        ),
    },
    "1012": {
        **HDR_1009_1012,
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF039": "GLONASS L1 Code Indicator",
                "DF040": "GLONASS Satellite Frequency Channel Number",
                "DF041": "GLONASS L1 Pseudorange",
                "DF042": "GLONASS L1 PhaseRange - L1 Pseudorange",
                "DF043": "GLONASS L1 Lock time Indicator",
                "DF044": "GLONASS Integer L1 Pseudorange Modulus Ambiguity",
                "DF045": "GLONASS L1 CNR",
                "DF046": "GLONASS L2 Code Indicator",
                "DF047": "GLONASS L2-L1 Pseudorange Difference",
                "DF048": "GLONASS L2 PhaseRange - L1 Pseudorange",
                "DF049": "GLONASS L2 Lock time Indicator",
                "DF050": "GLONASS L2 CNR",
            },
        ),
    },
    "1013": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF051": "Modified Julian Day (MJD) Number",
        "DF052": "Seconds of Day (UTC)",
        "DF053": "No. of Message ID Announcements to Follow (Nm)",
        "DF054": "Leap Seconds, GPS-UTC",
        "group": (
            "DF053",
            {
                "DF055": "Message ID",
                "DF056": "Message Sync Flag",
                "DF057": "Message Transmission Interval",
            },
        ),
    },
    "1014": {
        "DF002": "Message Number",
        "DF059": "Network ID",
        "DF072": "Subnetwork ID",
        "DF058": "Number of Auxiliary Stations Transmitted",
        "DF060": "Master Reference Station ID",
        "DF061": "Auxiliary Reference Station ID",
        "DF062": "Aux-Master Delta Latitude",
        "DF063": "Aux-Master Delta Longitude",
        "DF064": "Aux-Master Delta Height",
    },
    "1015": {
        **HDR_1015_1017,
        "group": (
            "DF067",
            {
                "DF068": "GPS Satellite ID",
                "DF074": "GPS Ambiguity Status Flag",
                "DF075": "GPS Non Sync Count",
                "DF069": "GPS Ionospheric Carrier Phase Correction Difference",
            },
        ),
    },
    "1016": {
        **HDR_1015_1017,
        "group": (
            "DF067",
            {
                "DF068": "GPS Satellite ID",
                "DF074": "GPS Ambiguity Status Flag",
                "DF075": "GPS Non Sync Count",
                "DF070": "GPS Geometric Carrier Phase Correction Difference",
                "DF071": "GPS IODE",
            },
        ),
    },
    "1017": {
        **HDR_1015_1017,
        "group": (
            "DF067",
            {
                "DF068": "GPS Satellite ID",
                "DF074": "GPS Ambiguity Status Flag",
                "DF075": "GPS Non Sync Count",
                "DF070": "GPS Geometric Carrier Phase Correction Difference",
                "DF071": "GPS IODE",
                "DF069": "GPS Ionospheric Carrier Phase Correction Difference",
            },
        ),
    },
    # "1018": {RESERVED for Alt Ionospheric Correction Diff Msg},
    "1019": {
        "DF002": "Message Number",
        "DF009": "GPS Satellite ID",
        "DF076": "GPS Week Number",
        "DF077": "GPS SV ACCURACY",
        "DF078": "GPS CODE ON L2",
        "DF079": "GPS IDOT",
        "DF071": "GPS IODE ",
        "DF081": "GPS toc",
        "DF082": "GPS af2",
        "DF083": "GPS af1",
        "DF084": "GPS af0",
        "DF085": "GPS IODC",
        "DF086": "GPS Crs",
        "DF087": "GPS ∆n",
        "DF088": "GPS M0",
        "DF089": "GPS Cuc",
        "DF090": "GPS e (Eccentricity)",
        "DF091": "GPS Cus",
        "DF092": "GPS A½",
        "DF093": "GPS toe",
        "DF094": "GPS Cic",
        "DF095": "GPS Ω0",
        "DF096": "GPS Cis",
        "DF097": "GPS i0",
        "DF098": "GPS Crc",
        "DF099": "GPS ω (Argument of Perigee)",
        "DF100": "GPS ΩDOT (Rate of Right Ascension)",
        "DF101": "GPS tGD",
        "DF102": "GPS SV HEALTH",
        "DF103": "GPS L2 P data flag",
        "DF137": "GPS Fit Interval",
    },
    "1020": {
        "DF002": "Message Number",
        "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
        "DF040": "GLONASS Satellite Frequency Channel Number",
        "DF104": "GLONASS almanac health (Cn word)",
        "DF105": "GLONASS almanac health availability indicator",
        "DF106": "GLONASS P1",
        "DF107": "GLONASS tk",
        "DF108": "GLONASS MSB of Bn word",
        "DF109": "GLONASS P2",
        "DF110": "GLONASS tb",
        "DF111": "GLONASS xn(tb), first derivative",
        "DF112": "GLONASS xn(tb)",
        "DF113": "GLONASS xn(tb), second derivative",
        "DF114": "GLONASS yn(tb), first derivative",
        "DF115": "GLONASS yn(tb)",
        "DF116": "GLONASS yn(tb), second derivative",
        "DF117": "GLONASS zn(tb), first derivative",
        "DF118": "GLONASS zn(tb)",
        "DF119": "GLONASS zn(tb), second derivative",
        "DF120": "GLONASS P3",
        "DF121": "GLONASS γn(tb)",
        "DF122": "GLONASS-M P",
        "DF123": "GLONASS-M ln (third string)",
        "DF124": "GLONASS τn(tb)",
        "DF125": "GLONASS-M Δτn",
        "DF126": "GLONASS En",
        "DF127": "GLONASS-M P4",
        "DF128": "GLONASS-M FT",
        "DF129": "GLONASS-M NT",
        "DF130": "GLONASS-M M",
        "DF131": "GLONASS The Availability of Additional Data",
        "DF132": "GLONASS NA",
        "DF133": "GLONASS τc",
        "DF134": "GLONASS-M N4",
        "DF135": "GLONASS-M τGPS",
        "DF136": "GLONASS-M ln (fifth string)",
        "DF001_7": "Reserved",
    },
    "1021": {
        "DF002": "Message Number",
        "DF143": "Source-Name Counter",
        "group1": (
            "DF143",
            {
                "DF144": "Source-Name",
            },
        ),
        "DF145": "Target-Name Counter",
        "group2": (
            "DF145",
            {
                "DF146": "Target-Name",
            },
        ),
        "DF147": "System Identification Number",
        "DF148": "Utilized Transformation Message Indicator",
        "DF149": "Plate Number",
        "DF150": "Computation Indicator",
        "DF151": "Height Indicator",
        "DF152": "ΦV - Latitude of Origin, Area of Validity",
        "DF153": "ΛV - Longitude of Origin, Area of Validity",
        "DF154": "∆φV - N/S Extension, Area of Validity",
        "DF155": "∆λV - E/W Extension, Area of Validity",
        "DF156": "dX - Translation in X-direction",
        "DF157": "dY - Translation in Y-direction",
        "DF158": "dZ - Translation in Z-direction",
        "DF159": "R1 - Rotation Around the X-axis",
        "DF160": "R2 - Rotation Around the Y-axis",
        "DF161": "R3 - Rotation Around the Z-axis",
        "DF162": "dS - Scale Correction",
        "DF166": "add aS - Semi-major Axis of Source System Ellipsoid",
        "DF167": "add bS - Semi-minor Axis of Source System Ellipsoid",
        "DF168": "add aT - Semi-major Axis of Target System Ellipsoid",
        "DF169": "add bT - Semi-minor Axis of Target System Ellipsoid",
        "DF214": "Horizontal Helmert/Molodenski Quality Indicator",
        "DF215": "Vertical Helmert/Molodenski Quality Indicator",
    },
    "1022": {
        "DF002": "Message Number",
        "DF143": "Source-Name Counter",
        "group1": (
            "DF143",
            {
                "DF144": "Source-Name",
            },
        ),
        "DF145": "Target-Name Counter",
        "group2": (
            "DF145",
            {
                "DF146": "Target-Name",
            },
        ),
        "DF147": "System Identification Number",
        "DF148": "Utilized Transformation Message Indicator",
        "DF149": "Plate Number",
        "DF150": "Computation Indicator",
        "DF151": "Height Indicator",
        "DF152": "ΦV - Latitude of Origin, Area of Validity",
        "DF153": "ΛV - Longitude of Origin, Area of Validity",
        "DF154": "∆φV - N/S Extension, Area of Validity",
        "DF155": "∆λV - E/W Extension, Area of Validity",
        "DF156": "dX - Translation in X-direction",
        "DF157": "dY - Translation in Y-direction",
        "DF158": "dZ - Translation in Z-direction",
        "DF159": "R1 - Rotation Around the X-axis",
        "DF160": "R2 - Rotation Around the Y-axis",
        "DF161": "R3 - Rotation Around the Z-axis",
        "DF162": "dS - Scale Correction",
        "DF163": "XP  - X Coordinate for M-B Rotation Point",
        "DF164": "YP  - Y Coordinate for M-B Rotation Point",
        "DF165": "ZP  - Z Coordinate for M-B Rotation Point",
        "DF166": "add aS - Semi-major Axis of Source System Ellipsoid",
        "DF167": "add bS - Semi-minor Axis of Source System Ellipsoid",
        "DF168": "add aT - Semi-major Axis of Target System Ellipsoid",
        "DF169": "add bT - Semi-minor Axis of Target System Ellipsoid",
        "DF214": "Horizontal Helmert/Molodenski Quality Indicator",
        "DF215": "Vertical Helmert/Molodenski Quality Indicator",
    },
    "1023": {
        "DF002": "Message Number",
        "DF147": "System Identification Number",
        "DF190": "Horizontal Shift Indicator",
        "DF191": "Vertical Shift Indicator",
        "DF192": "φ0 - Latitude of Origin of Grids",
        "DF193": "λ0 - Longitude of Origin of Grids",
        "DF194": "∆φ - N/S Grid Area Extension",
        "DF195": "∆λ - E/W Grid Area Extension",
        "DF196": "Mean ∆φ - Mean Latitude Offset",
        "DF197": "Mean ∆λ - Mean Longitude Offset",
        "DF198": "Mean ∆H - Mean Height Offset",
        "group1": (
            NRES,
            {
                "DF199": "δφi - Latitude Residual",
                "DF200": "δλi - Longitude Residual",
                "DF201": "δhi - Height Residual",
            },
        ),
        "DF212": "Horizontal Interpolation Method Indicator",
        "DF213": "Vertical Interpolation Method Indicator",
        "DF216": "Horizontal Grid Quality Indicator",
        "DF217": "Vertical Grid Quality Indicator",
        "DF051": "Modified Julian Day (MJD) Number",
    },
    "1024": {
        "DF002": "Message Number",
        "DF147": "System Identification Number",
        "DF190": "Horizontal Shift Indicator",
        "DF191": "Vertical Shift Indicator",
        "DF202": "N0 - Northing of Origin",
        "DF203": "E0 - Easting of Origin",
        "DF204": "∆N - N/S Grid Area Extension",
        "DF205": "∆E - E/W Grid Area Extension",
        "DF206": "Mean ∆N - Mean Local Northing Offset",
        "DF207": "Mean ∆E - Mean Local Easting Offset",
        "DF208": "Mean ∆h - Mean Local Height Offset",
        "group1": (
            NRES,
            {
                "DF209": "δNi - Residual in Local Northing",
                "DF210": "δEi - Residual in Local Easting",
                "DF211": "δhi - Residual in Local Height",
            },
        ),
        "DF212": "Horizontal Interpolation Method Indicator",
        "DF213": "Vertical Interpolation Method Indicator",
        "DF216": "Horizontal Grid Quality Indicator",
        "DF217": "Vertical Grid Quality Indicator",
        "DF051": "Modified Julian Day (MJD) Number",
    },
    "1025": {
        "DF002": "Message Number",
        "DF147": "System Identification Number",
        "DF170": "Projection Type",
        "DF171": "LaNO - Latitude of Natural Origin",
        "DF172": "LoNO - Longitude of Natural Origin",
        "DF173": "add SNO - Scale Factor at Natural Origin",
        "DF174": "FE - False Easting",
        "DF175": "FN - False Northing",
    },
    "1026": {
        "DF002": "Message Number",
        "DF147": "System Identification Number",
        "DF170": "Projection Type",
        "DF176": "LaFO - Latitude of False Origin",
        "DF177": "LoFO - Longitude of False Origin",
        "DF178": "LaSP1 - Latitude of Standard Parallel No. 1",
        "DF179": "LaSP2 - Latitude of Standard Parallel No. 2",
        "DF180": "EFO - Easting of False Origin",
        "DF181": "NFO - Northing of False Origin",
    },
    "1027": {
        "DF002": "Message Number",
        "DF147": "System Identification Number",
        "DF170": "Projection Type",
        "DF182": "Rectification Flag",
        "DF183": "LaPC - Latitude of Projection Center",
        "DF184": "LoPC - Longitude of Projection Center",
        "DF185": "AzIL - Azimuth of Initial Line",
        "DF186": "Diff ARSG - Difference, Angle from Rectified to Skew Grid",
        "DF187": "Add SIL - Scale factor on Initial Line",
        "DF188": "EPC - Easting at Projection Center",
        "DF189": "NPC - Northing at Projection Center",
    },
    # "1028": {RESERVED for Global Plate-Fixed XFormation},
    "1029": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF051": "Modified Julian Day (MJD) Number",
        "DF052": "Seconds of Day (UTC)",
        "DF138": "Number of Characters to Follow",
        "DF139": "Number of UTF-8 Code Units (N)",
        "group": (
            "DF139",
            {
                "DF140": "UTF-8 Character Code Units",
            },
        ),
    },
    "1030": {
        "DF002": "Message Number",
        "DF224": "GPS Residuals Epoch Time (TOW)",
        "DF003": "Reference Station ID",
        "DF223": "N-Refs",
        "DF006": "GPS Number of Satellite Signals Processed",
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF218": "soc",
                "DF219": "sod",
                "DF220": "soh",
                "DF221": "sIc",
                "DF222": "sId",
            },
        ),
    },
    "1031": {
        "DF002": "Message Number",
        "DF225": "GLONASS Residuals Epoch Time (tk)",
        "DF003": "Reference Station ID",
        "DF223": "N-Refs",
        "DF035": "GLONASS Number of Satellite Signals Processed",
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID",
                "DF218": "soc",
                "DF219": "sod",
                "DF220": "soh",
                "DF221": "sIc",
                "DF222": "sId",
            },
        ),
    },
    "1032": {
        "DF002": "Message Number",
        "DF003": "Non-Physical Reference Station ID",
        "DF226": "Physical Reference Station ID",
        "DF021": "ITRF Epoch Year",
        "DF025": "Physical reference station ARP ECEF-X",
        "DF026": "Physical reference station ARP ECEF-Y",
        "DF027": "Physical reference station ARP ECEF-Z",
    },
    "1033": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF029": "Antenna Descriptor Counter N",
        "group1": (
            "DF029",
            {
                "DF030": "Antenna Descriptor",
                "DF031": "Antenna Setup ID",
            },
        ),
        "DF032": "Antenna Serial Number Counter M",
        "group2": (
            "DF032",
            {
                "DF033": "Antenna Serial Number",
            },
        ),
        "DF227": "Receiver Type Descriptor Counter I",
        "group3": (
            "DF227",
            {
                "DF228": "Receiver Type Descriptor",
            },
        ),
        "DF229": "Receiver Firmware Version Counter J",
        "group4": (
            "DF229",
            {
                "DF230": "Receiver Firmware Version",
            },
        ),
        "DF231": "Receiver Serial Number Counter K",
        "group5": (
            "DF231",
            {
                "DF232": "Receiver Serial Number",
            },
        ),
    },
    "1034": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF240": "GPS FKP Epoch Time (TOW)",
        "DF006": "No. of GPS Satellite Signals Processed",
        "group": (
            "DF006",
            {
                "DF009": "GPS Satellite ID",
                "DF071": "GPS Issue of data ephemeris (IODE)",
                "DF242": "N0: Geometric gradient (North)",
                "DF243": "E0: Geometric gradient (East)",
                "DF244": "NI: Ionospheric gradient (North)",
                "DF245": "EI: Ionospheric gradient (East)",
            },
        ),
    },
    "1035": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF241": "GLONASS FKP Epoch Time",
        "DF035": "No. of GLONASS Satellite Signals Processed",
        "group": (
            "DF035",
            {
                "DF038": "GLONASS Satellite ID",
                "DF392": "GLONASS Issue Of Data (IOD)",
                "DF242": "N0: Geometric gradient (North)",
                "DF243": "E0: Geometric gradient (East)",
                "DF244": "NI: Ionospheric gradient (North)",
                "DF245": "EI: Ionospheric gradient (East)",
            },
        ),
    },
    # "1036": {Not Used},
    "1037": {
        **HDR_1037_1039,
        "group": (
            "DF234",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF235": "GLONASS Ambiguity Status Flag",
                "DF236": "GLONASS Non Sync Count",
                "DF237": "GLONASS Ionospheric Carrier Phase Correction Difference",
            },
        ),
    },
    "1038": {
        **HDR_1037_1039,
        "group": (
            "DF234",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF235": "GLONASS Ambiguity Status Flag",
                "DF236": "GLONASS Non Sync Count",
                "DF238": "GLONASS Geometric Carrier Phase Correction Difference",
                "DF239": "GLONASS IOD",
            },
        ),
    },
    "1039": {
        **HDR_1037_1039,
        "group": (
            "DF234",
            {
                "DF038": "GLONASS Satellite ID (Satellite Slot Number)",
                "DF235": "GLONASS Ambiguity Status Flag",
                "DF236": "GLONASS Non Sync Count",
                "DF238": "GLONASS Geometric Carrier Phase Correction Difference",
                "DF239": "GLONASS IOD",
                "DF237": "GLONASS Ionospheric Carrier Phase Correction Difference",
            },
        ),
    },
    "1041": {
        "DF002": "Message Number",
        "DF516": "NavIC/IRNSS Satellide ID",
        "DF517": "Week Number (WN)",
        "DF518": "Clock bias (af0)",
        "DF519": "Clock drift (af1",
        "DF520": "Clock drift rate (af2)",
        "DF521": "SV Accuracy (URA)",
        "DF522": "Time of clock (toc)",
        "DF523": "Total Group Delay (TGD)",
        "DF524": "Mean Motion Difference (∆n)",
        "DF525": "Issue of Data Ephemeris & Clock (IODEC)",
        "DF526": "Reserved bits after IODEC",
        "DF527": "L5 Flag",
        "DF528": "S Flag",
        "DF529": "Cuc",
        "DF530": "Cus",
        "DF531": "Cic",
        "DF532": "Cis",
        "DF533": "Crc",
        "DF534": "Crs",
        "DF535": "Rate of Inclination angle (IDOT)",
        "DF536": "Mean Anomaly (M0)",
        "DF537": "Time of ephemeris (tOE)",
        "DF538": "Eccentricity (e)",
        "DF539": "Square root of Semi major axis (√A)",
        "DF540": "Long of Ascending Node (Ω0)",
        "DF541": "Argument of perigee (ω)",
        "DF542": "Rate of RAAN (ΩDOT)",
        "DF543": "Inclination (i0)",
        "DF544": "2 spare bits after IDOT",
        "DF545": "2 spare bits after i0",
    },
    "1042": {
        "DF002": "Message Number",
        "DF488": "BDS Satellite ID",
        "DF489": "BDS Week Number",
        "DF490": "BDS URAI",
        "DF491": "BDS IDOT",
        "DF492": "BDS AODE",
        "DF493": "BDS Toc",
        "DF494": "BDS a2",
        "DF495": "BDS a1",
        "DF496": "BSD a0",
        "DF497": "BDS AODC",
        "DF498": "BDS Crs",
        "DF499": "BDS ∆n",
        "DF500": "BDS M0",
        "DF501": "BDS Cuc",
        "DF502": "BDS e",
        "DF503": "BDS Cus",
        "DF504": "BDS A½",
        "DF505": "BDS Toe",
        "DF506": "BDS Cic",
        "DF507": "BDS Ω0",
        "DF508": "BDS Cis",
        "DF509": "BDS i0",
        "DF510": "BDS Crc",
        "DF511": "BDS ω",
        "DF512": "BDS ΩDOT",
        "DF513": "BDS TGD1",
        "DF514": "BDS TGD2",
        "DF515": "BSD SV Health",
    },
    "1044": {
        "DF002": "Message Number",
        "DF429": "QZSS Satellite ID",
        "DF430": "QZSS toc",
        "DF431": "QZSS af2",
        "DF432": "QZSS af1",
        "DF433": "QZSS af0",
        "DF434": "QZSS IODE",
        "DF435": "QZSS Crs",
        "DF436": "QZSS ∆n",
        "DF437": "QZSS M0",
        "DF438": "QZSS Cuc",
        "DF439": "QZSS e",
        "DF440": "QZSS Cus",
        "DF441": "QZSS A½",
        "DF442": "QZSS toe",
        "DF443": "QZSS Cic",
        "DF444": "QZSS Ω0",
        "DF445": "QZSS Cis",
        "DF446": "QZSS i0",
        "DF447": "QZSS Crc",
        "DF448": "QZSS ω",
        "DF449": "QZSS Ω0n DOT",
        "DF450": "QZSS i0-DOT",
        "DF451": "QZSS Codes on L2 Channel",
        "DF452": "QZSS Week Number",
        "DF453": "QZSS URA",
        "DF454": "QZSS SV health",
        "DF455": "QZSS TGD",
        "DF456": "QZSS IODC",
        "DF457": "QZSS Fit Interval",
    },
    "1045": {
        "DF002": "Message Number",
        "DF252": "Galileo Satellite ID",
        "DF289": "Galileo Week Number",
        "DF290": "Galileo IODnav",
        "DF291": "Galileo SV SISA",
        "DF292": "Galileo Rate of Inclination (IDOT)",
        "DF293": "Galileo toc",
        "DF294": "Galileo af2",
        "DF295": "Galileo af1",
        "DF296": "Galileo af0",
        "DF297": "Galileo Crs",
        "DF298": "Galileo ∆n",
        "DF299": "Galileo M0",
        "DF300": "Galileo Cuc",
        "DF301": "Galileo Eccentricity (e)",
        "DF302": "Galileo Cus",
        "DF303": "Galileo A½",
        "DF304": "Galileo toe",
        "DF305": "Galileo Cic",
        "DF306": "Galileo Ω0",
        "DF307": "Galileo Cis",
        "DF308": "Galileo i0",
        "DF309": "Galileo Crc",
        "DF310": "Galileo ω",
        "DF311": "Galileo ΩDOT",
        "DF312": "Galileo BGD (E1/E5a)",
        "DF314": "Galileo E5a Signal Health Status (OSHS)",
        "DF315": "Galileo E5a Data Validity Status (OSDVS)",
        "DF001_7": "Reserved",
    },
    "1046": {
        "DF002": "Message Number",
        "DF252": "Galileo Satellite ID",
        "DF289": "Galileo Week Number",
        "DF290": "Galileo IODnav",
        "DF286": "Galileo SISA Index (E1,E5b)",
        "DF292": "Galileo Rate of Inclination (IDOT)",
        "DF293": "Galileo toc",
        "DF294": "Galileo af2",
        "DF295": "Galileo af1",
        "DF296": "Galileo af0",
        "DF297": "Galileo Crs",
        "DF298": "Galileo ∆n",
        "DF299": "Galileo M0",
        "DF300": "Galileo Cuc",
        "DF301": "Galileo Eccentricity (e)",
        "DF302": "Galileo Cus",
        "DF303": "Galileo A½",
        "DF304": "Galileo toe",
        "DF305": "Galileo Cic",
        "DF306": "Galileo Ω0",
        "DF307": "Galileo Cis",
        "DF308": "Galileo i0",
        "DF309": "Galileo Crc",
        "DF310": "Galileo ω",
        "DF311": "Galileo ΩDOT",
        "DF312": "Galileo BGD (E1/E5a)",
        "DF313": "Galileo BGD (E5b,E1)",
        "DF316": "Galileo E5b Signal Health Status",
        "DF317": "Galileo E5b Data Validity Status",
        "DF287": "Galileo E1b Signal Health Status",
        "DF288": "Galileo E1b Data Validity Status",
        "DF001_2": "Reserved",
    },
    "1057": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF375": "Satellite Reference Datum",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF071": "GPS IODE",
                "DF365": "Delta Radial",
                "DF366": "Delta Along-Track",
                "DF367": "Delta Cross-Track",
                "DF368": "Dot Delta Radial",
                "DF369": "Dot Delta Along-Track",
                "DF370": "Dot Delta Cross-Track",
            },
        ),
    },
    "1058": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF376": "Delta Clock C0",
                "DF377": "Delta Clock C1",
                "DF378": "Delta Clock C2",
            },
        ),
    },
    "1059": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "groupsat": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF379": "No. of Code Biases Processed",
                "groupbias": (  # nested group
                    "DF379",
                    {
                        "DF380": "GPS Signal and Tracking Mode Indicator",
                        "DF383": "Code Bias",
                    },
                ),
            },
        ),
    },
    "1060": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF375": "Satellite Reference Datum",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF071": "GPS IODE",
                "DF365": "Delta Radial",
                "DF366": "Delta Along-Track",
                "DF367": "Delta Cross-Track",
                "DF368": "Dot Delta Radial",
                "DF369": "Dot Delta Along-Track",
                "DF370": "Dot Delta Cross-Track",
                "DF376": "Delta Clock C0",
                "DF377": "Delta Clock C1",
                "DF378": "Delta Clock C2",
            },
        ),
    },
    "1061": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF389": "SSR URA",
            },
        ),
    },
    "1062": {
        "DF002": "Message Number",
        "DF385": "GPS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF068": "GPS Satellite ID",
                "DF390": "High Rate Clock Correction",
            },
        ),
    },
    "1063": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF375": "Satellite Reference Datum",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF392": "GLONASS IOD",
                "DF365": "Delta Radial",
                "DF366": "Delta Along-Track",
                "DF367": "Delta Cross-Track",
                "DF368": "Dot Delta Radial",
                "DF369": "Dot Delta Along-Track",
                "DF370": "Dot Delta Cross-Track",
            },
        ),
    },
    "1064": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF376": "Delta Clock C0",
                "DF377": "Delta Clock C1",
                "DF378": "Delta Clock C2",
            },
        ),
    },
    "1065": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "groupsat": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF379": "No. of Code Biases Processed",
                "groupbias": (  # nested group
                    "DF379",
                    {
                        "DF381": "GLONASS Signal and Tracking Mode Indicator",
                        "DF383": "Code Bias",
                    },
                ),
            },
        ),
    },
    "1066": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF375": "Satellite Reference Datum",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF392": "GLONASS IOD",
                "DF365": "Delta Radial",
                "DF366": "Delta Along-Track",
                "DF367": "Delta Cross-Track",
                "DF368": "Dot Delta Radial",
                "DF369": "Dot Delta Along-Track",
                "DF370": "Dot Delta Cross-Track",
                "DF376": "Delta Clock C0",
                "DF377": "Delta Clock C1",
                "DF378": "Delta Clock C2",
            },
        ),
    },
    "1067": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF389": "SSR URA",
            },
        ),
    },
    "1068": {
        "DF002": "Message Number",
        "DF386": "GLONASS Epoch Time 1s",
        "DF391": "SSR Update Interval",
        "DF388": "Multiple Message Indicator",
        "DF413": "IOD SSR",
        "DF414": "SSR Provider ID",
        "DF415": "SSR Solution ID",
        "DF387": "No. of Satellites",
        "group": (
            "DF387",
            {
                "DF384": "GLONASS Satellite ID",
                "DF390": "High Rate Clock Correction",
            },
        ),
    },
    # GPS
    "1071": MSM1,
    "1072": MSM2,
    "1073": MSM3,
    "1074": MSM4,
    "1075": MSM5,
    "1076": MSM6,
    "1077": MSM7,
    # GLONASS
    "1081": MSM1,
    "1082": MSM2,
    "1083": MSM3,
    "1084": MSM4,
    "1085": MSM5,
    "1086": MSM6,
    "1087": MSM7,
    # Galileo
    "1091": MSM1,
    "1092": MSM2,
    "1093": MSM3,
    "1094": MSM4,
    "1095": MSM5,
    "1096": MSM6,
    "1097": MSM7,
    # SBAS
    "1101": MSM1,
    "1102": MSM2,
    "1103": MSM3,
    "1104": MSM4,
    "1105": MSM5,
    "1106": MSM6,
    "1107": MSM7,
    # QZSS
    "1111": MSM1,
    "1112": MSM2,
    "1113": MSM3,
    "1114": MSM4,
    "1115": MSM5,
    "1116": MSM6,
    "1117": MSM7,
    # BeiDou
    "1121": MSM1,
    "1122": MSM2,
    "1123": MSM3,
    "1124": MSM4,
    "1125": MSM5,
    "1126": MSM6,
    "1127": MSM7,
    # IRNSS
    "1131": MSM1,
    "1132": MSM2,
    "1133": MSM3,
    "1134": MSM4,
    "1135": MSM5,
    "1136": MSM6,
    "1137": MSM7,
    "1230": {
        "DF002": "Message Number",
        "DF003": "Reference Station ID",
        "DF421": "GLONASS Code-Phase bias indicator",
        "DF001_3": "Reserved",
        "DF422": "GLONASS FDMA signals mask",  # NBIAS = num bits set
        # TODO verify that each iteration of this group only ever contains
        # one of either DF423, DF424, DF425 or FD426?
        "group": (
            NBIAS,
            {
                "DF423": "GLONASS L1 C/A Code-Phase Bias",
                # "DF424": "GLONASS L1 P Code-Phase Bias",
                # "DF425": "GLONASS L2 C/A Code-Phase Bias",
                # "DF426": "GLONASS L2 P Code-Phase Bias",
            },
        ),
    },
}
