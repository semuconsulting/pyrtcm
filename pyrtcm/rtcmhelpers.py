"""
Collection of RTCM helper methods which can be used
outside the RTCMMessage or RTCMReader classes

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import logging
from datetime import datetime, timedelta
from pyrtcm.rtcmtypes_core import RTCM_DATA_FIELDS


def bits2val(att: str, res: float, bitfield: list) -> object:
    """
    Convert bit array to value for this attribute type.

    :param str att: attribute type e.g. "UNT008"
    :param float res: resolution (where defined)
    :param list bitfield: array of bits representing attribute
    :return: value
    :rtype: object (int, float, char, bool)
    """

    typ = atttyp(att)
    siz = attsiz(att)
    logging.debug("Att type %s, size: %s", typ, siz)

    val = 0
    if typ == "SNT":  # int, MSB indicates sign
        for bit in bitfield[1:]:
            val = (val << 1) | bit
        if bitfield[0]:
            val *= -1
    else:  # all other types
        for bit in bitfield:
            val = (val << 1) | bit
    if typ == "INT" and bitfield[0]:  # 2's compliment -ve int
        val = val - (1 << siz)
    # TODO apply any scaling factor (res) here?
    elif typ in ("CHA", "UTF"):  # ASCII or UTF-8 character
        val = chr(val)

    return val


def num_setbits(bitfield: list) -> int:
    """
    Get number of set bits in bitfield.

    :param list bitfield: array of bits
    :return: number of bits set
    :rtype: int
    """

    n = 0
    for bf in bitfield:
        if bf:
            n += 1
    return n


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

    POLY = 0x1864CFB
    crc = 0
    for octet in message:
        crc ^= octet << 16
        for _ in range(8):
            crc <<= 1
            if crc & 0x1000000:
                crc ^= POLY
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


def datares(datafield: str) -> float:
    """
    Get resolution (scaling factor) of data field.

    :param str datafield: datafield e.g. 'DF234'
    :return: datafield resolution or 0 if N/A
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


def get_bitarray(data: bytes) -> list:
    """
    Convert data bytes to bit array.

    :param bytes data: data
    :return: bit array
    :rtype: list
    """

    return [get_bit(data, i) for i in range(len(data) * 8)]


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
