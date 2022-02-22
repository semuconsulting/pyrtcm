"""
Example illustrating how to generate RTCM3 payloads from
constituent datafields.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyrtcm import RTCMMessage, datasiz


def df2payload(datafields: list) -> bytes:
    """
    Convert list of (datafield, value) tuples to RTCM3 payload.

    :param list datafields: list of (datafield, value) tuples
    :return: payload as bytes
    :rtype: bytes
    """

    # convert (datafield, value) tuples to bit stream
    bits = ""
    for (dfd, val) in datafields:
        bits += f"{val:0{datasiz(dfd)}b}"
    print(f"\nbitstream = {bits}")

    # convert bit stream to octets
    octets = [f"0b{bits[i : i + 8]:0<8}" for i in range(0, len(bits), 8)]
    print(f"\noctets = {octets}")

    # convert octets to bytes
    pay = b""
    for octet in octets:
        pay += int(octet, 2).to_bytes(1, "little")
    return pay


# define constituent data fields in the order in
# which they appear in the payload definition.
# the example here is a 1065 message type
data = [
    ("DF002", 1065),
    ("DF386", 12345),
    ("DF391", 3),
    ("DF388", 0),
    ("DF413", 1),
    ("DF414", 2),
    ("DF415", 3),
    ("DF387", 2),  # 2 satellites
    # # sat 1
    ("DF384", 23),
    ("DF379", 2),  # 2 biases for sat 1
    # # sat1, bias 1
    ("DF381", 4),
    ("DF383", 7),
    # # sat1, bias 2
    ("DF381", 2),
    ("DF383", 9),
    # # sat 2
    ("DF384", 26),
    ("DF379", 1),  # 1 bias for sat 2
    # # sat2, bias 1
    ("DF381", 3),
    ("DF383", 5),
]

# convert list of datafields to payload
payload = df2payload(data)
print(f"\npayload = {payload}")

# create RTCM message from payload
msg = RTCMMessage(payload=payload)
print(f"\nmessage = {msg}")
