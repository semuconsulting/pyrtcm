"""
Main RTCM Message Protocol Class.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import logging
import struct
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt
import pyrtcm.rtcmtypes_get as rtg
from pyrtcm.rtcmhelpers import (
    calc_crc24q,
    crc_2_bytes,
    len_2_bytes,
    get_bitarray,
    bits_2_val,
    datasiz,
    itow2utc,
)

LOGGING = logging.WARNING


class RTCMMessage:
    """RTCM Message Class."""

    def __init__(self, payload: bytes, **kwargs):
        """Constructor.

        :param bytes payload : message payload
        :param kwargs: optional payload key/value pairs
        :raises: RTCMMessageError

        """

        logging.basicConfig(
            format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
            level=LOGGING,
        )

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)

        self._payload = payload

        self._do_attributes(**kwargs)

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate RTCMMessage attributes from payload.

        :param kwargs: optional payload key/value pairs
        :raises: RTCMTypeError

        """

        offset = 0  # payload offset in bits
        index = []  # array of (nested) group indices
        self._payload_bits = get_bitarray(self._payload)  # payload as bit array
        logging.debug(
            "Payload bits: %s, length: %s", self._payload_bits, len(self._payload)
        )

        try:

            pdict = (
                self._get_dict()
            )  # get payload definition dict for this message identity
            if pdict is None:  # unknown (or not yet implemented) message identity
                logging.debug("Unknown message identity: %s", self.identity)
                return
            for key in pdict:  # process each attribute in dict
                logging.debug("Key: %s", key)
                if key == rtt.NYI:
                    setattr(self, "status", pdict[key])
                    continue
                (offset, index) = self._set_attribute(
                    offset, pdict, key, index, **kwargs
                )

        except (
            AttributeError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise rte.RTCMTypeError(
                (
                    f"Incorrect type for attribute '{key}' "
                    f"in message type {self.identity}"
                )
            ) from err
        except (OverflowError,) as err:
            raise rte.RTCMTypeError(
                (
                    f"Overflow error for attribute '{key}' "
                    f"in message type {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, offset: int, pdict: dict, key: str, index: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param int offset: payload offset in bytes
        :param dict pdict: dict representing payload definition
        :param str key: attribute keyword
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        # att = pdict[key]  # get attribute type
        att = key
        if isinstance(att, tuple):  # repeating group of attributes
            (offset, index) = self._set_attribute_group(att, offset, index, **kwargs)
        else:  # single attribute
            offset = self._set_attribute_single(att, offset, key, index, **kwargs)

        return (offset, index)

    def _set_attribute_group(
        self, att: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple att: attribute group - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        index.append(0)  # add a (nested) group index
        numr, attd = att  # number of repeats, attribute dictionary

        # derive or retrieve number of items in group
        if isinstance(numr, int):  # fixed number of repeats
            rng = numr
        else:  # number of repeats is defined in named attribute
            rng = getattr(self, numr)
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(rng):
            index[-1] = i + 1
            for key1 in attd:
                (offset, index) = self._set_attribute(
                    offset, attd, key1, index, **kwargs
                )

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_single(
        self, att: object, offset: int, key: str, index: list, **kwargs
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str att: attribute type string e.g. 'INT008'
        :param int offset: payload offset in bits
        :param str key: attribute keyword
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: offset
        :rtype: int

        """
        # pylint: disable=no-member

        # if attribute is part of a (nested) repeating group, suffix name with index
        keyr = key
        for i in index:  # one index for each nested level
            if i > 0:
                keyr += f"_{i:02d}"

        # get value of required number of bits at current payload offset
        atts = datasiz(key)
        bitfield = self._payload_bits[offset : offset + atts]
        logging.debug("Bitfield: %s, size: %s", bitfield, atts)
        val = bits_2_val(bitfield)

        setattr(self, keyr, val)
        offset += atts

        return offset

    def _get_dict(self) -> dict:
        """
        Get payload dictionary corresponding to message identity
        (or None if message type not defined)

        :return: dictionary representing payload definition
        :rtype: dict or None
        """

        return rtg.RTCM_PAYLOADS_GET.get(self.identity, None)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str
        """

        if self.payload is None:
            return f"<RTCM({self.identity})>"

        stg = f"<RTCM({self.identity}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                if att == "iTOW":  # attribute is a GPS Time of Week
                    val = itow2utc(val)  # show time in UTC format
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str
        """

        return f"RTCMMessage({self._payload})"

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name: attribute name
        :param object value: attribute value
        :raises: rtcmMessageError
        """

        if self._immutable:
            raise rte.RTCMMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return: serialized output
        :rtype: bytes
        """

        size = len_2_bytes(self._payload)
        message = rtt.RTCM_HDR + size + self._payload
        crc = crc_2_bytes(message)
        return message + crc

    @property
    def identity(self) -> str:
        """
        Getter for identity.

        :return: message identity e.g. "1005"
        :rtype: str
        """

        return str(self._payload[0] << 4 | self._payload[1] >> 4)

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return: raw payload as bytes
        :rtype: bytes

        """

        return self._payload
