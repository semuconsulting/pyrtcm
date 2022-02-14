"""
Collection of RTCM helper methods which can be used
outside the RTCMMessage or RTCMReader classes

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

from datetime import datetime, timedelta
from pyrtcm.rtcmtypes_core import RTCM_DATA_TYPES


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


def crc_2_bytes(message: bytes) -> bytes:
    """
    Generate CRC as 3 bytes, suitable for
    constructing RTCM message transport.

    :param bytes message: message _without_ CRC
    :return: CRC as 3 bytes
    :rtype: bytes
    """

    return calc_crc24q(message).to_bytes(3, "big")


def len_2_bytes(payload: bytes) -> bytes:
    """
    Generate payload length as 2 bytes, suitable for
    constructing RTCM message transport.

    :param bytes payload: message payload (i.e. _without_ header, length or CRC)
    :return: CRC as 2 bytes
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

    :param str datafield: attribute type e.g. 'UNT012'
    :return: size of data field in bits
    :rtype: int

    """

    (att, _) = RTCM_DATA_TYPES[datafield]
    return attsiz(att)


def datadesc(datafield: str) -> str:
    """
    Get description of data field.

    :param str datafield: attribute type e.g. 'UNT012'
    :return: datafield description
    :rtype: str
    """

    (_, desc) = RTCM_DATA_TYPES[datafield]
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


def bits_2_val(bits: list) -> int:
    """
    Convert bit array to integer.

    :param list bits: bit array
    :return: integer value
    :rtype: int
    """

    val = 0
    for bit in bits:
        val = (val << 1) | bit
    return val


def itow2utc(itow: int) -> datetime.time:
    """
    Convert GPS Time Of Week to UTC time
    (UTC = GPS - 18 seconds; correct as from 1/1/2017).

    :param int itow: GPS Time Of Week
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = datetime(1980, 1, 6) + timedelta(seconds=(itow / 1000) - 18)
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
