"""
RTCM Protocol core globals and constants

Created on 14 Feb 2022

Information sourced from RTCM STANDARD 10403.3 © 2016 RTCM

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

# pylint: disable=line-too-long

NMEA_HDR = [
    b"$V",
    b"$M",
    b"$P",
    b"$B",
    b"$D",
    b"$I",
    b"$L",
    b"$G",
    b"$F",
    b"$S",
    b"$H",
    b"$R",
    b"$E",
    b"$Y",
    b"$A",
    b"$C",
    b"$Z",
    b"$T",
    b"$W",
]
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
ERR_RAISE = 2
ERR_LOG = 1
ERR_IGNORE = 0
NA = "N/A"

NSAT = "NSat"
NSIG = "NSig"
NCELL = "NCell"
NRES = 16  # number of Residuals groups in MT1023 and MT1024
NHARMCOEFFC = "_NHarmCoeffC"  # number of cosine harmonic coefficients in 4076
NHARMCOEFFS = "_NHarmCoeffS"  # number of sine harmonic coefficients in 4076

# Power of 2 scaling constants
P2_P4 = 16  # 2**4
P2_4 = 0.0625  # 2**-4
P2_5 = 0.03125  # 2**-5
P2_6 = 0.015625  # 2**-6
P2_10 = 0.0009765625  # 2**-10
P2_11 = 0.00048828125  # 2**-11
P2_19 = 1.9073486328125e-06  # 2**-19
P2_20 = 9.5367431640625e-07  # 2**-20
P2_24 = 5.960464477539063e-08  # 2**-24
P2_28 = 3.725290298461914e-09  # 2**-28
P2_29 = 1.862645149230957e-09  # 2**-29
P2_30 = 9.313225746154785e-10  # 2**-30
P2_31 = 4.656612873077393e-10  # 2**-31
P2_32 = 2.3283064365386963e-10  # 2**-32
P2_33 = 1.1641532182693481e-10  # 2**-33
P2_34 = 5.820766091346741e-11  # 2**-34
P2_41 = 4.547473508864641e-13  # 2**-41
P2_43 = 1.1368683772161603e-13  # 2**-43
P2_46 = 1.4210854715202004e-14  # 2**-46
P2_50 = 8.881784197001252e-16  # 2**-50
P2_55 = 2.7755575615628914e-17  # 2**-55
P2_59 = 1.734723475976807e-18  # 2**-59
P2_66 = 1.3552527156068805e-20  # 2**-66

# ***************************************************
# THESE ARE THE RTCM PROTOCOL DATA TYPES
# ***************************************************
BIT = "BIT"  # bitfield
BITX = "BITX"  # variable bitfield
CHA = "CHA"  # characters, ISO 8859-1 (not limited to ASCII)
INT = "INT"  # 2’s complement integer
UINT = "UINT"  # unsigned integer
INTS = "SNT"  # sign-magnitude integer
UTF = "UTF"  # Unicode UTF-8 Code Unit
PRN = "PRN"  # Derived satellite PRN
CELPRN = "CPR"  # Derived cell PRN
CELSIG = "CSG"  # Derived cell Signal ID

# ****************************************************
# THESE ARE THE RTCM PROTOCOL DATA FIELDS
#
# DF key: (data_type, size in bits, resolution (scale factor), description)
# scale_factor of 0 means N/A (no scaling)
#
# NOTICE 1: These values are provided in semicircles;
#           multiply by π to use in orbit,  computations
#
# ****************************************************
RTCM_DATA_FIELDS = {
    "PRN": (PRN, 0, 0, "Derived satellite PRN"),
    "CELLPRN": (CELPRN, 0, 0, "Derived satellite PRN"),
    "CELLSIG": (CELSIG, 0, 0, "Derived satellite Signal ID"),
    "DF001": (BIT, 1, 0, "Reserved Field"),
    "DF001_1": (BIT, 1, 0, "Reserved 1 BIT, "),
    "DF001_2": (BIT, 2, 0, "Reserved 2 BIT, s"),
    "DF001_3": (BIT, 3, 0, "Reserved 3 BIT, s"),
    "DF001_7": (BIT, 7, 0, "Reserved 7 BIT, s"),
    "DF002": (UINT, 12, 0, "Message Number"),
    "DF003": (UINT, 12, 0, "Reference Station ID"),
    "DF004": (UINT, 30, 1, "GPS Epoch Time (TOW)"),
    "DF005": (BIT, 1, 0, "Synchronous GNSS Message Flag"),
    "DF006": (UINT, 5, 0, "No. of GPS Satellite Signals Processed"),
    "DF007": (BIT, 1, 0, "GPS Divergence-free Smoothing Indicator"),
    "DF008": (BIT, 3, 0, "GPS Smoothing Interval"),
    "DF009": (UINT, 6, 0, "GPS Satellite ID"),
    "DF010": (BIT, 1, 0, "GPS L1 Code Indicator"),
    "DF011": (UINT, 24, 0.02, "GPS L1 Pseudorange"),
    "DF012": (INT, 20, 0.0005, "GPS L1 PhaseRange - L1 Pseudorange"),
    "DF013": (UINT, 7, 0, "GPS L1 Lock Time Indicator"),
    "DF014": (UINT, 8, 0, "GPS Integer L1 Pseudorange Modulus Ambiguity"),
    "DF015": (UINT, 8, 0.25, "GPS L1 CNR"),
    "DF016": (BIT, 2, 0, "GPS L2 Code Indicator"),
    "DF017": (INT, 14, 0.02, "GPS L2-L1 Pseudorange Difference"),
    "DF018": (INT, 20, 0.0005, "GPS L2 PhaseRange - L1 Pseudorange"),
    "DF019": (UINT, 7, 0, "GPS L2 Lock Time Indicator"),
    "DF020": (UINT, 8, 0.25, "GPS L2 CNR"),
    "DF021": (UINT, 6, 0, "ITRF Realization Year"),
    "DF022": (BIT, 1, 0, "GPS Indicator"),
    "DF023": (BIT, 1, 0, "GLONASS Indicator"),
    "DF024": (BIT, 1, 0, "Galileo Indicator"),
    "DF025": (INT, 38, 0.0001, "Antenna Ref. Point, ECEF-X"),
    "DF026": (INT, 38, 0.0001, "Antenna Ref. Point, ECEF-Y"),
    "DF027": (INT, 38, 0.0001, "Antenna Ref. Point, ECEF-Z"),
    "DF028": (UINT, 16, 0.0001, "Antenna Height"),
    "DF029": (UINT, 8, 0, "Descriptor Counter"),
    "DF030": (CHA, 8, 0, "Antenna Descriptor"),
    "DF031": (UINT, 8, 0, "Antenna Setup ID"),
    "DF032": (UINT, 8, 0, "Serial Number Counter"),
    "DF033": (CHA, 8, 0, "Antenna Serial Number"),
    "DF034": (UINT, 27, 1, "GLONASS Epoch Time (tk)"),
    "DF035": (UINT, 5, 1, "No. of GLONASS Satellite Signals Processed"),
    "DF036": (BIT, 1, 0, "GLONASS Divergence-free Smoothing Indicator"),
    "DF037": (BIT, 3, 0, "GLONASS Smoothing Interval"),
    "DF038": (UINT, 6, 0, "GLONASS Satellite ID (Satellite Slot Number)"),
    "DF039": (BIT, 1, 0, "GLONASS L1 Code Indicator"),
    "DF040": (UINT, 5, 1, "GLONASS Satellite Frequency Channel Number"),
    "DF041": (UINT, 25, 0.02, "GLONASS L1 Pseudorange"),
    "DF042": (INT, 20, 0.0005, "GLONASS L1 PhaseRange - L1 Pseudorange"),
    "DF043": (UINT, 7, 0, "GLONASS L1 Lock Time Indicator"),
    "DF044": (
        UINT,
        7,
        0,
        "GLONASS Integer L1 Pseudorange Modulus Ambiguity",
    ),
    "DF045": (UINT, 8, 0.25, "GLONASS L1 CNR"),
    "DF046": (BIT, 2, 0, "GLONASS L2 Code Indicator"),
    "DF047": (INT, 14, 0.02, "GLONASS L2-L1 Pseudorange Difference"),
    "DF048": (INT, 20, 0.0005, "GLONASS L2 PhaseRange - L1 Pseudorange"),
    "DF049": (UINT, 7, 0, "GLONASS L2 Lock Time Indicator"),
    "DF050": (UINT, 8, 0.25, "GLONASS L2 CNR"),
    "DF051": (UINT, 16, 1, "Modified Julian Day (MJD) Number"),
    "DF052": (UINT, 17, 1, "Seconds of Day (UTC)"),
    "DF053": (UINT, 5, 1, "Number of Message ID Announcements to Follow (Nm)"),
    "DF054": (UINT, 8, 1, "Leap Seconds, GPS-UTC"),
    "DF055": (UINT, 12, 1, "Message ID"),
    "DF056": (BIT, 1, 0, "Message Sync Flag"),
    "DF057": (UINT, 16, 0.1, "Message Transmission Interval"),
    "DF058": (UINT, 5, 1, "Number of Auxiliary Stations Transmitted"),
    "DF059": (UINT, 8, 1, "Network ID"),
    "DF060": (UINT, 12, 1, "Master Reference Station ID"),
    "DF061": (UINT, 12, 1, "Auxiliary Reference Station ID"),
    "DF062": (INT, 20, 25 * 10**6, "Aux-Master Delta Latitude"),
    "DF063": (INT, 21, 25 * 10**6, "Aux-Master Delta Longitude"),
    "DF064": (INT, 23, 1, "Aux-Master Delta Height"),
    "DF065": (UINT, 23, 0.1, "GPS Epoch Time (GPS TOW)"),
    "DF066": (BIT, 1, 1, "GPS Multiple Message Indicator"),
    "DF067": (UINT, 4, 1, "Number of GPS Satellites"),
    "DF068": (UINT, 6, 1, "GPS Satellite ID"),
    "DF069": (INT, 17, 0.5, "GPS Ionospheric Carrier Phase Correction Difference"),
    "DF070": (INT, 17, 0.5, "GPS Geometric Carrier Phase Correction Difference"),
    "DF071": (BIT, 8, 1, "GPS IODE"),
    "DF072": (UINT, 4, 0, "Subnetwork ID"),
    "DF073": (UINT, 8, 0, "RESERVED for Provider ID"),
    "DF074": (BIT, 2, 0, "GPS Ambiguity Status Flag"),
    "DF075": (UINT, 3, 0, "GPS Non Sync Count"),
    "DF076": (UINT, 10, 0, "GPS Week number"),
    "DF077": (BIT, 4, 0, "GPS SV Acc. (URA)"),
    "DF078": (BIT, 2, 1, "GPS CODE ON L2"),
    "DF079": (INT, 14, P2_43, "GPS IDOT (Issue of Data, Time)"),  # see NOTICE 1 above
    "DF080": (UINT, 8, 1, "GPS IODE (Issue of Data, Ephemeris)"),
    "DF081": (UINT, 16, P2_P4, "GPS toc (Reference Time, Clock)"),
    "DF082": (INT, 8, P2_55, "GPS af2 (Clock correction drift rate)"),
    "DF083": (INT, 16, P2_43, "GPS af1 (Clock correction drift)"),
    "DF084": (INT, 22, P2_31, "GPS af0 (Clock correction bias)"),
    "DF085": (UINT, 10, 1, "GPS IODC (Issue of Data, Clock)"),
    "DF086": (
        INT,
        16,
        P2_5,
        "GPS Crs (Amplitude of sine harmonic correction term to the orbit, radius)",
    ),
    "DF087": (
        INT,
        16,
        P2_43,
        "GPS ∆n (Mean motion difference from computed value)",
    ),  # see NOTICE 1 above
    "DF088": (INT, 32, P2_31, "GPS M0 (Mean Anomaly)"),  # see NOTICE 1 above
    "DF089": (
        INT,
        16,
        P2_29,
        "GPS Cuc (Amplitude of cosine harmonic correction term to argument of latitude)",
    ),
    "DF090": (UINT, 32, P2_33, "GPS e (Eccentricity)"),
    "DF091": (
        INT,
        16,
        P2_29,
        "GPS Cus (Amplitude of sine harmonic correction term to argument of latitude)",
    ),
    "DF092": (UINT, 32, P2_19, "GPS A½ (Square root of Semi-major Axis)"),
    "DF093": (UINT, 16, P2_P4, "GPS toe (Reference Time, Ephemeris)"),
    "DF094": (
        INT,
        16,
        P2_29,
        "GPS Cic (Amplitude of cosine harmonic correction term to angle of inclination)",
    ),
    "DF095": (
        INT,
        32,
        P2_31,
        "GPS Ω0 (Longitude of Ascending Node)",
    ),  # see NOTICE 1 above
    "DF096": (
        INT,
        16,
        P2_29,
        "GPS Cis (Amplitude of sine harmonic correction term to angle of inclination)",
    ),
    "DF097": (INT, 32, P2_31, "GPS i0 (Inclination)"),  # see NOTICE 1 above
    "DF098": (
        INT,
        16,
        P2_5,
        "GPS Crc (Amplitude of cosine harmonic correction term to orbit,  radius)",
    ),
    "DF099": (INT, 32, P2_31, "GPS ω (Argument of Perigee)"),  # see NOTICE 1 above
    "DF100": (
        INT,
        24,
        P2_43,
        "GPS ΩDOT (Rate of Change of Right Ascension)",
    ),  # see NOTICE 1 above
    "DF101": (INT, 8, P2_31, "GPS tGD"),
    "DF102": (UINT, 6, 1, "GPS SV HEALTH"),
    "DF103": (BIT, 1, 1, "GPS L2 P data flag"),
    "DF104": (BIT, 1, 0, "GLONASS almanac health"),
    "DF105": (BIT, 1, 0, "GLONASS almanac health availability indicator"),
    "DF106": (BIT, 2, 0, "GLONASS P1"),
    "DF107": (BIT, 12, 0, "GLONASS tk"),
    "DF108": (BIT, 1, 0, "GLONASS MSB of Bn word"),
    "DF109": (BIT, 1, 0, "GLONASS P2"),
    "DF110": (UINT, 7, 1, "GLONASS tb"),
    "DF111": (INTS, 24, P2_20, "GLONASS xn(tb), first derivative"),
    "DF112": (INTS, 27, P2_11, "GLONASS xn(tb)"),
    "DF113": (INTS, 5, P2_30, "GLONASS xn(tb), second derivative"),
    "DF114": (INTS, 24, P2_20, "GLONASS yn(tb), first derivative"),
    "DF115": (INTS, 27, P2_11, "GLONASS yn(tb)"),
    "DF116": (INTS, 5, P2_30, "GLONASS yn(tb), second derivative"),
    "DF117": (INTS, 24, P2_20, "GLONASS zn(tb), first derivative"),
    "DF118": (INTS, 27, P2_11, "GLONASS zn(tb)"),
    "DF119": (INTS, 5, P2_30, "GLONASS zn(tb), second derivative"),
    "DF120": (BIT, 1, 0, "GLONASS P3"),
    "DF121": (INTS, 11, 0, "GLONASS γn(tb) (Relative deviation)"),
    "DF122": (BIT, 2, 0, "GLONASS-M P"),
    "DF123": (BIT, 1, 0, "GLONASS-M ln (third string)"),
    "DF124": (INTS, 22, 0, "GLONASS τn (tb)"),
    "DF125": (INTS, 5, 0, "GLONASS-M Δτn"),
    "DF126": (UINT, 5, 1, "GLONASS En"),
    "DF127": (BIT, 1, 0, "GLONASS-M P4"),
    "DF128": (UINT, 4, 0, "GLONASS-M FT"),
    "DF129": (UINT, 11, 1, "GLONASS-M NT"),
    "DF130": (BIT, 2, 0, "GLONASS-M M"),
    "DF131": (BIT, 1, 0, "GLONASS The Availability of Additional Data"),
    "DF132": (UINT, 11, 1, "GLONASS NA"),
    "DF133": (INTS, 32, 0, "GLONASS τc"),
    "DF134": (UINT, 5, 0, "GLONASS-M N4"),
    "DF135": (INTS, 22, 0, "GLONASS-M τGPS"),
    "DF136": (BIT, 1, 0, "GLONASS-M ln (fifth string)"),
    "DF137": (BIT, 1, 1, "GPS Fit Interval"),
    "DF138": (UINT, 7, 1, "Number of Characters to Follow"),
    "DF139": (UINT, 8, 1, "Number of UTF-8 Code Units"),
    "DF140": (UTF, 8, 0, "UTF-8 Character Code Units"),
    "DF141": (BIT, 1, 0, "Reference-Station Indicator"),
    "DF142": (BIT, 1, 0, "Single Receiver Oscillator Indicator"),
    "DF143": (UINT, 5, 0, "Source-Name Counter"),
    "DF144": (CHA, 8, 0, "Source-Name"),
    "DF145": (UINT, 5, 0, "Target-Name Counter"),
    "DF146": (CHA, 8, 0, "Target-Name"),
    "DF147": (UINT, 8, 0, "SystemIdentification Number"),
    "DF148": (BIT, 10, 0, "Utilized Tranformation Message Indicator"),
    "DF149": (UINT, 5, 0, "Plate Number"),
    "DF150": (UINT, 4, 0, "Computation Indicator"),
    "DF151": (UINT, 2, 0, "Height Indicator"),
    "DF152": (INT, 19, 2, "ΦV (Area of validity, lat)"),
    "DF153": (INT, 20, 2, "ΛV (Area of validity, lon)"),
    "DF154": (UINT, 14, 2, "∆ΦV (Area of validity, NS extension"),
    "DF155": (UINT, 14, 2, "∆ΛV (Area of validity, EW extension"),
    "DF156": (INT, 23, 0.001, "dX (Translation in X"),
    "DF157": (INT, 23, 0.001, "dY (Translation in Y)"),
    "DF158": (INT, 23, 0.001, "dZ (Translation in Z)"),
    "DF159": (INT, 32, 0.00002, "R1 (Rotation around X)"),
    "DF160": (INT, 32, 0.00002, "R2 (Rotation around Y)"),
    "DF161": (INT, 32, 0.00002, "R3 (Rotation around Z)"),
    "DF162": (INT, 25, 0.00002, "dS (Scale correction)"),
    "DF163": (INT, 35, 0.001, "XP (X-coord for Molodenski-Badekas rotation)"),
    "DF164": (INT, 35, 0.001, "YP (Y-coord for Molodenski-Badekas rotation)"),
    "DF165": (INT, 35, 0.001, "ZP (Z-coord for Molodenski-Badekas rotation)"),
    "DF166": (UINT, 24, 0.001, "add aS"),
    "DF167": (UINT, 25, 0.001, "add bS"),
    "DF168": (UINT, 24, 0.001, "add aT"),
    "DF169": (UINT, 25, 0.001, "add bT"),
    "DF170": (UINT, 6, 0, "Projection Type"),
    "DF171": (INT, 34, 0.000000011, "LaNO [°]"),
    "DF172": (INT, 35, 0.000000011, "LoNO [°]"),
    "DF173": (UINT, 30, 0.00001, "add SNO"),
    "DF174": (UINT, 36, 0.001, "FE"),
    "DF175": (INT, 35, 0.001, "FN"),
    "DF176": (INT, 34, 0.000000011, "LaFO [°]"),
    "DF177": (INT, 35, 0.000000011, "LoFO [°]"),
    "DF178": (INT, 34, 0.000000011, "LaSP1 [°]"),
    "DF179": (INT, 34, 0.000000011, "LaSP2 [°]"),
    "DF180": (UINT, 36, 0.001, "EFO"),
    "DF181": (INT, 35, 0.001, "NFO"),
    "DF182": (BIT, 1, 0, "Rectification Flag"),
    "DF183": (INT, 34, 0.000000011, "LaPC"),
    "DF184": (INT, 35, 0.000000011, "LoPC"),
    "DF185": (UINT, 35, 0.000000011, "AzIL"),
    "DF186": (INT, 26, 0.000000011, "Diff ARSG"),
    "DF187": (UINT, 30, 0.00001, "Add SIL"),
    "DF188": (UINT, 36, 0.001, "EPC"),
    "DF189": (INT, 35, 0.001, "NPC"),
    "DF190": (BIT, 1, 0, "Horizontal Shift Indicator"),
    "DF191": (BIT, 1, 0, "Vertical Shift Indicator"),
    "DF192": (INT, 21, 0.5, "Φ0"),
    "DF193": (INT, 22, 0.5, "Λ0"),
    "DF194": (UINT, 12, 0.5, "∆φ"),
    "DF195": (UINT, 12, 0.5, "∆λ"),
    "DF196": (INT, 8, 0.001, "Mean ∆φ"),
    "DF197": (INT, 8, 0.001, "Mean ∆λ"),
    "DF198": (INT, 15, 0.01, "Mean ∆H"),
    "DF199": (INT, 9, 0.00003, "δφi"),
    "DF200": (INT, 9, 0.00003, "δλi"),
    "DF201": (INT, 9, 0.001, "δhi"),
    "DF202": (INT, 25, 10, "N0"),
    "DF203": (UINT, 26, 10, "E0"),
    "DF204": (UINT, 12, 10, "∆N"),
    "DF205": (UINT, 12, 10, "∆E"),
    "DF206": (INT, 10, 0.01, "Mean ∆N"),
    "DF207": (INT, 10, 0.01, "Mean ∆E"),
    "DF208": (INT, 15, 0.01, "Mean ∆h"),
    "DF209": (INT, 9, 0.001, "δNi"),
    "DF210": (INT, 9, 0.001, "δEi"),
    "DF211": (INT, 9, 0.001, "δhi"),
    "DF212": (UINT, 2, 0, "Horizontal Interpolation Method Indicator"),
    "DF213": (UINT, 2, 0, "Vertical Interpolation Method Indicator"),
    "DF214": (UINT, 3, 0, "Horizontal Helmert/Molodenski Quality Indicator"),
    "DF215": (UINT, 3, 0, "Vertical Helmert/Molodenski Quality Indicator"),
    "DF216": (UINT, 3, 0, "Horizontal Grid Quality Indicator"),
    "DF217": (UINT, 3, 0, "Vertical Grid Quality Indicator"),
    "DF218": (UINT, 8, 0.5, "soc"),
    "DF219": (UINT, 9, 0.01, "sod"),
    "DF220": (UINT, 6, 0.1, "soh"),
    "DF221": (UINT, 10, 0.5, "sIc"),
    "DF222": (UINT, 10, 0.01, "sId"),
    "DF223": (UINT, 7, 0, "N-Refs"),
    "DF224": (UINT, 20, 1, "GPS Residuals Epoch Time (TOW)"),
    "DF225": (UINT, 17, 1, "GLONASS Residuals Epoch Time (tk)"),
    "DF226": (UINT, 12, 0, "Physical Reference Station ID"),
    "DF227": (UINT, 8, 0, "Receiver Type Descriptor Counter"),
    "DF228": (CHA, 8, 0, "Receiver Type Descriptor"),
    "DF229": (UINT, 8, 0, "Receiver Firmware Version Counter"),
    "DF230": (CHA, 8, 0, "Receiver Firmware Version"),
    "DF231": (UINT, 8, 0, "Receiver Serial Number Counter"),
    "DF232": (CHA, 8, 0, "Receiver Serial Number"),
    "DF233": (UINT, 20, 0.1, "GLONASS NW Epoch Time"),
    "DF234": (UINT, 4, 0, "Number of GLONASS Data Entries"),
    "DF235": (BIT, 2, 0, "GLONASS Ambiguity Status Flag"),
    "DF236": (UINT, 3, 0, "GLONASS Non Sync Count"),
    "DF237": (
        INT,
        17,
        0.5,
        "GLONASS Ionospheric Carrier Phase Correction Difference",
    ),
    "DF238": (INT, 17, 0.5, "GLONASS Geometric Carrier Phase Correction Difference"),
    "DF239": (BIT, 8, 0, "GLONASS IOD"),
    "DF240": (UINT, 20, 1, "GPS FKP Epoch Time"),
    "DF241": (UINT, 17, 1, "GLONASS FKP Epoch Time"),
    "DF242": (INT, 12, 0.01, "N0: Geometric Gradient in north (ppm)"),
    "DF243": (INT, 12, 0.01, "E0: Geometric gradient in east (ppm)"),
    "DF244": (INT, 14, 0.01, "NI: Ionospheric gradient in north  (ppm)"),
    "DF245": (INT, 14, 0.01, "EI: Ionospheric gradient in east  (ppm)"),
    # 'DF246-DF251': RESERVED,
    "DF248": (UINT, 30, 1, "Galileo Epoch Time (TOW)"),
    "DF252": (UINT, 6, 0, "Galileo Satellite ID"),
    "DF286": (BIT, 8, 0, "Galileo SISA (E1,E5b"),
    "DF287": (BIT, 2, 0, "Galileo E1-B Signal Health Status"),
    "DF288": (BIT, 1, 0, "Galileo E1-B Data Validity Status"),
    "DF289": (UINT, 12, 1, "Galileo Week Number"),
    "DF290": (UINT, 10, 1, "Galileo IODnav"),
    "DF291": (BIT, 8, 0, "Galileo SV SISA"),
    "DF292": (INT, 14, P2_43, "Galileo Rate of Inclination (IDOT)"),
    "DF293": (UINT, 14, 60, "Galileo toc"),
    "DF294": (INT, 6, P2_59, "Galileo af2"),
    "DF295": (INT, 21, P2_46, "Galileo af1"),
    "DF296": (INT, 31, P2_34, "Galileo af0"),
    "DF297": (INT, 16, P2_5, "Galileo Crs"),
    "DF298": (INT, 16, P2_43, "Galileo ∆n"),
    "DF299": (INT, 32, P2_31, "Galileo M0"),
    "DF300": (INT, 16, P2_29, "Galileo Cuc"),
    "DF301": (UINT, 32, P2_33, "Galileo Eccentricity (e)"),
    "DF302": (INT, 16, P2_29, "Galileo Cus"),
    "DF303": (UINT, 32, P2_19, "Galileo A½"),
    "DF304": (UINT, 14, 60, "Galileo toe"),
    "DF305": (INT, 16, P2_29, "Galileo Cic"),
    "DF306": (INT, 32, P2_31, "Galileo Ω0"),
    "DF307": (INT, 16, P2_29, "Galileo Cis"),
    "DF308": (INT, 32, P2_31, "Galileo i0"),
    "DF309": (INT, 16, P2_5, "Galileo Crc"),
    "DF310": (INT, 32, P2_31, "Galileo ω (Argument of Perigee)"),
    "DF311": (INT, 24, P2_43, "Galileo ΩDOT"),
    "DF312": (INT, 10, P2_32, "Galileo BGD (E1/E5a)"),
    "DF313": (INT, 10, P2_32, "Galileo BGD E5b/E1"),
    "DF314": (BIT, 2, 0, "Galileo E5a Signal Health Status"),
    "DF315": (BIT, 1, 0, "Galileo E5a Data Validity Status"),
    "DF316": (BIT, 2, 0, "Galileo SOL NAV Signal Health Status (SOLHS)"),
    "DF317": (BIT, 1, 0, "Galileo SOL NAV Data Validity Status (SOLDVS)"),
    # 'DF318-DF363': RESERVED,
    "DF364": (BIT, 2, 0, "Quarter Cycle Indicator"),
    "DF365": (INT, 22, 0.1, "Delta Radial"),
    "DF366": (INT, 20, 0.4, "Delta Along-Track"),
    "DF367": (INT, 20, 0.4, "Delta Cross-Track"),
    "DF368": (INT, 21, 0.001, "Dot Delta Radial"),
    "DF369": (INT, 19, 0.004, "Dot Delta AlongTrack"),
    "DF370": (INT, 19, 0.004, "Dot Delta CrossTrack"),
    "DF371": (INT, 27, 0.00002, "RESERVED for Dot Dot Delta Radial"),
    "DF372": (INT, 25, 0.00008, "RESERVED for Dot Dot DeltaAlong-Track"),
    "DF373": (INT, 25, 0.00008, "RESERVED for Dot Dot Delta Cross-Track"),
    "DF374": (BIT, 1, 0, "Satellite Reference Point"),
    "DF375": (BIT, 1, 0, "Satellite Reference Datum"),
    "DF376": (INT, 22, 0.1, "Delta Clock C0"),
    "DF377": (INT, 21, 0.001, "Delta Clock C1"),
    "DF378": (INT, 27, 0.00002, "Delta Clock C2"),
    "DF379": (UINT, 5, 1, "No. of Code Biases Processed"),
    "DF380": (UINT, 5, 1, "GPS Signal and Tracking Mode Identifier"),
    "DF381": (UINT, 5, 1, "GLONASS Signal and Tracking Mode Identifier"),
    "DF382": (UINT, 5, 1, "RESERVED for Galileo Signal and Tracking Mode Identifier"),
    "DF383": (INT, 14, 0.01, "Code Bias"),
    "DF384": (UINT, 5, 1, "GLONASS Satellite ID"),
    "DF385": (UINT, 20, 1, "GPS Epoch Time 1s"),
    "DF386": (UINT, 17, 1, "GLONASS Epoch Time 1s"),
    "DF387": (UINT, 6, 1, "No. of Satellites"),
    "DF388": (BIT, 1, 1, "Multiple Message Indicator"),
    "DF389": (BIT, 6, 0, "SSR URA"),
    "DF390": (INT, 22, 0.1, "High Rate Clock Correction"),
    "DF391": (BIT, 4, 1, "SSR Update Interval"),
    "DF392": (BIT, 8, 0, "GLONASS Issue Of Data (IOD)"),
    "DF393": (BIT, 1, 0, "MSM Multiple message bit"),
    "DF394": (BIT, 64, 0, "GNSS Satellite mask"),
    "DF395": (BIT, 32, 0, "GNSS Signal mask"),
    "DF396": (BITX, 0, 0, "GNSS Cell mask"),
    "DF397": (
        UINT,
        8,
        1,
        "The number of integer milliseconds in GNSS Satellite rough range",
    ),
    "DF398": (UINT, 10, P2_10, "GNSS Satellite rough range modulo 1 millisecond"),
    "DF399": (INT, 14, 1, "GNSS Satellite rough Phase Range Rate"),
    "DF400": (INT, 15, P2_24, "GNSS signal fine Pseudorange"),
    "DF401": (INT, 22, P2_29, "GNSS signal fine PhaseRange data"),
    "DF402": (UINT, 4, 0, "GNSS PhaseRange Lock Time Indicator"),
    "DF403": (UINT, 6, 1, "GNSS signal CNR"),
    "DF404": (INT, 15, 0.0001, "GNSS signal fine Phase Range Rate"),
    "DF405": (
        INT,
        20,
        P2_29,
        "GNSS signal fine Pseudorange with extended resolution",
    ),
    "DF406": (
        INT,
        24,
        P2_31,
        "GNSS signal fine PhaseRange data with extended resolution",
    ),
    "DF407": (
        UINT,
        10,
        0,
        "GNSS PhaseRange Lock Time Indicator with extended range and resolution.",
    ),
    "DF408": (UINT, 10, P2_4, "GNSS signal CNR with extended resolution"),
    "DF409": (UINT, 3, 1, "IODS - Issue Of Data Station"),
    # 'DF410': RESERVED,
    "DF411": (UINT, 2, 0, "Clock Steering Indicator"),
    "DF412": (UINT, 2, 0, "External Clock Indicator"),
    "DF413": (UINT, 4, 1, "IOD SSR"),
    "DF414": (UINT, 16, 1, "SSR Provider ID"),
    "DF415": (UINT, 4, 1, "SSR Solution ID"),
    "DF416": (UINT, 3, 1, "GLONASS Day Of Week"),
    "DF417": (BIT, 1, 0, "GNSS Smoothing Type Indicator"),
    "DF418": (BIT, 3, 0, "GNSS Smoothing Interval"),
    "DF419": (UINT, 4, 1, "GLONASS Satellite Frequency Channel Number"),
    "DF420": (BIT, 1, 0, "Half-cycle ambiguity indicator"),
    "DF421": (BIT, 1, 0, "GLONASS Code-Phase Bias Indicator"),
    "DF422_1": (BIT, 1, 0, "GLONASS FDMA Signals Mask L1 C/A"),
    "DF422_2": (BIT, 1, 0, "GLONASS FDMA Signals Mask L1 P"),
    "DF422_3": (BIT, 1, 0, "GLONASS FDMA Signals Mask L2 C/A"),
    "DF422_4": (BIT, 1, 0, "GLONASS FDMA Signals Mask L2 P"),
    "DF423": (INT, 16, 0.02, "GLONASS L1 C/A Code-Phase Bias"),
    "DF424": (INT, 16, 0.02, "GLONASS L1 P Code-Phase Bias"),
    "DF425": (INT, 16, 0.02, "GLONASS L2 C/A Code-Phase Bias"),
    "DF426": (INT, 16, 0.02, "GLONASS L2 P Code-Phase Bias"),
    "DF427": (UINT, 30, 1, "BeiDou Epoch Time (TOW)"),
    "DF428": (UINT, 30, 1, "QZSS Epoch Time (TOW)"),
    "DF429": (UINT, 4, 1, "QZSS Satellite ID"),
    "DF430": (UINT, 16, P2_P4, "QZSS toc"),
    "DF431": (INT, 8, P2_55, "QZSS af2"),
    "DF432": (INT, 16, P2_43, "QZSS af1"),
    "DF433": (INT, 22, P2_31, "QZSS af0"),
    "DF434": (UINT, 8, 1, "QZSS IODE"),
    "DF435": (INT, 16, P2_5, "QZSS Crs"),
    "DF436": (INT, 16, P2_43, "QZSS ∆n"),
    "DF437": (INT, 32, P2_31, "QZSS M0"),
    "DF438": (INT, 16, P2_29, "QZSS Cuc"),
    "DF439": (UINT, 32, P2_33, "QZSS e"),
    "DF440": (INT, 16, P2_29, "QZSS Cus"),
    "DF441": (UINT, 32, P2_19, "QZSS A½"),
    "DF442": (UINT, 16, P2_P4, "QZSS toe"),
    "DF443": (INT, 16, P2_29, "QZSS Cic"),
    "DF444": (INT, 32, P2_31, "QZSS Ω0"),
    "DF445": (INT, 16, P2_29, "QZSS Cis"),
    "DF446": (INT, 32, P2_31, "QZSS i0"),
    "DF447": (INT, 16, P2_5, "QZSS Crc"),
    "DF448": (INT, 32, P2_31, "QZSS ω (Argument of Perigee)"),
    "DF449": (INT, 24, P2_43, "QZSS ΩDOT (Rate of Right Ascension)"),
    "DF450": (INT, 14, P2_43, "QZSS i0-DOT"),
    "DF451": (BIT, 2, 1, "QZSS Codes on L2 Channel"),
    "DF452": (UINT, 10, 1, "QZSS Week Number"),
    "DF453": (UINT, 4, 0, "QZSS URA"),
    "DF454": (UINT, 6, 1, "QZSS SV health"),
    "DF455": (INT, 8, P2_31, "QZSS TGD"),
    "DF456": (UINT, 10, 1, "QZSS IODC"),
    "DF457": (BIT, 1, 1, "QZSS Fit Interval"),
    "DF488": (UINT, 6, 0, "BDS Satellite ID"),
    "DF489": (UINT, 13, 1, "BDS Week Number"),
    "DF490": (BIT, 4, 1, "BDS URAI"),
    "DF491": (INT, 14, P2_43, "BDS IDOT"),
    "DF492": (UINT, 5, 1, "BDS AODE"),
    "DF493": (UINT, 17, 8, "BDS Toc"),
    "DF494": (INT, 11, P2_66, "BDS a2"),
    "DF495": (INT, 22, P2_50, "BDS a1"),
    "DF496": (INT, 24, P2_33, "BSD a0"),
    "DF497": (UINT, 5, 1, "BDS AODC"),
    "DF498": (INT, 18, P2_6, "BDS Crs"),
    "DF499": (INT, 16, P2_43, "BDS ∆n"),
    "DF500": (INT, 32, P2_31, "BDS M0"),
    "DF501": (INT, 18, P2_31, "BDS Cuc"),
    "DF502": (UINT, 32, P2_33, "BDS e (Eccentricity)"),
    "DF503": (INT, 18, P2_31, "BDS Cus"),
    "DF504": (UINT, 32, P2_19, "BDS A½"),
    "DF505": (UINT, 17, 8, "BDS Toe"),
    "DF506": (INT, 18, P2_31, "BDS Cic"),
    "DF507": (INT, 32, P2_31, "BDS Ω0"),
    "DF508": (INT, 18, P2_31, "BDS Cis"),
    "DF509": (INT, 32, P2_31, "BDS i0"),
    "DF510": (INT, 18, P2_6, "BDS Crc"),
    "DF511": (INT, 32, P2_31, "BDS ω (Argument of Perigee)"),
    "DF512": (INT, 24, P2_43, "BDS ΩDOT (Rate of Right Ascension)"),
    "DF513": (INT, 10, 0.1, "BDS TGD1"),
    "DF514": (INT, 10, 0.1, "BDS TGD2"),
    "DF515": (BIT, 1, 1, "BSD SV Health"),
    "DF516": (UINT, 6, 1, "NAVIC/IRNSS Satellite ID"),
    "DF517": (UINT, 10, 1, "NAVIC/IRNSS Week Number (WN)"),
    "DF518": (INT, 22, P2_31, "NAVIC/IRNSS Clock Bias (af0)"),
    "DF519": (INT, 16, P2_43, "NAVIC/IRNSS Clock Drift (af1)"),
    "DF520": (INT, 8, P2_55, "NAVIC/IRNSS Clock Drift Rate (af2)"),
    "DF521": (UINT, 4, 1, "NAVIC/IRNSS SV Accuracy (URA)"),
    "DF522": (UINT, 16, 16, "NAVIC/IRNSS Time of Clock (toc)"),
    "DF523": (INT, 8, P2_31, "NAVIC/IRNSS Total Group Delay (TGD)"),
    "DF524": (INT, 22, P2_41, "NAVIC/IRNSS Mean Motion Difference (∆n)"),
    "DF525": (UINT, 8, 1, "NAVIC/IRNSS Issue of Data Ephemeric & Clock (IODEC)"),
    "DF526": (UINT, 10, 1, "NAVIC/IRNSS Reserved bits after IODEC"),
    "DF527": (BIT, 1, 1, "NAVIC/IRNSS L5 Flag"),
    "DF528": (BIT, 1, 1, "NAVIC/IRNSS S Flag"),
    "DF529": (INT, 15, P2_28, "NAVIC/IRNSS Cuc"),
    "DF530": (INT, 15, P2_28, "NAVIC/IRNSS Cus"),
    "DF531": (INT, 15, P2_28, "NAVIC/IRNSS Cic"),
    "DF532": (INT, 15, P2_28, "NAVIC/IRNSS Cis"),
    "DF533": (INT, 15, P2_4, "NAVIC/IRNSS Crc"),
    "DF534": (INT, 15, P2_4, "NAVIC/IRNSS Crs"),
    "DF535": (INT, 14, P2_43, "NAVIC/IRNSS IDOT"),
    "DF536": (INT, 32, P2_31, "NAVIC/IRNSS M0"),
    "DF537": (UINT, 16, 16, "NAVIC/IRNSS tOE"),
    "DF538": (UINT, 32, P2_33, "NAVIC/IRNSS e (Eccentricity)"),
    "DF539": (UINT, 32, P2_19, "NAVIC/IRNSS √A (Square root of semi major axis)"),
    "DF540": (INT, 32, P2_31, "NAVIC/IRNSS Ω0 (Long of Ascending Node)"),
    "DF541": (INT, 32, P2_31, "NAVIC/IRNSS ω (Argument of perigee)"),
    "DF542": (INT, 22, P2_41, "NAVIC/IRNSS ΩDOT (Rate of Right Ascension)"),
    "DF543": (INT, 32, P2_31, "NAVIC/IRNSS i0 (Inclination)"),
    "DF544": (BIT, 2, 1, "NAVIC/IRNSS 2 spare bits after IDOT"),
    "DF545": (BIT, 2, 1, "NAVIC/IRNSS 2 spare bits after i0"),
    "DF546": (UINT, 30, 1, "NAVIC/IRNSS Epoch Time (TOW)"),
    "ExtSatInfo": (UINT, 4, 0, "Extended Satellite Information"),
    # IGS SSR data types, used in 4076 messages
    # https://files.igs.org/pub/data/format/igs_ssr_v1.pdf
    "IDF001": (UINT, 3, 1, "IGM/IM Version"),
    "IDF002": (UINT, 8, 1, "IGS Message Number"),
    "IDF003": (UINT, 20, 1, "SSR Epoch Time 1s"),
    "IDF004": (BIT, 4, 1, "SSR Update Interval"),
    "IDF005": (BIT, 1, 1, "SSR Multiple Message Indicator"),
    "IDF006": (BIT, 1, 1, "Global/Regional CRS Indicator"),
    "IDF007": (UINT, 4, 1, "IOD SSR"),
    "IDF008": (UINT, 16, 1, "SSR Provider ID"),
    "IDF009": (UINT, 4, 1, "SSR Solution ID"),
    "IDF010": (UINT, 6, 1, "No. of Satellites"),
    "IDF011": (UINT, 6, 1, "GNSS Satellite ID"),
    "IDF012": (BIT, 8, 1, "GNSS IOD"),
    "IDF013": (INT, 22, 0.1, "Delta Orbit Radial"),
    "IDF014": (INT, 20, 0.4, "Delta Orbit Along-Track"),
    "IDF015": (INT, 20, 0.4, "Delta Orbit Cross-Track"),
    "IDF016": (INT, 21, 0.001, "Dot Orbit Delta Radial"),
    "IDF017": (INT, 19, 0.004, "Dot Orbit Delta Along-Track"),
    "IDF018": (INT, 19, 0.004, "Dot Orbit Delta Cross-Track"),
    "IDF019": (INT, 22, 0.1, "Delta Clock C0"),
    "IDF020": (INT, 21, 0.001, "Delta Clock C1"),
    "IDF021": (INT, 27, 0.00002, "Delta Clock C2"),
    "IDF022": (INT, 22, 0.1, "High Rate Clock Correction"),
    "IDF023": (UINT, 5, 1, "No. of Biases Processed"),
    "IDF024": (UINT, 5, 1, "GNSS Signal and Tracking Mode Identifier"),
    "IDF025": (INT, 14, 0.01, "Code Bias"),
    "IDF026": (UINT, 9, 1 / 256, "Yaw Angle"),
    "IDF027": (INT, 8, 1 / 8192, "Yaw Rate"),
    "IDF028": (INT, 20, 0.0001, "Phase Bias"),
    "IDF029": (BIT, 1, 1, "Signal Integer Indicator"),
    "IDF030": (BIT, 2, 1, "Signals Wide-Lane Integer Indicator"),
    "IDF031": (UINT, 4, 1, "Signal Discontinuity Counter"),
    "IDF032": (BIT, 1, 1, "Dispersive Bias Consistency Indicator"),
    "IDF033": (BIT, 1, 1, "MW Consistency Indicator"),
    "IDF034": (BIT, 6, 1, "SSR URA"),
    "IDF035": (UINT, 2, 1, "Number of Ionospheric Layers"),
    "IDF036": (UINT, 8, 10, "Height of Ionospheric Layer"),
    "IDF037": (UINT, 4, 1, "Spherical Harmonics Degree"),
    "IDF038": (UINT, 4, 1, "Spherical Harmonics Order"),
    "IDF039": (INT, 16, 0.005, "Spherical Harmonic Coefficient C"),
    "IDF040": (INT, 16, 0.005, "Spherical Harmonic Coefficient S"),
    "IDF041": (UINT, 9, 0.05, "VTEC Quality Indicator"),
}

# ***************************************************************************
# THESE ARE THE RTCM PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the rtcmtypes_* modules
# ***************************************************************************
RTCM_MSGIDS = {
    "1001": "GPS L1-Only RTK Observables",
    "1002": "GPS Extended L1-Only RTK Observables",
    "1003": "GPS L1&L2 RTK Observables",
    "1004": "GPS Extended L1&L2 RTK Observables",
    "1005": "Stationary RTK Reference Station ARP",
    "1006": "Stationary RTK Reference Station ARP with Antenna Height",
    "1007": "Antenna Descriptor",
    "1008": "Antenna Descriptor & Serial Number",
    "1009": "GLONASS L1-Only RTK Observables",
    "1010": "GLONASS Extended L1-Only RTK Observables",
    "1011": "GLONASS L1&L2 RTK Observables",
    "1012": "GLONASS Extended L1&L2 RTK Observables",
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
    "1041": "NavIC/IRNSS Ephemerides",
    "1042": "Beidou Ephemerides",
    "1044": "QZSS Ephemerides",
    "1045": "Galileo F/NAV Ephemerides",
    "1046": "Galileo I/NAV Ephemerides",
    "1057": "GPS SSROrBIT,  Correction",
    "1058": "GPS SSR Clock Correction",
    "1059": "GPS SSR Code Bias",
    "1060": "GPS SSR Combined OrBIT,  and Clock Corrections",
    "1061": "GPS SSR URA",
    "1062": "GPS SSR High Rate Clock Correction",
    "1063": "GLONASS SSR OrBIT,  Correction",
    "1064": "GLONASS SSR Clock Correction",
    "1065": "GLONASS SSR Code Bias",
    "1066": "GLONASS SSR Combined OrBIT,  and Clock Correction",
    "1067": "GLONASS SSR URA",
    "1068": "GLONASS SSR High Rate Clock Correction",
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
    "1128": "Reserved MSM",
    "1129": "Reserved MSM",
    "1130": "Reserved MSM",
    "1131": "IRNSS MSM1",
    "1132": "IRNSS MSM2",
    "1133": "IRNSS MSM3",
    "1134": "IRNSS MSM4",
    "1135": "IRNSS MSM5",
    "1136": "IRNSS MSM6",
    "1137": "IRNSS MSM7",
    # "1138-1229":"Reserved MSM",
    "1230": "GLONASS L1 and L2 Code-Phase Biases",
    # "1240-1263": "SSR Messages"
    #
    # NB: Only those proprietary messages with public
    # domain definitions have been implemented.
    #
    # "4001-4095": "Proprietary Messages",
    # "4072": "Mitsubishi Electric Corp",
    # "4073": "Unicore Communications Inc",
    # "4075": "Alberding GmbH",
    # "4076": "International GNSS Service (IGS)",
    "4076_021": "GPS SSR OrBIT,  Correction",
    "4076_022": "GPS SSR Clock Correction",
    "4076_023": "GPS SSR Combined OrBIT,  and Clock Correction",
    "4076_024": "GPS SSR High Rate Clock Correction",
    "4076_025": "GPS SSR Code Bias",
    "4076_026": "GPS SSR Phase Bias",
    "4076_027": "GPS SSR URA",
    # "4076_028-040": "Reserved for GPS",
    "4076_041": "GLONASS SSR OrBIT,  Correction",
    "4076_042": "GLONASS SSR Clock Correction",
    "4076_043": "GLONASS SSR Combined OrBIT,  and Clock Correction",
    "4076_044": "GLONASS SSR High Rate Clock Correction",
    "4076_045": "GLONASS SSR Code Bias",
    "4076_046": "GLONASS SSR Phase Bias",
    "4076_047": "GLONASS SSR URA",
    # "4076_048-060": "Reserved for GLONASS",
    "4076_061": "Galileo SSR OrBIT,  Correction",
    "4076_062": "Galileo SSR Clock Correction",
    "4076_063": "Galileo SSR Combined OrBIT,  and Clock Correction",
    "4076_064": "Galileo SSR High Rate Clock Correction",
    "4076_065": "Galileo SSR Code Bias",
    "4076_066": "Galileo SSR Phase Bias",
    "4076_067": "Galileo SSR URA",
    # "4076_068-080": "Reserved for Galileo",
    "4076_081": "QZSS SSR OrBIT,  Correction",
    "4076_082": "QZSS SSR Clock Correction",
    "4076_083": "QZSS SSR Combined OrBIT,  and Clock Correction",
    "4076_084": "QZSS SSR High Rate Clock Correction",
    "4076_085": "QZSS SSR Code Bias",
    "4076_086": "QZSS SSR Phase Bias",
    "4076_087": "QZSS SSR URA",
    # "4076_088-100": "Reserved for QZSS",
    "4076_101": "BeiDou SSR OrBIT,  Correction",
    "4076_102": "BeiDou SSR Clock Correction",
    "4076_103": "BeiDou SSR Combined OrBIT,  and Clock Correction",
    "4076_104": "BeiDou SSR High Rate Clock Correction",
    "4076_105": "BeiDou SSR Code Bias",
    "4076_106": "BeiDou SSR Phase Bias",
    "4076_107": "BeiDou SSR URA",
    # "4076_108-120": "Reserved for BeiDou",
    "4076_121": "SBAS SSR OrBIT,  Correction",
    "4076_122": "SBAS SSR Clock Correction",
    "4076_123": "SBAS SSR Combined OrBIT,  and Clock Correction",
    "4076_124": "SBAS SSR High Rate Clock Correction",
    "4076_125": "SBAS SSR Code Bias",
    "4076_126": "SBAS SSR Phase Bias",
    "4076_127": "SBAS SSR URA",
    # "4076_128-140": "Reserved for SBAS",
    # "4076_141-160": "Reserved for NavIC/IRNSS",
    # "4076_161-200": "Reserved",
    "4076_201": "GNSS SSR Ionosphere VTEC Spherical Harmonics",
    # "4077": "Hemisphere GNSS Inc.",
    # "4078": "ComNav Technology Ltd.",
    # "4079": "SubCarrier Systems Corp. (SCSC) The makers of SNIP",
    # "4080": "NavCom Technology, Inc.",
    # "4081": "Seoul National University GNSS Lab",
    # "4082": "Cooperative Research Centre for Spatial Information",
    # "4083": "German Aerospace Center, Institute of Communications and Navigation (DLR)",
    # "4084": "Geodetics, Inc.",
    # "4085": "European GNSS Supervisory Authority",
    # "4086": "inPosition GmbH",
    # "4087": "Fugro",
    # "4088": "IfEN GmbH",
    # "4089": "Septentrio Satellite Navigation",
    # "4090": "Geo++",
    # "4091": "Topcon Positioning Systems",
    # "4092": "Leica Geosystems",
    # "4093": "NovAtel Inc.",
    # "4094": "Trimble Navigation Ltd.",
    # "4095": "Ashtech",
}

# map of MSM msg identity to GNSS name, epoch attribute name
GNSSMAP = {
    "107": ("GPS", "DF004"),
    "108": ("GLONASS", "DF034"),
    "109": ("GALILEO", "DF248"),
    "110": ("SBAS", "DF004"),
    "111": ("QZSS", "DF428"),
    "112": ("BEIDOU", "DF427"),
    "113": ("NAVIC", "DF546"),
}

# map of 4076_201 coefficients
COEFFS = {
    0: ("IDF039", "Cosine Coefficients"),
    1: ("IDF040", "Sine Coefficients"),
}
