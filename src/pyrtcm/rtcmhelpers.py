"""
Collection of RTCM helper methods which can be used
outside the RTCMMessage or RTCMReader classes

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from datetime import datetime, timedelta

from pyrtcm.rtcmtypes_core import COEFFS, GNSSMAP, RTCM_DATA_FIELDS


def att2idx(att: str) -> int:
    """
    Get integer index corresponding to grouped attribute.

    e.g. DF389_06 -> 6; DF406_103 -> 103

    :param str att: grouped attribute name e.g. DF406_01
    :return: index as integer, or 0 if not grouped
    :rtype: int
    """

    try:
        return int(att[att.rindex("_") - len(att) + 1 :])
    except ValueError:
        return 0


def att2name(att: str) -> str:
    """
    Get name of grouped attribute.

    e.g. DF389_06 -> DF389; DF406_103 -> DF406

    :param str att: grouped attribute name e.g. DF406_01
    :return: name without index e.g. DF406
    :rtype: str
    """

    try:
        return att[: att.rindex("_")]
    except ValueError:
        return att


def bits2val(att: str, scale: float, bitfield: int) -> object:
    """
    Convert bitfield to value for given attribute type.

    :param str att: attribute type e.g. "UNT008"
    :param float scale: scaling factor (where defined)
    :param int bitfield: attribute as integer
    :return: value
    :rtype: object (int, float, char, bool)
    """

    typ = atttyp(att)
    siz = attsiz(att)
    val = msb = 0

    if typ in ("SNT", "INT"):
        msb = 2 ** (siz - 1)
    if typ == "SNT":  # int, MSB indicates sign
        val = bitfield & msb - 1
        if bitfield & msb:
            val *= -1
    else:  # all other types
        val = bitfield
    if typ == "INT" and (bitfield & msb):  # 2's compliment -ve int
        val = val - (1 << siz)
    if typ in ("CHA", "UTF"):  # ASCII or UTF-8 character
        val = chr(val)
    # apply any scaling factor
    else:
        if scale not in (0, 1):
            val *= scale

    return val


def calc_crc24q(message: bytes) -> int:
    """
    Perform CRC24Q cyclic redundancy check.

    If the message includes the appended CRC bytes, the
    function will return 0 if the message is valid.
    If the message excludes the appended CRC bytes, the
    function will return the applicable CRC.

    :param bytes message: message
    :return: CRC or 0
    :rtype: int

    """

    poly = 0x1864CFB
    crc = 0
    for octet in message:
        crc ^= octet << 16
        for _ in range(8):
            crc <<= 1
            if crc & 0x1000000:
                crc ^= poly
    return crc & 0xFFFFFF


def crc2bytes(message: bytes) -> bytes:
    """
    Generate CRC as 3 bytes, suitable for
    constructing RTCM message transport.

    :param bytes message: message including header & length but _without_ CRC
    :return: CRC as 3 bytes
    :rtype: bytes
    """

    return calc_crc24q(message).to_bytes(3, "big")


def len2bytes(payload: bytes) -> bytes:
    """
    Generate payload length as 2 bytes, suitable for
    constructing RTCM message transport.

    :param bytes payload: message payload (i.e. _without_ header, length or CRC)
    :return: payload length as 2 bytes padded with leading zeros
    :rtype: bytes
    """

    return len(payload).to_bytes(2, "big")


def atttyp(att: str) -> str:
    """
    Get attribute type as string.

    :param str att: attribute type e.g. 'UNT002'
    :return: type of attribute as string e.g. 'UNT'
    :rtype: str

    """

    return att[0:3]


def attsiz(att: str) -> int:
    """
    Get attribute size in bits.

    :param str att: attribute type e.g. 'U002'
    :return: size of attribute in bits
    :rtype: int

    """

    return int(att[-3:])


def datasiz(datafield: str) -> int:
    """
    Get data field size in bits.

    :param str datafield: datafield e.g. 'DF234'
    :return: size of data field in bits
    :rtype: int

    """

    (att, _, _) = RTCM_DATA_FIELDS[datafield[0:5]]
    return attsiz(att)


def datascale(datafield: str) -> float:
    """
    Get scaling factor of data field.

    :param str datafield: datafield e.g. 'DF234'
    :return: datafield scale factor or 0 if N/A
    :rtype: float
    """

    (_, res, _) = RTCM_DATA_FIELDS[datafield[0:5]]
    return res


def datadesc(datafield: str) -> str:
    """
    Get description of data field.

    :param str datafield: datafield e.g. 'DF234'
    :return: datafield description
    :rtype: str
    """

    (_, _, desc) = RTCM_DATA_FIELDS[datafield[0:5]]
    return desc


def get_bit(data: bytes, num: int) -> int:
    """
    Get specified bit from bytes.

    :param bytes data: data
    :param int num: bit position
    :return: selected bit value
    :rtype: int
    """

    base = int(num // 8)
    shift = 7 - int(num % 8)
    return (data[base] >> shift) & 0x1


def tow2utc(tow: int) -> datetime.time:
    """
    Convert GPS Time Of Week to UTC time
    (UTC = GPS - 18 seconds; correct as from 1/1/2017).

    :param int tow: GPS Time Of Week
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = datetime(1980, 1, 6) + timedelta(seconds=(tow / 1000) - 18)
    return utc.time()


def hextable(raw: bytes, cols: int = 8) -> str:
    """
    Formats raw (binary) message in tabular hexadecimal format e.g.

    000: 2447 4e47 5341 2c41 2c33 2c33 342c 3233 | b'$GNGSA,A,3,34,23' |

    :param bytes raw: raw (binary) data
    :param int cols: number of columns in hex table (8)
    :return: table of hex data
    :rtype: str
    """

    hextbl = ""
    colw = cols * 4
    rawh = raw.hex()
    for i in range(0, len(rawh), colw):
        rawl = rawh[i : i + colw].ljust(colw, " ")
        hextbl += f"{int(i/2):03}: "
        for col in range(0, colw, 4):
            hextbl += f"{rawl[col : col + 4]} "
        hextbl += f" | {bytes.fromhex(rawl)} |\n"

    return hextbl


def escapeall(val: bytes) -> str:
    """
    Escape all byte characters e.g. b'\\\\x73' rather than b`s`

    :param bytes val: bytes
    :return: string of escaped bytes
    :rtype: str
    """

    return "b'{}'".format("".join(f"\\x{b:02x}" for b in val))


def parse_msm(msg: object) -> tuple:
    """
    Parse individual MSM message into iterable data arrays.

    :param RTCMMessage msg: RTCM MSM Message
    :return: tuple of (metadata, sat data array, cell data array)
    :rtype: tuple
    """

    if not msg.ismsm:
        return None

    meta = {}
    gmap = GNSSMAP[msg.identity[0:3]]
    meta["identity"] = msg.identity
    meta["gnss"] = gmap[0]
    meta["station"] = msg.DF003
    meta["epoch"] = getattr(msg, gmap[1])
    meta["sats"] = msg.NSat
    meta["cells"] = msg.NCell
    msmsats = []
    for i in range(1, msg.NSat + 1):  # iterate through satellites
        sats = {}
        for attr in ["PRN", "DF397", "DF398", "DF399", "DF419", "ExtSatInfo"]:
            if hasattr(msg, f"{attr}_{i:02d}"):
                sats[attr] = getattr(msg, f"{attr}_{i:02d}")
        msmsats.append(sats)
    msmcells = []
    for i in range(1, msg.NCell + 1):  # iterate through cells (satellite/signal)
        cells = {}
        for attr in [
            "CELLPRN",
            "CELLSIG",
            "DF400",
            "DF401",
            "DF402",
            "DF403",
            "DF404",
            "DF405",
            "DF406",
            "DF407",
            "DF408",
            "DF420",
        ]:
            if hasattr(msg, f"{attr}_{i:02d}"):
                cells[attr] = getattr(msg, f"{attr}_{i:02d}")
        msmcells.append(cells)

    return (meta, msmsats, msmcells)


def parse_4076_201(msg: object):
    """
    Parse individual 4076_201 message into iterable data arrays.

    :param RTCMMessage parsed: parsed 4076_201 message
    :return: dict of {metadata, [cosine coefficients], [sine coefficients]} for each layer
    :rtype: dict
    """

    if msg.identity != "4076_201":
        return None

    hmc = {}
    # for each ionospheric layer
    for lyr in range(msg.IDF035 + 1):  # number of ionospheric layers
        hmc[lyr] = {}
        hmc[lyr]["Layer Height"] = getattr(msg, f"IDF036_{lyr+1:02d}")
        # for each coefficient (cosine & sine)
        for field, coeff in COEFFS.values():
            hmc[lyr][coeff] = []
            i = 0
            eof = False
            # for each coefficient value
            while not eof:
                try:
                    hmc[lyr][coeff].append(
                        getattr(msg, f"{field}_{lyr+1:02d}_{i+1:02d}")
                    )
                    i += 1
                except AttributeError:
                    eof = True

    return hmc
