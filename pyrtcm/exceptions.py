"""
RTCM Custom Exception Types

Created on 14 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""


class ParameterError(Exception):
    """Parameter Error Class."""


class RTCMParseError(Exception):
    """
    RTCM Parsing error.
    """


class RTCMStreamError(Exception):
    """
    RTCM Streaming error.
    """


class RTCMMessageError(Exception):
    """
    RTCM Undefined message class/id.
    Essentially a prompt to add missing payload types to rtcm_PAYLOADS.
    """


class RTCMTypeError(Exception):
    """
    RTCM Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to rtcm_PAYLOADS.
    """
