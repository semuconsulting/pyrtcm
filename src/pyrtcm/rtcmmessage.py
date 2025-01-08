"""
Main RTCM Message Protocol Class.

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyrtcm.exceptions import RTCMMessageError, RTCMTypeError
from pyrtcm.rtcmhelpers import crc2bytes, escapeall, len2bytes
from pyrtcm.rtcmtables import PRNSIGMAP
from pyrtcm.rtcmtypes_core import (
    CELPRN,
    CELSIG,
    CHA,
    INT,
    INTS,
    NA,
    NCELL,
    NHARMCOEFFC,
    NHARMCOEFFS,
    NSAT,
    NSIG,
    PRN,
    RTCM_DATA_FIELDS,
    RTCM_HDR,
    RTCM_MSGIDS,
    STR,
)
from pyrtcm.rtcmtypes_get import RTCM_PAYLOADS_GET
from pyrtcm.rtcmtypes_get_igs import RTCM_PAYLOADS_GET_IGS
from pyrtcm.rtcmtypes_get_msm import RTCM_PAYLOADS_GET_MSM

BOOL = "B"


class RTCMMessage:
    """RTCM Message Class."""

    def __init__(self, payload: bytes = None, labelmsm: int = 1):
        """Constructor.

        :param bytes payload: message payload (mandatory)
        :param int labelmsm: MSM NSAT and NCELL attribute label (1 = RINEX, 2 = freq)
        :raises: RTCMMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)

        self._payload = payload
        if self._payload is None:
            raise RTCMMessageError("Payload must be specified")
        self._payloadi = int.from_bytes(self._payload, "big")  # payload as int
        self._payblen = len(self._payload) * 8  # length of payload in bits
        self._labelmsm = labelmsm
        self._unknown = False
        self._satmap = None
        self._cellmap = None
        self._do_attributes()

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self):
        """
        Populate RTCMMessage attributes from payload.

        :raises: RTCMTypeError
        """

        offset = 0  # payload offset in bits
        index = []  # array of (nested) group indices
        anam = ""
        try:
            # get payload definition dict for this message identity
            pdict = self._get_dict()
            if pdict is None:  # unknown (or not yet implemented) message identity
                self._do_unknown()
                return
            for anam in pdict:  # process each attribute in dict
                offset, index = self._set_attribute(anam, pdict, offset, index)

        except Exception as err:  # pragma: no cover
            raise RTCMTypeError(
                (
                    f"Error processing attribute '{anam}' "
                    f"in message type {self.identity} {err}"
                )
            ) from err

    def _set_attribute(self, anam: str, pdict: dict, offset: int, index: list) -> tuple:
        """
        Recursive routine to set individual, conditional or grouped payload attributes.

        :param str anam: attribute name
        :param dict pdict: dict representing payload definition
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple

        """

        adef = pdict[anam]  # get attribute definition
        if isinstance(adef, tuple):  # attribute group
            gtyp, _ = adef
            if isinstance(gtyp, tuple):  # conditional group of attributes
                offset, index = self._set_attribute_optional(adef, offset, index)
            else:  # repeating group of attributes
                offset, index = self._set_attribute_group(adef, offset, index)
        else:  # single attribute
            offset = self._set_attribute_single(anam, offset, index)

        return offset, index

    def _set_attribute_optional(self, adef: tuple, offset: int, index: list) -> tuple:
        """
        Process conditional group of attributes - group is present if attribute value
        = specific value, otherwise absent.

        :param tuple adef: attribute definition - tuple of ((attribute name, condition), group dict)
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple
        """

        (anam, con), gdict = adef  # (attribute name, condition), group dictionary
        # "+n" suffix signifies that one or more nested group indices
        # must be appended to name e.g. "DF379_01", "IDF023_03"
        # if "+" in anam:
        #     anam, nestlevel = anam.split("+")
        #     for i in range(int(nestlevel)):
        #        anam += f"_{index[i]:02d}"

        if getattr(self, anam) == con:  # if condition is met...
            # recursively process each group attribute,
            # incrementing the payload offset as we go
            for anamg in gdict:
                offset, index = self._set_attribute(anamg, gdict, offset, index)

        return offset, index

    def _set_attribute_group(self, adef: tuple, offset: int, index: list) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple adef: attribute definition - tuple of (attr name, attribute dict)
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple

        """

        anam, gdict = adef  # attribute signifying group size, group dictionary
        # derive or retrieve number of items in group
        if isinstance(anam, int):  # fixed number of repeats
            gsiz = anam
        else:  # number of repeats is defined in named attribute
            # "+n" suffix signifies that one or more nested group indices
            # must be appended to name e.g. "DF379_01", "IDF023_03"
            if "+" in anam:
                anam, nestlevel = anam.split("+")
                for i in range(int(nestlevel)):
                    anam += f"_{index[i]:02d}"
            gsiz = getattr(self, anam)
            if anam == "IDF035":  # 4076_201 range is N-1
                gsiz += 1

        index.append(0)  # add a (nested) group index level
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(gsiz):
            index[-1] = i + 1
            for anamg in gdict:
                offset, index = self._set_attribute(anamg, gdict, offset, index)

        index.pop()  # remove this (nested) group index

        return offset, index

    def _set_attribute_single(
        self,
        anam: str,
        offset: int,
        index: list,
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str anam: attribute name
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: offset
        :rtype: int

        """

        # pylint: disable=invalid-name, line-too-long

        # if attribute is part of a (nested) repeating group, suffix name with index
        anami = anam
        for i in index:  # one index for each nested level
            if i > 0:
                anami += f"_{i:02d}"

        # get value of required number of bits at current payload offset
        atyp, asiz, ares, _ = RTCM_DATA_FIELDS[anam]
        if anam == "DF396":  # this MSM attribute has variable length
            asiz = getattr(self, NSAT) * getattr(self, NSIG)
        if atyp == PRN:
            val = self._satmap[index[0]]
        elif atyp == CELPRN:
            val = self._cellmap[index[0]][0]
        elif atyp == CELSIG:
            val = self._cellmap[index[0]][1]
        else:
            # done inline for performance reasons...
            bits = self._payloadi >> (self._payblen - offset - asiz) & ((1 << asiz) - 1)
            msb = 1 << asiz - 1 if atyp in (INTS, INT) else 0
            if atyp == INTS:  # int, MSB indicates sign
                val = bits & msb - 1
                if bits & msb:
                    val *= -1
            elif atyp == CHA:
                val = chr(bits)
            else:  # all other types
                val = bits
            if atyp == INT and bits & msb:  # 2's compliment -ve int
                val -= 1 << asiz
            if atyp == STR:
                val = "" if val == 0 else chr(bits)
            else:
                if ares not in (0, 1):  # apply any scaling factor
                    val *= ares

        if atyp == STR:  # concatenated string
            setattr(self, anam, getattr(self, anam, "") + val)
        else:
            setattr(self, anami, val)
        offset += asiz

        # add special attributes to keep track of
        # MSM message group sizes
        # NB: This is predicated on MSM payload dictionaries
        # always having attributes DF394, DF395 and DF396
        # in that order
        if anam in ("DF394", "DF395", "DF396"):
            nbits = bin(bits).count("1")  # number of bits set
            if anam == "DF394":  # num of satellites in MSM message
                setattr(self, NSAT, nbits)
            elif anam == "DF395":  # num of signals in MSM message
                setattr(self, NSIG, nbits)
            elif anam == "DF396":  # num of cells in MSM message
                setattr(self, NCELL, nbits)
                # populate NSAT and NCELL mapping dictionaries
                self._getsatcellmaps()

        # add special coefficient attributes for message 4076_201
        if anam == "IDF038":
            i = index[0]
            N = getattr(self, f"IDF037_{i:02d}") + 1
            M = getattr(self, f"IDF038_{i:02d}") + 1
            nc = int(((N + 1) * (N + 2) / 2) - ((N - M) * (N - M + 1) / 2))
            ns = int(nc - (N + 1))
            # ncs = (N + 1) * (N + 1) - (N - M) * (N - M + 1)
            setattr(self, NHARMCOEFFC, nc)
            setattr(self, NHARMCOEFFS, ns)

        return offset

    def _getsatcellmaps(self):
        """
        Map group indices to satellite PRN & signal ID values via
        bitmasks DF394, DF395 and DF396.
        """

        prnmap, sigmap = PRNSIGMAP[str(self.identity)[0:3]]
        sigcode = 0 if self._labelmsm == 2 else 1

        sats = {}
        nsat = 0
        for idx in range(1, 65):
            if getattr(self, "DF394") >> (64 - idx) & 1:
                nsat += 1
                sats[nsat] = prnmap.get(idx, NA)

        sigs = []
        nsig = 0
        for idx in range(1, 33):
            if getattr(self, "DF395") >> (32 - idx) & 1:
                sgc = sigmap.get(idx, NA)
                fqc = sgc[1] if sigcode else sgc[0]
                sigs.append(fqc)
                nsig += 1

        ncells = int(nsat * nsig)
        cells = {}
        ncell = idx = 0
        for sat in range(nsat):
            for sig in range(nsig):
                idx += 1
                if getattr(self, "DF396") >> (ncells - idx) & 1:
                    ncell += 1
                    cells[ncell] = (sats[sat + 1], sigs[sig])

        self._satmap = sats
        self._cellmap = cells

    def _get_dict(self) -> dict:
        """
        Get payload dictionary corresponding to message identity
        (or None if message type not defined)

        :return: dictionary representing payload definition
        :rtype: dict or None
        """

        if "1070" <= self.identity <= "1229":  # MSM types
            return RTCM_PAYLOADS_GET_MSM.get(self.identity, None)
        if self.identity[:4] == "4076":  # IGS types
            return RTCM_PAYLOADS_GET_IGS.get(self.identity, None)
        return RTCM_PAYLOADS_GET.get(self.identity, None)

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

        stg = f"<RTCM({self.identity}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                # escape all byte chars
                if isinstance(val, bytes):  # pragma: no cover
                    val = escapeall(val)
                stg += att + "=" + str(val)
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
            raise RTCMMessageError(
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

        mid = self._payload[0] << 4 | self._payload[1] >> 4

        if mid == 4076:  # proprietary IGS SSR message type
            subtype = (self._payload[1] & 0x1) << 7 | self._payload[2] >> 1
            mid = f"{mid}_{subtype:03d}"

        return str(mid)

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return: raw payload as bytes
        :rtype: bytes

        """

        return self._payload

    @property
    def ismsm(self) -> bool:
        """
        Check if message is Multiple Signal Message (MSM) type.

        :return: True/False
        :rtype: bool
        """

        try:
            return "MSM" in RTCM_MSGIDS[self.identity]
        except KeyError:
            return False
