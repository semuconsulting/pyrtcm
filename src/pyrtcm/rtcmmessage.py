"""
Main RTCM Message Protocol Class.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_get as rtg
from pyrtcm.rtcmhelpers import (
    att2idx,
    att2name,
    attsiz,
    bits2val,
    cell2prn,
    crc2bytes,
    escapeall,
    len2bytes,
    num_setbits,
    sat2prn,
)
from pyrtcm.rtcmtypes_core import (
    ATT_NCELL,
    ATT_NSAT,
    BOOL_GROUPS,
    NCELL,
    NSAT,
    NSIG,
    RTCM_DATA_FIELDS,
    RTCM_HDR,
    RTCM_MSGIDS,
)


class RTCMMessage:
    """RTCM Message Class."""

    def __init__(self, payload: bytes = None, scaling: bool = True, labelmsm: int = 1):
        """Constructor.

        :param bytes payload: message payload (mandatory)
        :param bool scaling: whether to apply attribute scaling True/False (True)
        :param int labelmsm: whether to label MSM NSAT and NCELL attributes (0 = none, 1 = RINEX, 2 = freq)
        :raises: RTCMMessageError
        """
        # pylint: disable=unused-argument

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)

        self._payload = payload
        if self._payload is None:
            raise rte.RTCMMessageError("Payload must be specified")
        self._payblen = len(self._payload) * 8  # length of payload in bits
        self._scaling = scaling
        self._labelmsm = labelmsm
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

        try:
            # get payload definition dict for this message identity
            pdict = self._get_dict()
            if pdict is None:  # unknown (or not yet implemented) message identity
                self._do_unknown()
                return
            for key in pdict:  # process each attribute in dict
                (offset, index) = self._set_attribute(offset, pdict, key, index)

        except Exception as err:
            raise rte.RTCMTypeError(
                (
                    f"Error processing attribute '{key}' "
                    f"in message type {self.identity} {err}"
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
        # one index for each nested level (unless it's a 'boolean' group)
        keyr = key
        for i in index:
            if i > 0 and keyr not in BOOL_GROUPS:
                keyr += f"_{i:02d}"

        # get value of required number of bits at current payload offset
        att, scale, _ = RTCM_DATA_FIELDS[key]
        if not self._scaling:
            scale = 0
        if key == "DF396":  # this MSM attribute has variable length
            atts = getattr(self, NSAT) * getattr(self, NSIG)
        else:
            atts = attsiz(att)
        bitfield = self._getbits(offset, atts)
        val = bits2val(att, scale, bitfield)

        setattr(self, keyr, val)
        offset += atts

        # add special attributes to keep track of
        # MSM message group sizes
        # NB: This is predicated on MSM payload dictionaries
        # always having attributes DF394, DF395 and DF396
        # in that order
        if key == "DF394":  # num of satellites in MSM message
            setattr(self, NSAT, num_setbits(bitfield))
        elif key == "DF395":  # num of signals in MSM message
            setattr(self, NSIG, num_setbits(bitfield))
        elif key == "DF396":  # num of cells in MSM message
            setattr(self, NCELL, num_setbits(bitfield))

        return offset

    def _getbits(self, position: int, length: int) -> int:
        """
        Get unsigned integer value of masked bits in bytes.

        :param int position: position in bitfield, from leftmost bit
        :param int length: length of masked bits
        :return: value
        :rtype: int
        """

        if position + length > self._payblen:
            raise rte.RTCMMessageError(
                f"Attribute size {length} exceeds remaining "
                + f"payload length {self._payblen - position}"
            )

        return int.from_bytes(self._payload, "big") >> (
            self._payblen - position - length
        ) & (2**length - 1)

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

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str
        """

        # if MSM message and labelmsm flag is set,
        # label NSAT and NCELL group attributes with
        # corresponding satellite PRN and signal ID
        is_msm = False
        if not self._unknown:
            if self._labelmsm and "MSM" in RTCM_MSGIDS[self.identity]:
                sats = sat2prn(self)
                sigcode = 0 if self._labelmsm == 2 else 1  # freq band or RINEX code
                cells = cell2prn(self, sigcode)
                is_msm = True

        stg = f"<RTCM({self.identity}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                # escape all byte chars
                if isinstance(val, bytes):
                    val = escapeall(val)
                # label MSM NSAT and NCELL group attributes
                lbl = ""
                if is_msm:
                    aname = att2name(att)
                    if aname in ATT_NSAT:
                        prn = sats[att2idx(att)]
                        lbl = f"({prn})"
                    if aname in ATT_NCELL:
                        prn, sig = cells[att2idx(att)]
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
        message = RTCM_HDR + size + self._payload
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
