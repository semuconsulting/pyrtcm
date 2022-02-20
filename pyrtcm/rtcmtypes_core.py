"""
RTCM Protocol core globals and constants

Created on 14 Feb 2022

Information sourced from RTCM STANDARD 10403.2 © 2013 RTCM

:author: semuadmin
"""
# pylint: disable=line-too-long

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

# ***************************************************
# THESE ARE THE RTCM PROTOCOL DATA TYPES
# ***************************************************
BIT1 = "BIT001"  # 1 bit bit field
BIT2 = "BIT002"  # 2 bit bit field
BIT3 = "BIT003"  # 3 bit bit field
BIT4 = "BIT004"  # 4 bit bit field
BIT6 = "BIT006"  # 6 bit bit field
BIT7 = "BIT007"  # 7 bit bit field
BIT8 = "BIT008"  # 8 bit bit field
BIT10 = "BIT010"  # 10 bit bit field
BIT12 = "BIT012"  # 12 bit bit field
BIT32 = "BIT032"  # 32 bit bit field
BIT64 = "BIT064"  # 64 bit bit field
BITX = "BIT999"  # variable bit field TODO check against usage
CHAR8 = "CHA008"  # 8 bit characters, ISO 8859-1 (not limited to ASCII)
INT8 = "INT008"  # 8 bit 2’s complement integer
INT9 = "INT009"  # 9 bit 2’s complement integer
INT10 = "INT010"  # 10 bit 2’s complement integer
INT12 = "INT012"  # 12 bit 2’s complement integer
INT14 = "INT014"  # 14 bit 2’s complement integer
INT15 = "INT015"  # 15 bit 2’s complement integer
INT16 = "INT016"  # 16 bit 2’s complement integer
INT17 = "INT017"  # 17 bit 2’s complement integer
INT19 = "INT019"  # 19 bit bit 2’s complement integer
INT20 = "INT020"  # 20 bit 2’s complement integer
INT21 = "INT021"  # 21 bit 2’s complement integer
INT22 = "INT022"  # 22 bit 2’s complement integer
INT23 = "INT023"  # 23 bit 2’s complement integer
INT24 = "INT024"  # 24 bit 2’s complement integer
INT25 = "INT025"  # 25 bit 2’s complement integer
INT26 = "INT026"  # 26 bit 2’s complement integer
INT27 = "INT027"  # 27 bit 2's complement integer
INT30 = "INT030"  # 30 bit 2’s complement integer
INT32 = "INT032"  # 32 bit 2’s complement integer
INT34 = "INT034"  # 34 bit 2’s complement integer
INT35 = "INT035"  # 35 bit 2’s complement integer
INT38 = "INT038"  # 38 bit 2’s complement integer
UINT2 = "UINT002"  # 2 bit unsigned integer
UINT3 = "UINT003"  # 3 bit unsigned integer
UINT4 = "UINT004"  # 4 bit unsigned integer
UINT5 = "UINT005"  # 5 bit unsigned integer
UINT6 = "UINT006"  # 6 bit unsigned integer
UINT7 = "UINT007"  # 7 bit unsigned integer
UINT8 = "UINT008"  # 8 bit unsigned integer
UINT9 = "UINT009"  # 9 bit unsigned integer
UINT10 = "UNT010"  # 10 bit unsigned integer
UINT11 = "UNT011"  # 11 bit unsigned integer
UINT12 = "UNT012"  # 12 bit unsigned integer
UINT14 = "UNT014"  # 14 bit unsigned integer
UINT16 = "UNT016"  # 16 bit unsigned integer
UINT17 = "UNT017"  # 17 bit unsigned integer
UINT18 = "UNT018"  # 18 bit unsigned integer
UINT20 = "UNT020"  # 20 bit unsigned integer
UINT23 = "UNT023"  # 23 bit unsigned integer
UINT24 = "UNT024"  # 24 bit unsigned integer
UINT25 = "UNT025"  # 25 bit unsigned integer
UINT26 = "UNT026"  # 26 bit unsigned integer
UINT27 = "UNT027"  # 27 bit unsigned integer
UINT30 = "UNT030"  # 30 bit unsigned integer
UINT32 = "UNT032"  # 32 bit unsigned integer
UINT35 = "UNT035"  # 35 bit unsigned integer
UINT36 = "UNT036"  # 36 bit unsigned integer
INTS5 = "SNT005"  # 5 bit sign-magnitude integer
INTS11 = "SNT011"  # 11 bit sign-magnitude integer
INTS22 = "SNT022"  # 22 bit sign-magnitude integer
INTS24 = "SNT024"  # 24 bit sign-magnitude integer
INTS27 = "SNT027"  # 27 bit sign-magnitude integer
INTS32 = "SNT032"  # 32 bit sign-magnitude integer
UTF8 = "UTF008"  # Unicode UTF-8 Code Unit


# ***************************************************
# THESE ARE THE RTCM PROTOCOL DATA FIELDS
#
# DF key: (data_type, resolution, description)
#
# ***************************************************
RTCM_DATA_FIELDS = {
    "DF001": (BIT1, 0, "Reserved Field"),
    "DF001_1": (BIT1, 0, "Reserved 1 bit"),
    "DF001_2": (BIT2, 0, "Reserved 2 bits"),
    "DF001_3": (BIT3, 0, "Reserved 3 bits"),
    "DF001_7": (BIT7, 0, "Reserved 7 bits"),
    "DF002": (UINT12, 0, "Message Number"),
    "DF003": (UINT12, 0, "Reference Station ID"),
    "DF004": (UINT30, 1, "GPS Epoch Time (TOW)"),
    "DF005": (BIT1, 0, "Synchronous GNSS Message Flag"),
    "DF006": (UINT5, 0, "No. of GPS Satellite Signals Processed"),
    "DF007": (BIT1, 0, "GPS Divergencefree Smoothing Indicator"),
    "DF008": (BIT3, 0, "GPS Smoothing Interval"),
    "DF009": (UINT6, 0, "GPS Satellite ID"),
    "DF010": (BIT1, 0, "GPS L1 Code Indicator"),
    "DF011": (UINT24, 0.02, "GPS L1 Pseudorange"),
    "DF012": (INT20, 0.0005, "GPS L1 PhaseRange - L1 Pseudorange"),
    "DF013": (UINT7, 0, "GPS L1 Lock Time Indicator"),
    "DF014": (UINT8, 0, "GPS Integer L1 Pseudorange Modulus Ambiguity"),
    "DF015": (UINT8, 0.25, "GPS L1 CNR"),
    "DF016": (BIT2, 0, "GPS L2 Code Indicator"),
    "DF017": (INT14, 0.02, "GPS L2-L1 Pseudorange Difference"),
    "DF018": (INT20, 0.0005, "GPS L2 PhaseRange - L1 Pseudorange"),
    "DF019": (UINT7, 0, "GPS L2 Lock Time Indicator"),
    "DF020": (UINT8, 0.25, "GPS L2 CNR"),
    "DF021": (UINT6, 0, "ITRF Realization Year"),
    "DF022": (BIT1, 0, "GPS Indicator"),
    "DF023": (BIT1, 0, "GLONASS Indicator"),
    "DF024": (BIT1, 0, "Galileo Indicator"),
    "DF025": (INT38, 0.0001, "Antenna Ref. Point ECEF-X"),
    "DF026": (INT38, 0.0001, "Antenna Ref. Point ECEF-Y"),
    "DF027": (INT38, 0.0001, "Antenna Ref. Point ECEF-Z"),
    "DF028": (UINT16, 0.0001, "Antenna Height"),
    "DF029": (UINT8, 0, "Descriptor Counter"),
    "DF030": (CHAR8, 0, "Antenna Descriptor"),
    "DF031": (UINT8, 0, "Antenna Setup ID"),
    "DF032": (UINT8, 0, "Serial Number Counter"),
    "DF033": (CHAR8, 0, "Antenna Serial Number"),
    "DF034": (UINT27, 1, "GLONASS Epoch Time (tk)"),
    "DF035": (UINT5, 1, "No. of GLONASS Satellite Signals Processed"),
    "DF036": (BIT1, 0, "GLONASS Divergence-free Smoothing Indicator"),
    "DF037": (BIT3, 0, "GLONASS Smoothing Interval"),
    "DF038": (UINT6, 0, "GLONASS Satellite ID (Satellite Slot Number)"),
    "DF039": (BIT1, 0, "GLONASS L1 Code Indicator"),
    "DF040": (UINT5, 1, "GLONASS Satellite Frequency Channel Number"),
    "DF041": (UINT25, 0.02, "GLONASS L1 Pseudorange"),
    "DF042": (INT20, 0.0005, "GLONASS L1 PhaseRange - L1 Pseudorange"),
    "DF043": (UINT7, 0, "GLONASS L1 Lock Time Indicator"),
    "DF044": (
        UINT7,
        0,
        "GLONASS Integer L1 Pseudorange Modulus Ambiguity",
    ),
    "DF045": (UINT8, 0.25, "GLONASS L1 CNR"),
    "DF046": (BIT2, 0, "GLONASS L2 Code Indicator"),
    "DF047": (INT14, 0.02, "GLONASS L2-L1 Pseudorange Difference"),
    "DF048": (INT20, 0.0005, "GLONASS L2 PhaseRange - L1 Pseudorange"),
    "DF049": (UINT7, 0, "GLONASS L2 Lock Time Indicator"),
    "DF050": (UINT8, 0.25, "GLONASS L2 CNR"),
    "DF051": (UINT16, 1, "Modified Julian Day (MJD) Number"),
    "DF052": (UINT17, 1, "Seconds of Day (UTC)"),
    "DF053": (UINT5, 1, "Number of Message ID Announcements  to Follow (Nm)"),
    "DF054": (UINT8, 1, "Leap Seconds, GPS-UTC"),
    "DF055": (UINT12, 1, "Message ID"),
    "DF056": (BIT1, 0, "Message Sync Flag"),
    "DF057": (UINT16, 0.1, "Message Transmission Interval"),
    "DF058": (UINT5, 1, "Number of Auxiliary Stations Transmitted"),
    "DF059": (UINT8, 1, "Network ID"),
    "DF060": (UINT12, 1, "Master Reference Station ID"),
    "DF061": (UINT12, 1, "Auxiliary Reference Station ID"),
    "DF062": (INT20, 25 * 10**6, "Aux-Master Delta Latitude"),
    "DF063": (INT21, 25 * 10**6, "Aux-Master Delta Longitude"),
    "DF064": (INT23, 1, "Aux-Master Delta Height"),
    "DF065": (UINT23, 0.1, "GPS Epoch Time (GPS TOW)"),
    "DF066": (BIT1, 1, "GPS Multiple Message Indicator"),
    "DF067": (UINT4, 1, "Number of GPS Satellites"),
    "DF068": (UINT6, 1, "GPS Satellite ID"),
    "DF069": (INT17, 0.5, "GPS Ionospheric Carrier Phase Correction Difference"),
    "DF070": (INT17, 0.5, "GPS Geometric Carrier Phase Correction Difference"),
    "DF071": (BIT8, 1, "GPS IODE"),
    "DF072": (UINT4, 0, "Subnetwork ID"),
    "DF073": (UINT8, 0, "RESERVED for Provider ID"),
    "DF074": (BIT2, 0, "GPS Ambiguity Status Flag"),
    "DF075": (UINT3, 0, "GPS Non Sync Count"),
    "DF076": (UINT10, 0, "GPS Week number"),
    "DF077": (BIT4, 0, "GPS SV Acc. (URA)"),
    "DF078": (BIT2, 1, "GPS CODE ON L2"),
    "DF079": (INT14, 2**-43, "GPS IDOT"),
    "DF080": (UINT8, 1, "GPS IODE"),
    "DF081": (UINT16, 2**4, "GPS toc"),
    "DF082": (INT8, 2**-55, "GPS af2"),
    "DF083": (INT16, 2**-43, "GPS af1"),
    "DF084": (INT22, 2**-31, "GPS af0"),
    "DF085": (UINT10, 1, "GPS IODC"),
    "DF086": (INT16, 2**-5, "GPS Crs"),
    "DF087": (INT16, 2**-43, "GPS n (DELTA n)"),
    "DF088": (INT32, 2**-31, "GPS M0"),
    "DF089": (INT16, 2**-29, "GPS Cuc"),
    "DF090": (UINT32, 0, "GPS Eccentricity (e)"),
    "DF091": (INT16, 2**-29, "GPS Cus"),
    "DF092": (UINT32, 2**-19, "GPS (A)1/2"),
    "DF093": (UINT16, 2**4, "GPS toe"),
    "DF094": (INT16, 2**-29, "GPS Cic"),
    "DF095": (INT32, 2**-31, "GPS 0 (OMEGA)0"),
    "DF096": (INT16, 2**-29, "GPS Cis"),
    "DF097": (INT32, 2**-31, "GPS i0"),
    "DF098": (INT16, 2**-5, "GPS Crc"),
    "DF099": (INT32, 2**-31, "GPS  (Argument of Perigee)"),
    "DF100": (INT24, 2**-43, "GPS OMEGADOT (Rate of Right Ascension)"),
    "DF101": (INT8, 2**-31, "GPS tGD"),
    "DF102": (UINT6, 1, "GPS SV HEALTH"),
    "DF103": (BIT1, 1, "GPS L2 P data flag"),
    "DF104": (BIT1, 0, "GLONASS almanac health"),
    "DF105": (BIT1, 0, "GLONASS almanac health availability indicator"),
    "DF106": (BIT2, 0, "GLONASS P1"),
    "DF107": (BIT12, 0, "GLONASS tk"),
    "DF108": (BIT1, 0, "GLONASS MSB of Bn  word"),
    "DF109": (BIT1, 0, "GLONASS P2"),
    "DF110": (UINT7, 15, "GLONASS tb"),
    "DF111": (INTS24, 2**-20, "GLONASS xn(tb), first derivative"),
    "DF112": (INTS27, 2**-11, "GLONASS xn(tb)"),
    "DF113": (INTS5, 2**-30, "GLONASS xn(tb), second derivative"),
    "DF114": (INTS24, 2**-20, "GLONASS yn(tb), first derivative"),
    "DF115": (INTS27, 2**-11, "GLONASS yn(tb)"),
    "DF116": (INTS5, 2**-30, "GLONASS yn(tb), second derivative"),
    "DF117": (INTS24, 2**-20, "GLONASS zn(tb), first derivative"),
    "DF118": (INTS27, 2**-11, "GLONASS zn(tb)"),
    "DF119": (INTS5, 2**-30, "GLONASS zn(tb), second derivative"),
    "DF120": (BIT1, 0, "GLONASS P3"),
    "DF121": (INTS11, 0, "GLONASS n(tb)"),
    "DF122": (BIT2, 0, "GLONASS-M P"),
    "DF123": (BIT1, 0, "GLONASS-M ln  (third string)"),
    "DF124": (INTS22, 0, "GLONASS n(tb)"),
    "DF125": (INTS5, 0, "GLONASS-M Δn"),
    "DF126": (UINT5, 1, "GLONASS En"),
    "DF127": (BIT1, 0, "GLONASS-M P4"),
    "DF128": (UINT4, 0, "GLONASS-M FT"),
    "DF129": (UINT11, 1, "GLONASS-M NT"),
    "DF130": (BIT2, 0, "GLONASS-M M"),
    "DF131": (BIT1, 0, "GLONASS The Availability of Additional Data"),
    "DF132": (UINT11, 1, "GLONASS NA"),
    "DF133": (INTS32, 0, "GLONASS c"),
    "DF134": (UINT5, 0, "GLONASS-M N4"),
    "DF135": (INTS22, 0, "GLONASS-M GPS"),
    "DF136": (BIT1, 0, "GLONASS-M ln  (fifth string)"),
    "DF137": (BIT1, 1, "GPS Fit Interval"),
    "DF138": (UINT7, 1, "Number of Characters to Follow"),
    "DF139": (UINT8, 1, "Number of UTF-8 Code Units"),
    "DF140": (UTF8, 0, "UTF-8 Character Code Units"),
    "DF141": (BIT1, 0, "Reference-Station Indicator"),
    "DF142": (BIT1, 0, "Single Receiver Oscillator Indicator"),
    "DF143": (UINT5, 0, "Source-Name Counter"),
    "DF144": (CHAR8, 0, "Source-Name"),
    "DF145": (UINT5, 0, "Target-Name Counter"),
    "DF146": (CHAR8, 0, "Target-Name"),
    "DF147": (UINT8, 0, "SystemIdentification Number"),
    "DF148": (BIT10, 0, "Utilized Tranformation Message Indicator"),
    "DF149": (UINT5, 0, "Plate Number"),
    "DF150": (UINT4, 0, "Computation Indicator"),
    "DF151": (UINT2, 0, "Height Indicator"),
    "DF152": (INT19, 2, "ΦV"),
    "DF153": (INT20, 2, "ΛV"),
    "DF154": (UINT14, 2, "∆ΦV"),
    "DF155": (UINT14, 2, "∆ΛV"),
    "DF156": (INT23, 0.001, "dX"),
    "DF157": (INT23, 0.001, "dY"),
    "DF158": (INT23, 0.001, "dZ"),
    "DF159": (INT32, 0.00002, "R1"),
    "DF160": (INT32, 0.00002, "R2"),
    "DF161": (INT32, 0.00002, "R3"),
    "DF162": (INT25, 0.00001, "dS"),
    "DF163": (INT35, 0.001, "XP"),
    "DF164": (INT35, 0.001, "YP"),
    "DF165": (INT35, 0.001, "ZP"),
    "DF166": (UINT24, 0.001, "add aS"),
    "DF167": (UINT25, 0.001, "add bS"),
    "DF168": (UINT24, 0.001, "add aT"),
    "DF169": (UINT25, 0.001, "add bT"),
    "DF170": (UINT6, 0, "Projection Type"),
    "DF171": (INT34, 0.000000011, "LaNO [°]"),
    "DF172": (INT35, 0.000000011, "LoNO [°]"),
    "DF173": (UINT30, 0.00001, "add SNO"),
    "DF174": (UINT36, 0.001, "FE"),
    "DF175": (INT35, 0.001, "FN"),
    "DF176": (INT34, 0.000000011, "LaFO [°]"),
    "DF177": (INT35, 0.000000011, "LoFO [°]"),
    "DF178": (INT34, 0.000000011, "LaSP1 [°]"),
    "DF179": (INT34, 0.000000011, "LaSP2 [°]"),
    "DF180": (UINT36, 0.001, "EFO"),
    "DF181": (INT35, 0.001, "NFO"),
    "DF182": (BIT1, 0, "Rectification Flag"),
    "DF183": (INT34, 0.000000011, "LaPC"),
    "DF184": (INT35, 0.000000011, "LoPC"),
    "DF185": (UINT35, 0.000000011, "AzIL"),
    "DF186": (INT26, 0.000000011, "Diff ARSG"),
    "DF187": (UINT30, 0.00001, "Add SIL"),
    "DF188": (UINT36, 0.001, "EPC"),
    "DF189": (INT35, 0.001, "NPC"),
    "DF190": (BIT1, 0, "Horizontal Shift Indicator"),
    "DF191": (BIT1, 0, "Vertical Shift Indicator"),
    "DF192": (INT21, 0.5, "Φ0"),
    "DF193": (INT22, 0.5, "Λ0"),
    "DF194": (UINT12, 0.5, "∆φ"),
    "DF195": (UINT12, 0.5, "∆λ"),
    "DF196": (INT8, 0.001, "Mean ∆φ"),
    "DF197": (INT8, 0.001, "Mean ∆λ"),
    "DF198": (INT15, 0.01, "Mean ∆H"),
    "DF199": (INT9, 0.00003, "φi"),
    "DF200": (INT9, 0.00003, "λi"),
    "DF201": (INT9, 0.001, "hi"),
    "DF202": (INT25, 10, "N0"),
    "DF203": (UINT26, 10, "E0"),
    "DF204": (UINT12, 10, "∆N"),
    "DF205": (UINT12, 10, "∆E"),
    "DF206": (INT10, 0.01, "Mean ∆N"),
    "DF207": (INT10, 0.01, "Mean ∆E"),
    "DF208": (INT15, 0.01, "Mean ∆h"),
    "DF209": (INT9, 0.001, "Ni"),
    "DF210": (INT9, 0.001, "Ei"),
    "DF211": (INT9, 0.001, "hi"),
    "DF212": (UINT2, 0, "Horizontal Interpolation Method Indicator"),
    "DF213": (UINT2, 0, "Vertical Interpolation Method Indicator"),
    "DF214": (UINT3, 0, "Horizontal Helmert/Molodensk i Quality Indicator"),
    "DF215": (UINT3, 0, "Vertical Helmert/Molodenski Quality Indicator"),
    "DF216": (UINT3, 0, "Horizontal Grid Quality Indicator"),
    "DF217": (UINT3, 0, "Vertical Grid Quality Indicator"),
    "DF218": (UINT8, 0.5, "soc"),
    "DF219": (UINT9, 0.01, "sod"),
    "DF220": (UINT6, 0.1, "soh"),
    "DF221": (UINT10, 0.5, "sIc"),
    "DF222": (UINT10, 0.01, "sId"),
    "DF223": (UINT7, 0, "N-Refs"),
    "DF224": (UINT20, 1, "GPS Residuals Epoch Time (TOW)"),
    "DF225": (UINT17, 1, "GLONASS Residuals Epoch Time (tk)"),
    "DF226": (UINT12, 0, "Physical Reference Station ID"),
    "DF227": (UINT8, 0, "Receiver Type Descriptor Counter"),
    "DF228": (CHAR8, 0, "Receiver Type Descriptor"),
    "DF229": (UINT8, 0, "Receiver Firmware Version Counter"),
    "DF230": (CHAR8, 0, "Receiver Firmware Version"),
    "DF231": (UINT8, 0, "Receiver Serial Number Counter"),
    "DF232": (CHAR8, 0, "Receiver Serial Number"),
    "DF233": (UINT20, 0.1, "GLONASS NW Epoch Time"),
    "DF234": (UINT4, 0, "Number of GLONASS Data Entries"),
    "DF235": (BIT2, 0, "GLONASS Ambiguity Status Flag"),
    "DF236": (UINT3, 0, "GLONASS Non Sync Count"),
    "DF237": (
        INT17,
        0.5,
        "GLONASS Ionospheric Carrier Phase Correction Difference",
    ),
    "DF238": (INT17, 0.5, "GLONASS Geometric Carrier Phase Correction Difference"),
    "DF239": (BIT8, 0, "GLONASS IOD"),
    "DF240": (UINT20, 1, "GPS FKP Epoch Time"),
    "DF241": (UINT17, 1, "GLONASS FKP Epoch Time"),
    "DF242": (INT12, 0.01, "N0: Geometric Gradient in North (ppm)"),
    "DF243": (INT12, 0.01, "E0: Geometric gradient in east (ppm)"),
    "DF244": (INT14, 0.01, "NI: Ionospheric gradient in north  (ppm)"),
    "DF245": (INT14, 0.01, "EI: Ionospheric gradient in east  (ppm)"),
    # 'DF246-DF363': RESERVED,
    "DF364": (BIT2, 0, "Quarter Cycle Indicator"),
    "DF365": (INT22, 0.1, "Delta Radial"),
    "DF366": (INT20, 0.4, "Delta Along-Track"),
    "DF367": (INT20, 0.4, "Delta Cross-Track"),
    "DF368": (INT21, 0.001, "Dot Delta Radial"),
    "DF369": (INT19, 0.004, "Dot Delta AlongTrack"),
    "DF370": (INT19, 0.004, "Dot Delta CrossTrack"),
    "DF371": (INT27, 0.00002, "RESERVED for Dot Dot Delta Radial"),
    "DF372": (INT25, 0.00008, "RESERVED for Dot Dot DeltaAlong-Track"),
    "DF373": (INT25, 0.00008, "RESERVED for Dot Dot Delta Cross-Track"),
    "DF374": (BIT1, 0, "Satellite Reference Point"),
    "DF375": (BIT1, 0, "Satellite Reference Datum"),
    "DF376": (INT22, 0.1, "Delta Clock C0"),
    "DF377": (INT21, 0.001, "Delta Clock C1"),
    "DF378": (INT27, 0.00002, "Delta Clock C2"),
    "DF379": (UINT5, 1, "No. of Code Biases Processed"),
    "DF380": (UINT5, 1, "GPS Signal and Tracking Mode Identifier"),
    "DF381": (UINT5, 1, "GLONASS Signal and Tracking Mode Identifier"),
    "DF382": (UINT5, 1, "RESERVED for Galileo Signal and Tracking Mode Identifier"),
    "DF383": (INT14, 0.01, "Code Bias"),
    "DF384": (UINT5, 1, "GLONASS Satellite ID"),
    "DF385": (UINT20, 1, "GPS Epoch Time 1s"),
    "DF386": (UINT17, 1, "GLONASS Epoch Time 1s"),
    "DF387": (UINT6, 1, "No. of Satellites"),
    "DF388": (BIT1, 1, "Multiple Message Indicator"),
    "DF389": (BIT6, 0, "SSR URA"),
    "DF390": (INT22, 0.1, "High Rate Clock Correction"),
    "DF391": (BIT4, 1, "SSR Update Interval"),
    "DF392": (BIT8, 0, "GLONASS Issue Of Data (IOD)"),
    "DF393": (BIT1, 0, "MSM Multiple message bit"),
    "DF394": (BIT64, 0, "GNSS Satellite mask"),
    "DF395": (BIT32, 0, "GNSS Signal mask"),
    "DF396": (BITX, 0, "GNSS Cell mask"),
    "DF397": (
        UINT8,
        1,
        "The number of integer milliseconds in GNSS Satellite  rough range",
    ),
    "DF398": (UINT10, 2**-10, "GNSS Satellite rough range modulo 1 millisecond"),
    "DF399": (INT14, 1, "GNSS Satellite rough Phase Range Rate"),
    "DF400": (INT15, 2**-24, "GNSS signal fine Pseudorange"),
    "DF401": (INT22, 2**-29, "GNSS signal fine PhaseRange data"),
    "DF402": (UINT4, 0, "GNSS PhaseRange Lock Time Indicator"),
    "DF403": (UINT6, 1, "GNSS signal CNR"),
    "DF404": (INT15, 0.0001, "GNSS signal fine Phase Range Rate"),
    "DF405": (
        INT20,
        2**-29,
        "GNSS signal fine Pseudorange with extended resolution",
    ),
    "DF406": (
        INT24,
        2**-31,
        "GNSS signal fine PhaseRange data with extended resolution",
    ),
    "DF407": (
        UINT10,
        0,
        "GNSS PhaseRange Lock Time Indicator with extended range and resolution.",
    ),
    "DF408": (UINT10, 2**-4, "GNSS signal CNR with extended resolution"),
    "DF409": (UINT3, 1, "IODS - Issue Of Data Station"),
    # 'DF410': RESERVED,
    "DF411": (UINT2, 0, "Clock Steering Indicator"),
    "DF412": (UINT2, 0, "External Clock Indicator"),
    "DF413": (UINT4, 1, "IOD SSR"),
    "DF414": (UINT16, 1, "SSR Provider ID"),
    "DF415": (UINT4, 1, "SSR Solution ID"),
    "DF416": (UINT3, 1, "GLONASS Day Of Week"),
    "DF417": (BIT1, 0, "GNSS Smoothing Type Indicator"),
    "DF418": (BIT3, 0, "GNSS Smoothing Interval"),
    "DF419": (UINT4, 1, "GLONASS Satellite Frequency Channel Number"),
    "DF420": (BIT1, 0, "Half-cycle ambiguity indicator"),
    "DF421": (BIT1, 0, "GLONASS Code-Phase Bias Indicator"),
    "DF422": (BIT4, 0, "GLONASS FDMA Signals Mask"),
    "DF423": (INT16, 0.02, "GLONASS L1 C/A Code-Phase Bias"),
    "DF424": (INT16, 0.02, "GLONASS L1 P Code-Phase Bias"),
    "DF425": (INT16, 0.02, "GLONASS L2 C/A Code-Phase Bias"),
    "DF426": (INT16, 0.02, "GLONASS L2 P Code-Phase Bias"),
    "GNSSSpecific": (UINT4, 0, "Extended Satellite Information"),
    "GNSSEpoch": (UINT30, 0, "GNSS Epoch Time"),
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
    "1021": "Helmert / Abridged Molodenski Transformation Parameters",
    "1022": "Molodenski-Badekas Transformation Parameters",
    "1023": "Residuals, Ellipsoidal Grid Representation",
    "1024": "Residuals, Plane Grid Representation",
    "1025": "Projection Parameters, Projection Types other than Lambert Conic Conformal (2 SP) and Oblique Mercator",
    "1026": "Projection Parameters, Projection Type LCC2SP (Lambert Conic Conformal (2 SP))",
    "1027": "Projection Parameters, Projection Type OM (Oblique Mercator)",
    "1028": "(Reserved for Global to Plate-Fixed Transformation)",
    "1029": "Unicode Text String",
    "1030": "GPS Network RTK Residual Message",
    "1031": "GLONASS Network RTK Residual Message",
    "1032": "Physical Reference Station Position Message",
    "1033": "Receiver and Antenna Descriptors",
    "1034": "GPS Network FKP Gradient",
    "1035": "GLONASS Network FKP Gradient",
    "1037": "GLONASS Ionospheric Correction Differences",
    "1038": "GLONASS Geometric Correction Differences",
    "1039": "GLONASS Combined Geometric and Ionospheric Correction Differences",
    "1057": "SSR GPS Orbit Correction",
    "1058": "SSR GPS Clock Correction",
    "1059": "SSR GPS Code Bias",
    "1060": "SSR GPS Combined Orbit and Clock Corrections",
    "1061": "SSR GPS URA",
    "1062": "SSR GPS High Rate Clock Correction",
    "1063": "SSR GLONASS Orbit Correction",
    "1064": "SSR GLONASS Clock Correction",
    "1065": "SSR GLONASS Code Bias",
    "1066": "SSR GLONASS Combined Orbit and Clock Correction",
    "1067": "SSR GLONASS URA",
    "1068": "SSR GLONASS High Rate Clock Correction",
    "1070": "Reserved MSM",
    "1071": "GPS MSM1",
    "1072": "GPS MSM2",
    "1073": "GPS MSM3",
    "1074": "GPS MSM4",
    "1075": "GPS MSM5",
    "1076": "GPS MSM6",
    "1077": "GPS MSM7",
    "1078": "Reserved MSM",
    "1079": "Reserved MSM",
    "1080": "Reserved MSM",
    "1081": "GLONASS MSM1",
    "1082": "GLONASS MSM2",
    "1083": "GLONASS MSM3",
    "1084": "GLONASS MSM4",
    "1085": "GLONASS MSM5",
    "1086": "GLONASS MSM6",
    "1087": "GLONASS MSM7",
    "1088": "Reserved MSM",
    "1089": "Reserved MSM",
    "1090": "Reserved MSM",
    "1091": "GALILEO MSM1",
    "1092": "GALILEO MSM2",
    "1093": "GALILEO MSM3",
    "1094": "GALILEO MSM4",
    "1095": "GALILEO MSM5",
    "1096": "GALILEO MSM6",
    "1097": "GALILEO MSM7",
    "1098": "Reserved MSM",
    "1099": "Reserved MSM",
    "1100": "Reserved MSM",
    "1101": "SBAS MSM1",
    "1102": "SBAS MSM2",
    "1103": "SBAS MSM3",
    "1104": "SBAS MSM4",
    "1105": "SBAS MSM5",
    "1106": "SBAS MSM6",
    "1107": "SBAS MSM7",
    "1108": "Reserved MSM",
    "1109": "Reserved MSM",
    "1110": "Reserved MSM",
    "1111": "QZSS MSM1",
    "1112": "QZSS MSM2",
    "1113": "QZSS MSM3",
    "1114": "QZSS MSM4",
    "1115": "QZSS MSM5",
    "1116": "QZSS MSM6",
    "1117": "QZSS MSM7",
    "1118": "Reserved MSM",
    "1119": "Reserved MSM",
    "1120": "Reserved MSM",
    "1121": "BeiDou MSM1",
    "1122": "BeiDou MSM2",
    "1123": "BeiDou MSM3",
    "1124": "BeiDou MSM4",
    "1125": "BeiDou MSM5",
    "1126": "BeiDou MSM6",
    "1127": "BeiDou MSM7",
    # "1128-1229":"Reserved MSM",
    "1230": "GLONASS L1 and L2 Code-Phase Biases",
    # "4001-4079":"Proprietary Messages",
    "4080": "NavCom Technology, Inc.",
    "4081": "Seoul National University GNSS Lab",
    "4082": "Cooperative Research Centre for Spatial Information",
    "4083": "German Aerospace Center, Institute of Communications and Navigation (DLR)",
    "4084": "Geodetics, Inc.",
    "4085": "European GNSS Supervisory Authority",
    "4086": "inPosition GmbH",
    "4087": "Fugro",
    "4088": "IfEN GmbH",
    "4089": "Septentrio Satellite Navigation",
    "4090": "Geo++",
    "4091": "Topcon Positioning Systems",
    "4092": "Leica Geosystems",
    "4093": "NovAtel Inc.",
    "4094": "Trimble Navigation Ltd.",
    "4095": "Ashtech",
}
