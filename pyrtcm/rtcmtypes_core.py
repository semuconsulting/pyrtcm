"""
RTCM Protocol core globals and constants

Created on 14 Feb 2022

Information sourced from RTCM STANDARD 10403.1 © 2006 RTCM

:author: semuadmin
"""

NMEA_HDR = [b"\x24\x47", b"\x24\x50"]
UBX_HDR = b"\xb5\x62"
RTCM_HDR = b"\xd3"
NMEA_PROTOCOL = 1
UBX_PROTOCOL = 2
RTCM3_PROTOCOL = 4
GET = 0
SET = 1
POLL = 2
VALNONE = 0
VALCKSUM = 1
RTCM3_PROTOCOL = 4
ERR_RAISE = 2
ERR_LOG = 1
ERR_IGNORE = 0
NYI = "NYI"  # not yet implemented flag

# ***************************************************
# THESE ARE THE RTCM PROTOCOL PAYLOAD ATTRIBUTE TYPES
# ***************************************************
BIT1 = "BIT001"  # 1 bit bit field
BIT2 = "BIT002"  # 2 bit bit field
BIT3 = "BIT003"  # 3 bit bit field
BIT4 = "BIT004"  # 4 bit bit field
BIT8 = "BIT008"  # 8 bit bit field
BIT12 = "BIT012"  # 12 bit bit field
CHAR8 = "CHA008"  # 8 bit characters, ISO 8859-1 (not limited to ASCII)
INT8 = "INT008"  # 8 bit 2’s complement integer
INT14 = "INT014"  # 14 bit 2’s complement integer
INT16 = "INT016"  # 16 bit 2’s complement integer
INT17 = "INT017"  # 17 bit 2’s complement integer
INT20 = "INT020"  # 20 bit 2’s complement integer
INT21 = "INT021"  # 21 bit 2’s complement integer
INT22 = "INT022"  # 22 bit 2’s complement integer
INT23 = "INT023"  # 23 bit 2’s complement integer
INT24 = "INT024"  # 24 bit 2’s complement integer
INT30 = "INT030"  # 30 bit 2’s complement integer
INT32 = "INT032"  # 32 bit 2’s complement integer
INT38 = "INT038"  # 38 bit 2’s complement integer
UINT3 = "UNT003"  # 3 bit unsigned integer
UINT4 = "UNT004"  # 4 bit unsigned integer
UINT5 = "UNT005"  # 5 bit unsigned integer
UINT6 = "UNT006"  # 6 bit unsigned integer
UINT7 = "UNT007"  # 7 bit unsigned integer
UINT8 = "UNT008"  # 8 bit unsigned integer
UINT10 = "UNT010"  # 10 bit unsigned integer
UINT11 = "UNT011"  # 11 bit unsigned integer
UINT12 = "UNT012"  # 12 bit unsigned integer
UINT16 = "UNT016"  # 16 bit unsigned integer
UINT17 = "UNT017"  # 17 bit unsigned integer
UINT18 = "UNT018"  # 18 bit unsigned integer
UINT20 = "UNT020"  # 20 bit unsigned integer
UINT23 = "UNT023"  # 23 bit unsigned integer
UINT24 = "UNT024"  # 24 bit unsigned integer
UINT25 = "UNT025"  # 25 bit unsigned integer
UINT27 = "UNT027"  # 27 bit unsigned integer
UINT30 = "UNT030"  # 30 bit unsigned integer
UINT32 = "UNT032"  # 32 bit unsigned integer
INTS5 = "SNT005"  # 5 bit sign-magnitude integer
INTS11 = "SNT011"  # 11 bit sign-magnitude integer
INTS22 = "SNT022"  # 22 bit sign-magnitude integer
INTS24 = "SNT024"  # 24 bit sign-magnitude integer
INTS27 = "SNT027"  # 27 bit sign-magnitude integer
INTS32 = "SNT032"  # 32 bit sign-magnitude integer
UTF8 = "UTF008"  # Unicode UTF-8 Code Unit

# ***************************************************
# THESE ARE THE RTCM PROTOCOL DATA TYPES
# ***************************************************
RTCM_DATA_TYPES = {
    "DF001_1": (BIT1, "Reserved 1 bit"),
    "DF001_2": (BIT2, "Reserved 2 bits"),
    "DF002": (UINT12, "Message Number"),
    "DF003": (UINT12, "Reference Station ID"),
    "DF004": (UINT30, "GPS Epoch Time (TOW)"),
    "DF005": (BIT1, "Synchronous GNSS Message Flag"),
    "DF006": (UINT5, "No. of GPS Satellite Signals Processed"),
    "DF007": (BIT1, "GPS Divergencefree Smoothing Indicator"),
    "DF008": (BIT3, "GPS Smoothing Interval"),
    "DF009": (UINT6, "GPS Satellite ID"),
    "DF010": (BIT1, "GPS L1 Code Indicator"),
    "DF011": (UINT24, "GPS L1 Pseudorange"),
    "DF012": (INT20, "GPS L1 Phaserange - L1 Pseudorange"),
    "DF013": (UINT7, "GPS L1 Lock Time Indicator"),
    "DF014": (UINT8, "GPS Integer L1 Pseudorrange Modulus Ambiguity"),
    "DF015": (UINT8, "GPS L1 CNR"),
    "DF016": (BIT2, "GPS L2 Code Indicator"),
    "DF017": (INT14, "GPS L2-L1 Pseudorange Difference"),
    "DF018": (INT20, "GPS L2 Phaserange - L1 Pseudorange"),
    "DF019": (UINT7, "GPS L2 Lock Time Indicator"),
    "DF020": (UINT8, "GPS L2 CNR"),
    "DF021": (UINT6, "ITRF Realization Year"),
    "DF022": (BIT1, "GPS Indicator"),
    "DF023": (BIT1, "GLONASS Indicator"),
    "DF024": (BIT1, "Galileo Indicator"),
    "DF025": (INT38, "Antenna Ref. Point ECEF-X"),
    "DF026": (INT38, "Antenna Ref. Point ECEF-Y"),
    "DF027": (INT38, "Antenna Ref. Point ECEF-Z"),
    "DF028": (UINT16, "Antenna Height"),
    "DF029": (UINT8, "Descriptor Counter"),
    "DF030": (CHAR8, "Antenna Descriptor"),
    "DF031": (UINT8, "Antenna Setup ID"),
    "DF032": (UINT8, "Serial Number Counter"),
    "DF033": (CHAR8, "Antenna Serial Number"),
    "DF034": (UINT27, "GLONASS Epoch Time (tk)"),
    "DF035": (UINT5, "No. of GLONASS Satellite Signals Processed"),
    "DF036": (BIT1, "GLONASS Divergence-free Smoothing Indicator"),
    "DF037": (BIT3, "GLONASS Smoothing Interval"),
    "DF038": (UINT6, "GLONASS Satellite ID (Satellite Slot Number)"),
    "DF039": (BIT1, "GLONASS L1 Code Indicator"),
    "DF040": (UINT5, "GLONASS Satellite Frequency Channel Number"),
    "DF041": (UINT25, "GLONASS L1 Pseudorange"),
    "DF042": (INT20, "GLONASS L1 PhaseRange - L1 Pseudorange"),
    "DF043": (UINT7, "GLONASS L1 Lock Time Indicator"),
    "DF044": (UINT7, "GLONASS Integer L1 Pseudorange Modulus Ambiguity"),
    "DF045": (UINT8, "GLONASS L1 CNR"),
    "DF046": (BIT2, "GLONASS L2 Code Indicator"),
    "DF047": (INT14, "GLONASS  L2-L1 Pseudorange Difference"),
    "DF048": (INT20, "GLONASS L2 PhaseRange - L1 Pseudorange"),
    "DF049": (UINT7, "GLONASS L2 Lock Time Indicator"),
    "DF050": (UINT8, "GLONASS L2 CNR"),
    "DF051": (UINT16, "Modified Julian Day (MJD) Number"),
    "DF052": (UINT17, "Seconds of Day (UTC)"),
    "DF053": (UINT5, "Number of Message ID Announcements  to Follow (Nm)"),
    "DF054": (UINT8, "Leap Seconds,  GPS-UTC"),
    "DF055": (UINT12, "Message ID"),
    "DF056": (BIT1, "Message Sync Flag"),
    "DF057": (UINT16, "Message Transmission Interval"),
    "DF058": (UINT5, "Number of Auxiliary Stations Transmitted"),
    "DF059": (UINT8, "Network ID"),
    "DF060": (UINT12, "Master Reference Station ID"),
    "DF061": (UINT12, "Auxiliary Reference Station ID"),
    "DF062": (INT20, "Aux-Master Delta Latitude"),
    "DF063": (INT21, "Aux-Master Delta Longitude"),
    "DF064": (INT23, "Aux-Master Delta Height"),
    "DF065": (UINT23, "GPS Epoch Time (GPS TOW)"),
    "DF066": (BIT1, "GPS Multiple Message Indicator"),
    "DF067": (UINT4, "Number of GPS Satellites"),
    "DF068": (UINT6, "GPS Satellite ID"),
    "DF069": (INT17, "GPS Ionospheric Carrier Phase Correction Difference"),
    "DF070": (INT17, "GPS Geometric Carrier Phase Correction Difference"),
    "DF071": (BIT8, "GPS IODE"),
    "DF072": (UINT4, "Subnetwork ID"),
    "DF073": (UINT8, "RESERVED for Provider ID"),
    "DF074": (BIT2, "GPS Ambiguity Status Flag"),
    "DF075": (UINT3, "GPS Non Sync Count"),
    "DF076": (UINT10, "GPS Week number"),
    "DF077": (BIT4, "GPS SV Acc. (URA)"),
    "DF078": (BIT2, "GPS CODE ON L2"),
    "DF084": (INT22, "GPS af0"),
    "DF085": (UINT10, "GPS IODC"),
    "DF086": (INT16, "GPS Crs"),
    "DF087": (INT16, "GPS Δn (DELTA n)"),
    "DF088": (INT32, "GPS M0"),
    "DF089": (INT16, "GPS Cuc"),
    "DF090": (UINT32, "GPS Eccentricity (e)"),
    "DF091": (INT16, "GPS Cus"),
    "DF092": (UINT32, "GPS (A)1/2"),
    "DF093": (UINT16, "GPS toe"),
    "DF094": (INT16, "GPS Cic"),
    "DF095": (INT32, "GPS Ω0 (OMEGA)0"),
    "DF096": (INT16, "GPS Cis"),
    "DF097": (INT32, "GPS i0"),
    "DF098": (INT16, "GPS Crc"),
    "DF099": (INT32, "GPS ω (Argument of Perigee)"),
    "DF100": (INT24, "GPS OMEGADOT (Rate of Right Ascension)"),
    "DF101": (INT8, "GPS tGD"),
    "DF102": (UINT6, "GPS SV HEALTH"),
    "DF103": (BIT1, "GPS L2 P data flag"),
    "DF104": (BIT1, "GLONASS almanac health"),
    "DF105": (BIT1, "GLONASS almanac health availability indicator"),
    "DF106": (BIT2, "GLONASS P1"),
    "DF107": (BIT12, "GLONASS tk"),
    "DF108": (BIT1, "GLONASS MSB of Bn  word"),
    "DF109": (BIT1, "GLONASS P2"),
    "DF110": (UINT7, "GLONASS tb"),
    "DF111": (INTS24, "GLONASS xn(tb), first derivative"),
    "DF112": (INTS27, "GLONASS xn(tb)"),
    "DF113": (INTS5, "GLONASS xn(tb), second derivative"),
    "DF114": (INTS24, "GLONASS yn(tb), first derivative"),
    "DF115": (INTS27, "GLONASS yn(tb)"),
    "DF116": (INTS5, "GLONASS yn(tb), second derivative"),
    "DF117": (INTS24, "GLONASS zn(tb), first derivative"),
    "DF118": (INTS27, "GLONASS zn(tb)"),
    "DF119": (INTS5, "GLONASS zn(tb), second derivative"),
    "DF120": (BIT1, "GLONASS P3"),
    "DF121": (INTS11, "GLONASS yn(tb)"),
    "DF122": (BIT2, "GLONASS-M P"),
    "DF123": (BIT1, "GLONASS-M ln (third string)"),
    "DF124": (INTS22, "GLONASS τn(tb)"),
    "DF125": (INTS5, "GLONASS-M Δτn"),
    "DF126": (UINT5, "GLONASS En"),
    "DF127": (BIT1, "GLONASS-M P4"),
    "DF128": (UINT4, "GLONASS-M FT"),
    "DF129": (UINT11, "GLONASS-M NT"),
    "DF130": (BIT2, "GLONASS-M M"),
    "DF131": (BIT1, "GLONASS The Availability of Additional Data"),
    "DF132": (UINT11, "GLONASS NA"),
    "DF133": (INTS32, "GLONASS τc"),
    "DF134": (UINT5, "GLONASS-M N4"),
    "DF135": (INTS22, "GLONASS-M τGPS"),
    "DF136": (BIT1, "GLONASS-M ln (fifth string)"),
    "DF137": (BIT1, "GPS Fit Interval"),
    "DF138": (UINT7, "Number of Characters to Follow"),
    "DF139": (UINT8, "Number of UTF-8 Code Units"),
    "DF140": (UTF8, "UTF-8 Character Code Units"),
    "DF141": (BIT1, "Reference-Station Indicator"),
    "DF142": (BIT1, "Single Receiver Oscillator Indicator"),
}

# ***************************************************************************
# THESE ARE THE RTCM PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the rtcmtypes_* modules
# ***************************************************************************
RTCM_MSGIDS = {
    "1001": "L1-Only GPS RTK Observables",
    "1002": "Extended L1-Only GPS RTK Observables",
    "1003": "L1&L2 GPS RTK Observables",
    "1004": "Extended L1&L2 GPS RTK Observables",
    "1005": "Stationary RTK Reference Station ARP",
    "1006": "Stationary RTK Reference Station ARP with Antenna Height",
    "1007": "Antenna Descriptor",
    "1008": "Antenna Descriptor & Serial Number",
    "1009": "L1-Only GLONASS RTK Observables",
    "1010": "Extended L1-Only GLONASS RTK Observables",
    "1011": "L1&L2 GLONASS RTK Observables",
    "1012": "Extended L1&L2 GLONASS RTK Observables",
    "1013": "System Parameters",
    "1014": "Network Auxiliary Station Data",
    "1015": "GPS Ionospheric Correction Differences",
    "1016": "GPS Geometric Correction Differences",
    "1017": "GPS Combined Geometric and Ionospheric Correction Differences",
    "1018": "RESERVED for Alternative Ionospheric Correction Difference Message",
    "1019": "GPS Ephemerides",
    "1020": "GLONASS Ephemerides",
    "1021": "RESERVED for Coordinate Transformation Messages",
    "1022": "RESERVED for Coordinate Transformation Messages",
    "1023": "RESERVED for Coordinate Transformation Messages",
    "1024": "RESERVED for Coordinate Transformation Messages",
    "1025": "RESERVED for Coordinate Transformation Messages",
    "1026": "RESERVED for Coordinate Transformation Messages",
    "1027": "RESERVED for Coordinate Transformation Messages",
    "1028": "RESERVED for Coordinate Transformation Messages",
    "1029": "Unicode Text String",
    "1077": "Not Yet Implemented",
    "1087": "Not Yet Implemented",
    "1097": "Not Yet Implemented",
    "1127": "Not Yet Implemented",
    "1230": "Not Yet Implemented",
    # 4001-4087: RESERVED
    "4072": "Not Yet Defined",
    "4088": "IfEN GmbH",
    "4089": "Septentrio Satellite Navigation",
    "4090": "Geo++",
    "4091": "Topcon Positioning Systems",
    "4092": "Leica Geosystems",
    "4093": "NovAtel Inc.",
    "4094": "Trimble Navigation Ltd.",
    "4095": "Magellan Navigation Inc.",
}
