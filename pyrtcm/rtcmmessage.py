"""
Main RTCM Message Protocol Class.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import logging
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt
import pyrtcm.rtcmtypes_get as rtg
from pyrtcm.rtcmhelpers import (
    crc2bytes,
    len2bytes,
    get_bitarray,
    bits2val,
    attsiz,
    num_setbits,
    sat2prn,
    cell2prn,
    att2idx,
    att2name,
)

LOGGING = logging.WARNING
NSAT = "NSat"
NSIG = "NSig"
NCELL = "_NCell"
NBIAS = "_NBias"


class RTCMMessage:
    """RTCM Message Class."""

    def __init__(self, **kwargs):
        """Constructor.

        :param bytes payload: (kwarg) message payload (mandatory)
        :param bool scaling: (kwarg) whether to apply attribute scaling True/False (True)
        :param bool labelmsm: (kwarg) whether to label MSM NSAT and NCELL attributes (True)
        :raises: RTCMMessageError
        """
        # pylint: disable=unused-argument

        logging.basicConfig(
            format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
            level=LOGGING,
        )

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)

        self._payload = kwargs.get("payload", None)
        if self._payload is None:
            raise rte.RTCMMessageError("Payload must be specified")
        self._scaling = int(kwargs.get("scaling", True))
        self._labelmsm = int(kwargs.get("labelmsm", True))
        self._unknown = False
        self._do_attributes()

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self):
        """
        Populate RTCMMessage attributes from payload.

        :raises: RTCMTypeError
        """

        offset = 0  # payload offset in bits
        index = []  # array of (nested) group indices
        self._payload_bits = get_bitarray(self._payload)  # payload as bit array
        logging.debug(
            "Payload identity %s, bits: %s, length: %s",
            self.identity,
            self._payload_bits,
            len(self._payload),
        )

        try:

            pdict = (
                self._get_dict()
            )  # get payload definition dict for this message identity
            if pdict is None:  # unknown (or not yet implemented) message identity
                self._do_unknown()
                return
            for key in pdict:  # process each attribute in dict
                logging.debug("Key: %s", key)
                (offset, index) = self._set_attribute(offset, pdict, key, index)

        except Exception as err:
            raise rte.RTCMTypeError(
                (
                    f"Error processing attribute '{key}' "
                    f"in message type {self.identity}"
                )
            ) from err

    def _set_attribute(self, offset: int, pdict: dict, key: str, index: list) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param int offset: payload offset in bits
        :param dict pdict: dict representing payload definition
        :param str key: attribute keyword
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple

        """

        att = pdict[key]  # get attribute type
        if isinstance(att, tuple):  # repeating group of attributes
            (offset, index) = self._set_attribute_group(att, offset, index)
        else:  # single attribute
            offset = self._set_attribute_single(att, offset, key, index)

        return (offset, index)

    def _set_attribute_group(self, att: tuple, offset: int, index: list) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple att: attribute group - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple

        """

        numr, attd = att  # number of repeats, attribute dictionary
        # derive or retrieve number of items in group
        if isinstance(numr, int):  # fixed number of repeats
            rng = numr
        else:  # number of repeats is defined in named attribute
            # if attribute is within a group
            # append group index to name e.g. "DF379_01"
            if numr == "DF379":
                numr += f"_{index[-1]:02d}"
            rng = getattr(self, numr)

        index.append(0)  # add a (nested) group index level
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(rng):
            index[-1] = i + 1
            for key1 in attd:
                (offset, index) = self._set_attribute(offset, attd, key1, index)

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_single(
        self,
        att: object,
        offset: int,
        key: str,
        index: list,
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str att: attribute type string e.g. 'INT008'
        :param int offset: payload offset in bits
        :param str key: attribute keyword
        :param list index: repeating group index array
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
        att, scale, _ = rtt.RTCM_DATA_FIELDS[key]
        if not self._scaling:
            scale = 0
        if key == "DF396":  # this MSM attribute has variable length
            atts = getattr(self, NCELL)
        else:
            atts = attsiz(att)
        bitfield = self._payload_bits[offset : offset + atts]
        logging.debug("Bitfield: %s, size: %s", bitfield, atts)
        val = bits2val(att, scale, bitfield)

        setattr(self, keyr, val)
        offset += atts

        # add special attributes to keep track of
        # MSM / 1230 message group sizes
        # NB: This is predicated on MSM payload dictionaries
        # always having attributes DF394, DF395 and DF396
        # in that order
        if key == "DF394":  # num of satellites in MSM message
            setattr(self, NSAT, num_setbits(bitfield))
        if key == "DF395":  # num of signals in MSM message
            setattr(self, NSIG, num_setbits(bitfield))
            setattr(self, NCELL, getattr(self, NSAT) * getattr(self, NSIG))
        if key == "DF422":  # num of bias entries in 1230 message
            setattr(self, NBIAS, num_setbits(bitfield))

        return offset

    def _get_dict(self) -> dict:
        """
        Get payload dictionary corresponding to message identity
        (or None if message type not defined)

        :return: dictionary representing payload definition
        :rtype: dict or None
        """

        return rtg.RTCM_PAYLOADS_GET.get(self.identity, None)

    def _do_unknown(self):
        """
        Handle unknown message type.
        """

        setattr(self, "DF002", self.identity)
        self._unknown = True
        logging.debug("Unknown message identity: %s", self.identity)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str
        """

        # if MSM message and labelmsm flag is set,
        # label NSAT and NCELL group attributes with
        # corresponding satellite PRN and signal ID
        if self._labelmsm and "MSM" in rtt.RTCM_MSGIDS[self.identity]:
            sats = sat2prn(self)
            cells = cell2prn(self)
            is_msm = True
        else:
            is_msm = False

        stg = f"<RTCM({self.identity}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]

                # label MSM NSAT and NCELL group attributes
                lbl = ""
                if is_msm:
                    aname = att2name(att)
                    if aname in rtt.ATT_NSAT:
                        prn = sats[att2idx(att)]
                        lbl = f"({prn})"
                    if aname in rtt.ATT_NCELL:
                        prn, sig = cells[att2idx(att)]
                        sig = "n/a" if sig is None else sig
                        lbl = f"({prn},{sig})"

                stg += att + lbl + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        if self._unknown:
            stg += ", Not_Yet_Implemented"
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str
        """

        return f"RTCMMessage(payload={self._payload})"

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

        size = len2bytes(self._payload)
        message = rtt.RTCM_HDR + size + self._payload
        crc = crc2bytes(message)
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
