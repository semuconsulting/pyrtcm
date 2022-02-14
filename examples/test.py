import struct
from pyrtcm import RTCMMessage


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


payload = b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH "
msg = RTCMMessage(payload)
print(f"Message: {msg}")
raw = b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
print(f"Serialised: {msg.serialize()}\nShould be:  {raw}")
print(f"Messages match? {msg.serialize() == raw}")


# first two bytes should be 00111110 11010000

ba = [get_bit(payload, i) for i in range(len(payload) * 8)]

print(f"{ba}, len = {len(ba)} bytes = {len(ba)/8}, pay len = {len(payload)} ")

offset = 0
atts = 12
bits = ba[offset : offset + atts]

print(f"first three bytes = {payload[0]:08b}, {payload[1]:08b}, {payload[2]:08b}")
print(f"identity = {str(payload[0] << 4 | payload[1] >> 4)}")
print(f"bits = {bits}, value = {bits_2_val(bits)}")
offset = 12

atts = 12
bits = ba[offset : offset + atts]

print(f"identity = {str(payload[0] << 4 | payload[1] >> 4)}")
print(f"bits = {bits}, value = {bits_2_val(bits)}")
offset += atts
