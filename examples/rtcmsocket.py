"""
rtcmsocket.py

A simple example implementation of a GNSS socket reader
using the pyrtcm.RTCMReader iterator functions.

Created on 05 May 2022
@author: semuadmin
"""

import socket
from datetime import datetime
from pyrtcm.rtcmreader import RTCMReader


def read(stream: socket.socket):
    """
    Reads and parses RTCM3 message data from socket stream.
    """

    msgcount = 0
    start = datetime.now()

    rtr = RTCMReader(
        stream,
    )
    try:
        for (_, parsed_data) in rtr.iterate():
            print(parsed_data)
            msgcount += 1
    except KeyboardInterrupt:
        dur = datetime.now() - start
        secs = dur.seconds + dur.microseconds / 1e6
        print("Session terminated by user")
        print(
            f"{msgcount:,d} messages read in {secs:.2f} seconds:",
            f"{msgcount/secs:.2f} msgs per second",
        )


if __name__ == "__main__":

    SERVER = "192.168.0.72"
    PORT = 50007

    print(f"Opening socket {SERVER}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        read(sock)
