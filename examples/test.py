from pyrtcm import RTCMMessage, RTCMReader


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


raw = b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
payload = raw[3:-3]
msg1 = RTCMReader.parse(raw)
msg2 = RTCMMessage(payload)
print(f"Message from RTCMReader.parse():\n{msg1}")
print(f"Message from RTCMMessage():\n{msg2}")

print(f"Serialised: {msg2.serialize()}\nShould be:  {raw}")
print(f"Messages match? {msg2.serialize() == raw}")


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

bitfield = [1, 0, 1, 0, 1]
sign = -1 if bitfield[0] else 1
print(bitfield[0], sign, bitfield[1:])
val = 0
for bit in bitfield[1:]:
    val = (val << 1) | bit

print(val * sign)
