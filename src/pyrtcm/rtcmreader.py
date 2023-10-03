"""
RTCMReader class.

Reads and parses individual RTCM3 messages from any stream
which supports a read(n) -> bytes method.

RTCM3 transport layer bit format:

+--------+--------+---------+---------+----------------+---------+
|  0xd3  | 000000 | length  |  type   |    content     |   crc   |
+========+========+=========+=========+================+=========+
| 8 bits | 6 bits | 10 bits | 12 bits |    variable    | 24 bits |
+--------+--------+---------+---------+----------------+---------+
|                           |   payload; length x 8    |         |
+--------+--------+---------+---------+----------------+---------+

Returns both the raw binary data (as bytes) and the parsed data
(as RTCMMessage object).

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from socket import socket

import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt
from pyrtcm.rtcmhelpers import calc_crc24q
from pyrtcm.rtcmmessage import RTCMMessage
from pyrtcm.socket_stream import SocketStream


class RTCMReader:
    """
    rtcmReader class.
    """

    def __init__(
        self,
        datastream,
        validate: int = rtt.VALCKSUM,
        quitonerror: int = rtt.ERR_LOG,
        scaling: bool = True,
        labelmsm: int = 1,
        bufsize: int = 4096,
        errorhandler: object = None,
    ):  # pylint: disable=too-many-arguments
        """Constructor.

        :param datastream stream: input data stream
        :param int validate: 0 = ignore invalid checksum, 1 = validate checksum (1)
        :param int quitonerror: 0 = ignore,  1 = log and continue, 2 = (re)raise (1)
        :param bool scaling: apply attribute scaling True/False (True)
        :param int labelmsm: whether to label MSM NSAT and NCELL attributes (0 = none, 1 = RINEX, 2 = freq)
        :param int bufsize: socket recv buffer size (4096)
        :param object errorhandler: error handling object or function (None)
        :raises: RTCMStreamError (if mode is invalid)
        """

        if isinstance(datastream, socket):
            self._stream = SocketStream(datastream, bufsize=bufsize)
        else:
            self._stream = datastream
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._validate = validate
        self._scaling = scaling
        self._labelmsm = labelmsm

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as RTCMMessage)
        :rtype: tuple
        :raises: StopIteration
        """

        (raw_data, parsed_data) = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(self) -> tuple:
        """
        Read a single RTCM message from the stream buffer
        and return both raw and parsed data.

        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as RTCMMessage)
        :rtype: tuple
        :raises: RTCMStreamError (if unrecognised protocol in data stream)
        """

        parsing = True

        try:
            while parsing:  # loop until end of valid message or EOF
                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                # if not rtcm, NMEA or RTCM3, discard and continue
                if byte1 not in (b"\xb5", b"\x24", b"\xd3"):
                    continue
                byte2 = self._read_bytes(1)
                bytehdr = byte1 + byte2
                # if it's a UBX message (b'\xb5\x62'), ignore it
                if bytehdr == rtt.UBX_HDR:
                    (raw_data, parsed_data) = self._parse_ubx(bytehdr)
                    continue
                # if it's an NMEA message ('$G' or '$P'), ignore it
                if bytehdr in rtt.NMEA_HDR:
                    (raw_data, parsed_data) = self._parse_nmea(bytehdr)
                    continue
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                if byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    (raw_data, parsed_data) = self._parse_rtcm3(bytehdr)
                    parsing = False
                # unrecognised protocol header
                else:
                    continue

        except EOFError:
            return (None, None)
        except (
            rte.RTCMMessageError,
            rte.RTCMParseError,
            rte.RTCMStreamError,
            rte.RTCMTypeError,
        ) as err:
            if self._quitonerror:
                self._do_error(str(err))
            parsed_data = str(err)

        return (raw_data, parsed_data)

    def _parse_ubx(self, hdr: bytes) -> tuple:
        """
        Parse remainder of UBX message.

        :param bytes hdr: UBX header (b'\xb5\x62')
        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or None)
        :rtype: tuple
        """

        # read the rest of the UBX message from the buffer
        byten = self._read_bytes(4)
        clsid = byten[0:1]
        msgid = byten[1:2]
        lenb = byten[2:4]
        leni = int.from_bytes(lenb, "little", signed=False)
        byten = self._read_bytes(leni + 2)
        plb = byten[0:leni]
        cksum = byten[leni : leni + 2]
        raw_data = hdr + clsid + msgid + lenb + plb + cksum
        parsed_data = None
        return (raw_data, parsed_data)

    def _parse_nmea(self, hdr: bytes) -> tuple:
        """
        Parse remainder of NMEA message.

        :param bytes hdr: NMEA header ($G or $P)
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage or None)
        :rtype: tuple
        """

        # read the rest of the NMEA message from the buffer
        byten = self._read_line()  # NMEA protocol is CRLF-terminated
        raw_data = hdr + byten
        parsed_data = None
        return (raw_data, parsed_data)

    def _parse_rtcm3(self, hdr: bytes) -> tuple:
        """
        Parse any RTCM3 data in the stream.

        :param bytes hdr: first 2 bytes of RTCM3 header
        :return: tuple of (raw_data as bytes, parsed_stub as RTCMMessage)
        :rtype: tuple
        """

        hdr3 = self._read_bytes(1)
        size = (hdr[1] << 8) | hdr3[0]
        payload = self._read_bytes(size)
        crc = self._read_bytes(3)
        raw_data = hdr + hdr3 + payload + crc
        parsed_data = self.parse(
            raw_data,
            validate=self._validate,
            scaling=self._scaling,
            labelmsm=self._labelmsm,
        )
        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) < size:  # EOF
            raise EOFError()
        return data

    def _read_line(self) -> bytes:
        """
        Read until end of line (CRLF).

        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.readline()
        if data[-2:] != b"\x0d\x0a":
            raise EOFError()
        return data

    def _do_error(self, err: str):
        """
        Handle error.

        :param str err: error message
        :raises: RTCMParseError if quitonerror = 2
        """

        if self._quitonerror == rtt.ERR_RAISE:
            raise rte.RTCMParseError(err)
        if self._quitonerror == rtt.ERR_LOG:
            # pass to error handler if there is one
            if self._errorhandler is None:
                print(err)
            else:
                self._errorhandler(err)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(
        message: bytes,
        validate: int = rtt.VALCKSUM,
        scaling: bool = True,
        labelmsm: int = 1,
    ) -> "RTCMMessage":
        """
        Parse RTCM message to RTCMMessage object.

        :param bytes message: RTCM raw message bytes
        :param int validate: 0 = don't validate CRC, 1 = validate CRC (1)
        :param bool scaling: apply attribute scaling True/False (True)
        :param int labelmsm: whether to label MSM NSAT and NCELL attributes (0 = none, 1 = RINEX, 2 = freq)
        :return: RTCMMessage object
        :rtype: RTCMMessage
        :raises: RTCMParseError (if data stream contains invalid data or unknown message type)
        """
        # pylint: disable=unused-argument

        if validate & rtt.VALCKSUM:
            if calc_crc24q(message):
                raise rte.RTCMParseError(
                    f"RTCM3 message invalid - failed CRC: {message[-3:]}"
                )
        payload = message[3:-3]
        return RTCMMessage(payload=payload, scaling=scaling, labelmsm=labelmsm)
