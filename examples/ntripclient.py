#!/usr/bin/python -u
"""
A very simple example of an NTRIP client which uses pyrtcm to parse the RTCM3 output
from a designated NTRIP server & mountpoint to the terminal.

Based on https://github.com/liukai-tech/NtripClient-Tools but extensively refactored.
Original MIT license here https://github.com/liukai-tech/NtripClient-Tools/blob/master/LICENSE.

*** WORK IN PROGRESS ***

Usage:

python3 ntripclient.py server=127.0.0.1 port=2101 mountpoint=RTMC32 user=myuser@domain.com password=mypassword

NB: Please respect the terms and conditions of any public NTRIP service you use with this utility.

Created on 27 Mar 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

from platform import system
import socket
import sys
from datetime import datetime, timedelta
from base64 import b64encode
from typing import ByteString, Tuple
from pynmeagps import NMEAMessage, GET, ddd2dmm
from pyrtcm import RTCMReader, RTCMParseError, RTCMMessageError, ParameterError

USERAGENT = "pyrtcm NTRIP client/0.1"
GGAINTERVAL = timedelta(seconds=3)
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
    + "  lat - base latitude (53.0)\n"
    + "  lon - base longitute (-2.0)\n"
    + "  alt - base altitude (0.0)\n"
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
        self.caster = kwargs.get("server", "3.23.52.207")  # 3.23.52.207 = RTK2Go
        self.port = int(kwargs.get("port", 2101))
        self.mountpoint = kwargs.get("mountpoint", None)
        self.V2 = bool(kwargs.get("V2", True))
        self.lat = float(kwargs.get("lat", 53.0))
        self.lon = float(kwargs.get("lon", -2.0))
        self.alt = kwargs.get("alt", 0)
        self.verbose = bool(kwargs.get("verbose", True))
        self.lastGGATime = datetime(1990, 1, 1, 1, 0, 0)

        user = user + ":" + password
        self.user = b64encode(user.encode(encoding="utf-8"))

        self.socket = None

    def formatGET(self):
        """
        Format HTTP GET Request.
        """

        if self.mountpoint[0:1] != "/":
            self.mountpoint = "/" + self.mountpoint
        req = (
            f"GET {self.mountpoint} HTTP/1.1\r\n"
            + f"User-Agent: {USERAGENT}\r\n"
            + f"Authorization: Basic {self.user.decode(encoding='utf-8')}\r\n"
        )
        if self.V2:
            req += "Ntrip-Version: Ntrip/2.0\r\n"
        req += "\r\n"
        self.doOutput(req)
        return req.encode(encoding="utf-8")

    def formatGGA(self):
        """
        Format NMEA GGA sentence using pynmeagps.
        """

        return NMEAMessage(
            "GP",
            "GGA",
            GET,
            lat=float(ddd2dmm(self.lat, "LA")),
            NS="N" if self.lat > 0 else "S",
            lon=float(ddd2dmm(self.lon, "LN")),
            EW="E" if self.lon > 0 else "W",
            quality=1,
            numSV=15,
            HDOP=0.19,
            alt=float(self.alt),
            altUnit="M",
            sep=-8.992,
            sepUnit="M",
        )

    def doOutput(self, msg):
        """
        Output debug message according to verbosity setting.
        """

        if self.verbose:
            print(msg)

    def doHeader(self, sock):
        """
        Parse response header lines.
        """

        header = "Initial header"
        print("*** Start Of Header ***")
        while header:
            try:

                data = sock.recv(HDRBUFFER)
                header_lines = data.decode(encoding="utf-8").split("\r\n")

                for line in header_lines:
                    if line == "":
                        if header:
                            header = False
                            self.doOutput("*** End Of Header ***\n")
                    else:
                        self.doOutput(line)

                for line in header_lines:
                    if line.find("SOURCETABLE") >= 0:
                        self.doOutput("Mountpoint does not exist")
                        sys.exit(1)
                    elif line.find("401 Unauthorized") >= 0:
                        self.doOutput("Unauthorized request\n")
                        sys.exit(1)
                    elif line.find("404 Not Found") >= 0:
                        self.doOutput("Mountpoint does not exist\n")
                        sys.exit(2)
                    elif line.find("200 OK") >= 0:  # Request was valid
                        self.doGGA(sock)

            except UnicodeDecodeError as err:
                self.doOutput(f"Header decode error {err}")

    def doData(self, sock):
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

                self.doGGA(sock)

            except (RTCMParseError, RTCMMessageError) as err:
                self.doOutput(f"RTCM Parse Error {err}\n")
                data = False

    def doGGA(self, sock):
        """
        Send GGA sentence periodically.
        """

        if datetime.now() > self.lastGGATime + GGAINTERVAL:
            gga = self.formatGGA()
            sock.sendall(gga.serialize())
            self.lastGGATime = datetime.now()
            self.doOutput(gga)

    def run(self):
        """
        Open socket and read data from NTRIP caster.
        """

        try:

            with socket.socket() as sock:
                sock.connect((self.caster, self.port))
                self.doOutput(f"Connected to: {self.caster}:{self.port}")
                sock.settimeout(TIMEOUT)
                sock.sendall(self.formatGET())
                while True:
                    self.doHeader(sock)
                    self.doData(sock)

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
