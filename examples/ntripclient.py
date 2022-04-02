#!/usr/bin/python -u
"""
A very simple example of an NTRIP client which uses pyrtcm to parse the RTCM3 output
from a designated NTRIP server & mountpoint to the terminal.

Usage:

python3 ntripclient.py server=127.0.0.1 port=2101 mountpoint=RTMC32 user=myuser password=mypassword

For help, type:

python3 ntripclient.py -h

NB: NOT FOR PRODUCTION USE! Please respect the terms and conditions
of any public or private NTRIP service you use with this example.

Created on 27 Mar 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

from platform import system
import socket
import sys
from base64 import b64encode
from pyrtcm import (
    RTCMReader,
    RTCMParseError,
    RTCMMessageError,
    RTCMTypeError,
    ParameterError,
    RTCM_MSGIDS,
)


class ConnError(Exception):
    """Connection Error Class."""


USERAGENT = "pyrtcm NTRIP client/0.1"
HDRBUFFER = 4096
DATBUFFER = 1024
TIMEOUT = 10

# console escape sequences don't work on standard Windows terminal
if system() == "Windows":
    GREEN = ""
    YELLOW = ""
    BOLD = ""
    NORMAL = ""
else:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BOLD = "\033[1m"
    NORMAL = "\033[0m"

NTRIPCLIENT_HELP = (
    f"\n\n{GREEN}{BOLD} PYRTCM NTRIP CLIENT\n"
    + f"====================={NORMAL}\n\n"
    + "pyrtcm ntripclient is a command line utility to stream the "
    + "parsed RTCM3 output of an NTRIP server (caster) to the terminal.\n\n"
    + f"{GREEN}Usage:{NORMAL}\n\n"
    + "  ntripclient server=127.0.0.1 port=2101 mountpoint=RTMC32"
    + " user=myuser@domain.com password=mypassword\n"
    + "  Help: ntripclient -h\n\n"
    + f"{GREEN}Optional keyword arguments (default):{NORMAL}\n\n"
    + "  server - NTRIP caster URL or IP address (None)\n"
    + "  port - NTRIP caster port (2101)\n"
    + "  mountpoint - NTRIP mountpoint (None)\n"
    + "  V2 - use NTRIP version 2 (True)\n"
    + "  user - user name (anon)\n"
    + "  password - user password (password)\n"
    + "  idonly - show RTCM3 message identity & description only (False)\n"
    + "  listmp - list all available mountpoints (False)\n"
    + "  verbose - verbose log messages (True)\n\n"
    + f"{GREEN}Type Ctrl-C to terminate.{NORMAL}\n\n"
    + f"{YELLOW}© 2022 SEMU Consulting BSD 3-Clause license\n"
    + f"https://github.com/semuconsulting/pyrtcm/tree/main/examples{NORMAL}\n\n"
)


class NTRIPClient:
    """
    NTRIP Client Class.
    """

    def __init__(self, **kwargs):
        """
        Constructor.
        """

        user = kwargs.get("user", "anon")
        password = kwargs.get("password", "password")
        self._caster = kwargs.get("server", None)  # 3.23.52.207 = rtk2go.com
        self._port = int(kwargs.get("port", 2101))
        self._mountpoint = kwargs.get("mountpoint", None)
        self._V2 = int(kwargs.get("V2", True))
        self._idonly = int(kwargs.get("idonly", False))
        self._listmp = int(kwargs.get("listmp", False))
        self._verbose = int(kwargs.get("verbose", True))

        if self._caster is None or (self._mountpoint is None and not self._listmp):
            raise ParameterError(
                f"Invalid parameter(s). Server and Mountpoint must be provided.\n{NTRIPCLIENT_HELP}"
            )

        user = user + ":" + password
        self._user = b64encode(user.encode(encoding="utf-8"))
        if self._listmp:
            self._mountpoint = "XXXXXXXXXXXX"
        self._socket = None

    def _formatGET(self):
        """
        Format HTTP GET Request.
        """

        if self._mountpoint[0:1] != "/":
            self._mountpoint = "/" + self._mountpoint
        req = (
            f"GET {self._mountpoint} HTTP/1.1\r\n"
            + f"User-Agent: {USERAGENT}\r\n"
            + f"Authorization: Basic {self._user.decode(encoding='utf-8')}\r\n"
        )
        if self._V2:
            req += "Ntrip-Version: Ntrip/2.0\r\n"
        req += "\r\n"
        self.doOutput(req)
        return req.encode(encoding="utf-8")

    def doOutput(self, msg):
        """
        Output debug message according to verbosity setting.
        """

        if self._verbose:
            print(msg)

    def _doHeader(self, sock):
        """
        Parse response header lines.
        """

        conn = f"{self._caster}:{self._port}{self._mountpoint}"
        data = "Initial Header"
        self.doOutput("*** Start Of Header ***")
        while data:
            try:

                data = sock.recv(HDRBUFFER)
                header_lines = data.decode(encoding="utf-8").split("\r\n")

                for line in header_lines:
                    if line.find("SOURCETABLE") >= 0:  # end of mountpoint list
                        self.doOutput(line)
                        sys.exit()
                    elif (
                        line.find("401 Unauthorized") >= 0
                        or line.find("403 Forbidden") >= 0
                        or line.find("404 Not Found") >= 0
                    ):
                        raise ConnError(f"{line}: {conn}")
                    elif line == "":
                        break
                    self.doOutput(line)

            except UnicodeDecodeError:
                data = False

        self.doOutput("*** End Of Header ***\n")

    def _doData(self, sock):
        """
        Parse RTCM3 data.
        """

        buf = bytearray()
        data = "Initial data"
        while data:
            try:

                data = sock.recv(DATBUFFER)
                self.doOutput(f"Data bytes received: {len(data)}")
                buf += data

                # Parse the data into individual RTCM3 messages
                while True:
                    raw_data, buf = RTCMReader.parse_buffer(buf)

                    if raw_data is not None:
                        parsed_data = RTCMReader.parse(raw_data)
                        if self._idonly:
                            mid = parsed_data.identity
                            print(f"{mid} ({RTCM_MSGIDS[mid]})")
                        else:
                            print(f"{parsed_data}\n")
                        # if you wanted to forward this RTCM3 message to
                        # a GNSS device via its serial port at this point,
                        # you could use something like this:
                        #
                        # with Serial(port, baudrate, timeout=timeout) as serial:
                        #    serial.write(parsed_data.serialize())
                        #
                    else:
                        break

            except (RTCMParseError, RTCMMessageError, RTCMTypeError) as err:
                self.doOutput(f"RTCM Parse Error {err}\n")
                data = False

    def run(self):
        """
        Open socket and read data from NTRIP caster.
        """

        try:

            with socket.socket() as sock:
                sock.connect((self._caster, self._port))
                self.doOutput(f"Connected to: {self._caster}:{self._port}")
                sock.settimeout(TIMEOUT)
                sock.sendall(self._formatGET())
                while True:
                    self._doHeader(sock)
                    self._doData(sock)

        except socket.timeout as err:
            self.doOutput(f"Connection Timed Out {err}")
        except socket.error as err:
            self.doOutput(f"Connection Error {err}")
        except KeyboardInterrupt:
            self.doOutput("Connection Terminated by User")
            sys.exit()


def main():
    """
    CLI Entry point.
    :param: as per NTRIPClient constructor.
    :raises: ParameterError if parameters are invalid
    """
    # pylint: disable=raise-missing-from

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(NTRIPCLIENT_HELP)
            sys.exit()

    try:
        ntrip = NTRIPClient(**dict(arg.split("=") for arg in sys.argv[1:]))
        ntrip.run()
    except ValueError:
        raise ParameterError(f"Invalid parameter(s).\n{NTRIPCLIENT_HELP}")


if __name__ == "__main__":

    main()
