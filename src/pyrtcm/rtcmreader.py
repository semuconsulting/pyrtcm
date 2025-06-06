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

from logging import getLogger
from socket import socket

from pyrtcm.exceptions import (
    RTCMMessageError,
    RTCMParseError,
    RTCMStreamError,
    RTCMTypeError,
)
from pyrtcm.rtcmhelpers import calc_crc24q
from pyrtcm.rtcmmessage import RTCMMessage
from pyrtcm.rtcmtypes_core import (
    ENCODE_NONE,
    ERR_LOG,
    ERR_RAISE,
    VALCKSUM,
)
from pyrtcm.socketwrapper import SocketWrapper


class RTCMReader:
    """
    rtcmReader class.
    """

    def __init__(
        self,
        datastream,
        validate: int = VALCKSUM,
        quitonerror: int = ERR_LOG,
        labelmsm: int = 1,
        bufsize: int = 4096,
        parsed: bool = True,
        errorhandler: object = None,
        encoding: int = ENCODE_NONE,
    ):  # pylint: disable=too-many-arguments
        """Constructor.

        :param datastream stream: input data stream
        :param int validate: 0 = ignore invalid checksum, 1 = validate checksum (1)
        :param int quitonerror: ERR_IGNORE (0) = ignore errors,  ERR_LOG (1) = log continue,
            ERR_RAISE (2) = (re)raise (1)
        :param int labelmsm: MSM NSAT and NCELL attribute label (1 = RINEX, 2 = freq)
        :param int bufsize: socket recv buffer size (4096)
        :param bool parsed: 1 = return raw and parsed data, 0 = return only raw data \
            (parsed = None) (1)
        :param object errorhandler: error handling object or function (None)
        :param int encoding: encoding for socket stream \
            (0 = none, 1 = chunk, 2 = gzip, 4 = compress, 8 = deflate (can be OR'd)) (0)
        :raises: RTCMStreamError (if mode is invalid)
        """

        if isinstance(datastream, socket):
            self._stream = SocketWrapper(datastream, encoding=encoding, bufsize=bufsize)
        else:
            self._stream = datastream
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._validate = validate
        self._labelmsm = labelmsm
        self._parsed = parsed
        self._logger = getLogger(__name__)

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

        raw_data, parsed_data = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return raw_data, parsed_data

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

        while parsing:  # loop until end of valid message or EOF
            try:
                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                if byte1 != b"\xd3":
                    # not RTCM3, discard and continue
                    continue
                byte2 = self._read_bytes(1)
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                if byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    raw_data, parsed_data = self._parse_rtcm3(byte1 + byte2)
                    parsing = False
                else:
                    # not RTCM3, discard and continue
                    continue

            except EOFError:
                return None, None
            except (
                RTCMMessageError,
                RTCMParseError,
                RTCMStreamError,
                RTCMTypeError,
            ) as err:
                if self._quitonerror:
                    self._do_error(err)
                continue

        return raw_data, parsed_data

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
        if self._parsed:
            parsed_data = self.parse(
                raw_data,
                validate=self._validate,
                labelmsm=self._labelmsm,
            )
        else:
            parsed_data = None
        return raw_data, parsed_data

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) == 0:  # EOF
            raise EOFError()
        if 0 < len(data) < size:  # truncated stream
            raise RTCMStreamError(
                "Serial stream terminated unexpectedly. "
                f"{size} bytes requested, {len(data)} bytes returned."
            )
        return data

    def _do_error(self, err: Exception):
        """
        Handle error.

        :param Exception err: error message
        :raises: Exception if quitonerror = 2
        """

        if self._quitonerror == ERR_RAISE:
            raise err from err
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            if self._errorhandler is None:
                self._logger.error(err)
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
        validate: int = VALCKSUM,
        labelmsm: int = 1,
    ) -> RTCMMessage:
        """
        Parse RTCM message to RTCMMessage object.

        :param bytes message: RTCM raw message bytes
        :param int validate: 0 = don't validate CRC, 1 = validate CRC (1)
        :param int labelmsm: MSM NSAT and NCELL attribute label (1 = RINEX, 2 = freq)
        :return: RTCMMessage object
        :rtype: RTCMMessage
        :raises: RTCMParseError (if data stream contains invalid data or unknown message type)
        """

        if validate & VALCKSUM:
            if calc_crc24q(message):
                raise RTCMParseError(
                    f"RTCM3 message invalid - failed CRC: {message[-3:]}"
                )
        payload = message[3:-3]
        return RTCMMessage(payload=payload, labelmsm=labelmsm)
