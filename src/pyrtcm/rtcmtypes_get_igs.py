"""
RTCM Protocol IGS payload definitions

Information sourced from https://files.igs.org/pub/data/format/igs_ssr_v1.pdf

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyrtcm.rtcmtypes_core import NHARMCOEFFC, NHARMCOEFFS

# *************************************************************
# RTCM3 IGS SSR 4076 COMMON PAYLOAD DEFINITIONS
# *************************************************************
IGM01 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF006": "Global/Regional CRS Indicator",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF012": "GNSS IOD",
            "IDF013": "Delta Orbit Radial",
            "IDF014": "Delta Orbit Along-Track",
            "IDF016": "Delta Orbit Cross-Track",
            "IDF015": "Dot Orbit Delta Radial",
            "IDF017": "Dot Orbit Delta Along-Track",
            "IDF018": "Dot Orbit Delta Cross-Track",
        },
    ),
}
IGM02 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF019": "Delta Clock C0",
            "IDF020": "Delta Clock C1",
            "IDF021": "Delta Clock C2",
        },
    ),
}
IGM03 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF006": "Global/Regional CRS Indicator",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF012": "GNSS IOD",
            "IDF013": "Delta Orbit Radial",
            "IDF014": "Delta Orbit Along-Track",
            "IDF015": "Delta Orbit Cross-Track",
            "IDF016": "Dot Orbit Delta Radial",
            "IDF017": "Dot Orbit Delta Along-Track",
            "IDF018": "Dot Orbit Delta Cross-Track",
            "IDF019": "Delta Clock C0",
            "IDF020": "Delta Clock C1",
            "IDF021": "Delta Clock C2",
        },
    ),
}
IGM04 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF022": "High Rate Clock Correction",
        },
    ),
}
IGM05 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF023": "No. of Biases Processed",
            "groupbias": (  # nested group
                "IDF023+1",  # +1 signifies 1 nested group index must be added
                {
                    "IDF024": "GNSS Signal and Tracking Mode Identifier",
                    "IDF025": "Code Bias",
                },
            ),
        },
    ),
}
IGM06 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF032": "Dispersive Bias Consistency Indicator",
    "IDF033": "MW Consistency Indicator",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF023": "No. of Biases Processed",
            "IDF026": "Yaw Angle",
            "IDF027": "Yaw Rate",
            "groupbias": (  # nested group
                "IDF023+1",  # +1 signifies 1 nested group index must be added
                {
                    "IDF024": "GNSS Signal and Tracking Mode Identifier",
                    "IDF029": "Signal Integer Indicator",
                    "IDF030": "Signals Wide-Lane Integer Indicator",
                    "IDF031": "Signal Discontinuity Counter",
                    "IDF028": "Phase Bias",
                },
            ),
        },
    ),
}
IGM07 = {
    "DF002": "RTCM Message Number",
    "IDF001": "IGS SSR Version",
    "IDF002": "IGS Message Number",
    "IDF003": "SSR Epoch Time 1s",
    "IDF004": "SSR Update Interval",
    "IDF005": "SSR Multiple Message Indicator",
    "IDF007": "IOD SSR",
    "IDF008": "SSR Provider ID",
    "IDF009": "SSR Solution ID",
    "IDF010": "No. of Satellites",
    "groupsat": (
        "IDF010",
        {
            "IDF011": "GNSS Satellite ID",
            "IDF034": "SSR URA",
        },
    ),
}

# *************************************************************
# RTCM3 IGS MESSAGE PAYLOAD DEFINITIONS
# *************************************************************
RTCM_PAYLOADS_GET_IGS = {
    "4076_021": {**IGM01},
    "4076_022": {**IGM02},
    "4076_023": {**IGM03},
    "4076_024": {**IGM04},
    "4076_025": {**IGM05},
    "4076_026": {**IGM06},
    "4076_027": {**IGM07},
    "4076_041": {**IGM01},
    "4076_042": {**IGM02},
    "4076_043": {**IGM03},
    "4076_044": {**IGM04},
    "4076_045": {**IGM05},
    "4076_046": {**IGM06},
    "4076_047": {**IGM07},
    "4076_061": {**IGM01},
    "4076_062": {**IGM02},
    "4076_063": {**IGM03},
    "4076_064": {**IGM04},
    "4076_065": {**IGM05},
    "4076_066": {**IGM06},
    "4076_067": {**IGM07},
    "4076_081": {**IGM01},
    "4076_082": {**IGM02},
    "4076_083": {**IGM03},
    "4076_084": {**IGM04},
    "4076_085": {**IGM05},
    "4076_086": {**IGM06},
    "4076_087": {**IGM07},
    "4076_101": {**IGM01},
    "4076_102": {**IGM02},
    "4076_103": {**IGM03},
    "4076_104": {**IGM04},
    "4076_105": {**IGM05},
    "4076_106": {**IGM06},
    "4076_107": {**IGM07},
    "4076_121": {**IGM01},
    "4076_122": {**IGM02},
    "4076_123": {**IGM03},
    "4076_124": {**IGM04},
    "4076_125": {**IGM05},
    "4076_126": {**IGM06},
    "4076_127": {**IGM07},
    "4076_201": {
        "DF002": "RTCM Message Number",
        "IDF001": "IGS SSR Version",
        "IDF002": "IGS Message Number",
        "IDF003": "SSR Epoch Time 1s",
        "IDF004": "SSR Update Interval",
        "IDF005": "SSR Multiple Message Indicator",
        "IDF007": "IOD SSR",
        "IDF008": "SSR Provider ID",
        "IDF009": "SSR Solution ID",
        "IDF041": "VTEC Quality Indicator",
        "IDF035": "Number of Ionospheric Layers",  # Nᴵᴸ - 1
        "groupion": (
            "IDF035",
            {
                "IDF036": "Height of Ionospheric Layer",
                "IDF037": "Spherical Harmonics Degree",  # N - 1
                "IDF038": "Spherical Harmonics Order",  # M - 1
                "groupcoeffC": (
                    NHARMCOEFFC,
                    {
                        "IDF039": "Spherical Harmonic Coefficient C",
                    },
                ),
                "groupcoeffS": (
                    NHARMCOEFFS,
                    {
                        "IDF040": "Spherical Harmonic Coefficient S",
                    },
                ),
            },
        ),
    },
}
