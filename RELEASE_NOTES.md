# pyrtcm Release Notes

### RELEASE 1.1.3

1. Update RTCM message definitions - messages 1300-1305 added.
1. Adopt more advanced `SocketWrapper` class from pygnssutils to support socket datastream encoding (chunked, gzip, compress, deflate).
1. Add optional `encoding` argument to RTCMReader to support encoding values.

CHANGES:

### RELEASE 1.1.2

CHANGES:

1. Sphinx documentation and docstrings enhanced to include global constants and decodes.
1. `socket_stream.SocketStream` class renamed to `socket_wrapper.SocketWrapper` class for clarity.
1. Drop active support for Python 3.8 - now End of Life as at October 2024.

### RELEASE 1.1.1

ENHANCEMENTS:


1. Internal performance enhancements - UBXReader.parse() now 30% faster.
1. Internal enhancements to logging and exception handling.
1. Enhance test coverage


### RELEASE 1.1.0

ENHANCEMENTS:

1. `PRN`, `CELLPRN` and `CELLSIG` attributes added to satellite (NSAT) and cell (NCELL) groups within parsed RTCM3 MSM payloads via `SPARTNMessage._getsatcellmaps()` function, replacing previous `sat2prn()` and `cell2prn()` helper functionality. `labelmsm` keyword argument signifies either RINEX (1) or Frequency Band (2) signal format for CELLSIG attribute.

### RELEASE 1.0.20

ENHANCEMENTS

1. Add `parse_msm` helper method to parse RTCM3 MSM message type into series of iterable data arrays.
1. Add `parse_4076_201` helper method to parse RTCM3 4076_201 SSR message types into series of iterable data arrays.
1. Internal streamlining of conditional group parsing & updated docstrings - no functional changes.

### RELEASE 1.0.19

ENHANCEMENTS

1. Minor internal streamlining of nested group parsing - no functional changes.

### RELEASE 1.0.18

FIXES:

1. Fix IGM05/06 message parsing (e.g. 4076_025, 4076_066, etc.).

### RELEASE 1.0.17

ENHANCEMENTS:

1. Add proprietary IGS SSR 4076 messages, as defined in https://files.igs.org/pub/data/format/igs_ssr_v1.pdf. NB not fully tested as available NTRIP sources only cover a subset of the 4076 subtypes defined.

### RELEASE 1.0.16

CHANGES:

1. PRN SIG mapping streamlined - `id2prnsigmap()` helper method replaced by dictionary `PRNSIGMAP`.

### RELEASE 1.0.15

CHANGES:

1. MSM GNSSEpoch field now parsed into appropriate datafield(s) e.g. GLONASS GNSSEpoch = {"DF416": "GLONASS Day Of Week", "DF034": "GLONASS Epoch Time (tk)"}.
2. MSM Extended Satellite Information field parsed into appropriate datafield e.g. DF419 for GLONASS, ExtSatInfo for other GNSS.

### RELEASE 1.0.14

CHANGES:

1. Minor internal streamlining of RTCM 1230 message processing.

### RELEASE 1.0.13

ENHANCEMENTS:

1. Enhance MSM signal attribute labelling to support either frequency band (e.g. "L1") or signal RINEX code (e.g. "1C"). The `labelmsm` keyword argument is now an integer rather than a boolean, with values 0 = no label, 1 = label with signal RINEX code (the existing default behaviour), 2 = label with frequency band

### RELEASE 1.0.12

FIXES:

1. Amend rounding factor to improve accuracy - Fixes #40. Thanks to @alainmuls for issue report.

### RELEASE 1.0.11

CHANGES:

1. Update constructor arguments and docstrings to clarify API (no functional changes) - thanks to @zakkie for contribution.

### RELEASE 1.0.10

CHANGES:

1. Deprecated `RTCMReader.iterate()` method removed - use the standard iterator instead e.g. `rtr = RTCMReader(**wkargs): for (raw,parse) in ubr: ...`, passing any `quitonerror` or `errorhandler` kwargs to the RTCMReader constructor.

FIXES:

1. Fix incorrect DF454 datafield length - thanks to @k-stf for contribution. Fixes #37

### RELEASE 1.0.9

CHANGES:

1. Remove Python 3.7 from workflows.

### RELEASE 1.0.8

FIXES:

1. Fixes KeyError when processing unknown proprietary message types #33 - thanks to @wtc-rsat for issue report.

### RELEASE 1.0.7

FIXES:

1. Fix to MSM signal label mapping #27 - thanks to @jcmb for issue report.
1. Fix DF090 scaling factor #30 - thanks to @augustomazzoni  for issue report.

### RELEASE 1.0.6

FIXES:

1. Fix to MSM message payload #21 - thanks to @jcmb for issue report.

ENHANCEMENTS:

1. Internal bitfield parsing streamlined - almost twice as fast as previously.
2. Exception handling enhanced.

### RELEASE 1.0.5

FIXES:

1. Fix to 1230 message payload - will now correctly label DF423, DF424, DF425 & DF426 data fields.

CHANGES:

1. `__str__` method enhanced to escape all byte values for clarity e.g. will now return b'\x61\x62\x63' rather than b'abc'
2. `RTCMReader.iterate()` method deprecated - use the standard iterator instead e.g. `rtr = RTCMReader(**wkargs): for (raw,parse) in ubr: ...`, passing any `quitonerror` or `errorhandler` kwargs to the RTCMReader constructor.

### RELEASE 1.0.4

FIXES:

1. Fix payload definition for 1033 message type.


### RELEASE 1.0.3

FIXES:

1. Fix payload definition for DF430 in message type 1044. Thanks to @Ralphccs for contribution.
2. Fix typo in IRNSS_PRN_MAP table definition.

CHANGES:

1. internal changes to GitHub actions workflow for Node.js 16 compatibility.

### RELEASE 1.0.2

ENHANCEMENTS:

1. Add support for INRSS MSM message types 1131-1137.

### RELEASE 1.0.1

FIXES:

1. Message payload for 1023 and 1024 corrected to include correct x16 grouping for residuals - thanks to @jiargei for contribution.

### RELEASE 1.0.0

CHANGES:

1. Marked to v1.0.0.
2. shields.io build status badge URL updated. 

No functional changes

### RELEASE 0.3.1

CHANGES:

1. Logging removed - Fixes #12.

### RELEASE 0.3.0

CHANGES:

1. Setup status changed to Production/Stable.
2. `pyserial` dependency removed.

### RELEASE 0.2.9-beta

FIXES:

1. `cell2prn` routine in `rtcmhelpers.py` corrected for 1117 and 1127 MSM message types.

### RELEASE 0.2.8-beta

ENHANCEMENTS:

1. New optional keyword argument `labelmsm` added to `read()` and `parse()` methods. Defaults to `True`. When True, attributes within MSM NSAT and NCELL repeating groups are labelled with their corresponding satellite PRN and signal ID when the `__str__()` (`print()`) method is invoked - e.g. `DF405_10(014,2C)` signifies that the the 10th `DF405` attribute in the group refers to satellite PRN 014 and signal ID 2C (*in RINEX notation*). 
2. **NB** this only affects the string (print) representation of the RTCMMessage - the underlying payload and attribute names are unchanged.

### RELEASE 0.2.7-beta

FIXES:

1. MSM group name definitions updated (was preventing some MSM attributes from rendering). All MSM message types (1077, 1127, etc.) should now render properly.

ENHANCEMENTS:

1. Add helper method `cell2prn` and associated lookup tables to map MSM cells (DF405_01, DF405_02, etc.) to their corresponding satellite PRNs and signal IDs.

### RELEASE 0.2.6-beta

ENHANCEMENTS:

1. Add capability to read from TCP/UDP socket as well as serial stream. Utilises a SocketStream utility class to allow sockets to be read using standard stream-like read(bytes) and readline() methods.

### RELEASE 0.2.5-beta

CHANGES:

1. Remove support for Python 3.6, now end of life (should still work find on 3.6 but no longer actively tested on this version).

FIXES:

1. Add CRC validation to RTCMReader.parse() method.

### RELEASE 0.2.4-beta

FIXES:

1. Fixed occasional parse error in some 1127 (MSM7) messages (some NTRIP casters appear to send truncated 1127 messages in certain circumstances).

### RELEASE 0.2.3-beta

ENHANCEMENTS:

1. Additional Ephemerides message types added - 1041, 1042, 1044, 1045, 1046. `pyrtcm` should now support the full range of non-proprietary message types documented in RTCM 10403.3 (aka v3.3) with Amendment 2 - 2021-SC104-1217.
3. Minor enhancements to data field and message type descriptions.
2. `ntripclient.py` example enhanced and simplified.

### RELEASE 0.2.2-beta

FIXES:

1. Fixed error in RTCMReader.parse_buffer() which caused IndexError in certain circumstances. Apologies, previous fix was inadequate.

### RELEASE 0.2.1-beta

FIXES:

1. Fixed error in RTCMReader.parse_buffer() which caused IndexError in certain circumstances.

### RELEASE 0.2.0-beta

CHANGES:

1. Added `parse_buffer()` static method to `RTCMReader` to parse an individual RTCM3 message from a buffer
containing whole or partial RTCM3 messages, and return any remaining buffer. Can be used to parse the output from an NTRIP server HTTP GET response, for example. Thanks to @jakepoz and @foxittt for suggestion & inspiration.
2. Add simple NTRIP client example `ntripclient.py` which uses the new method above.
3. Development status updated to beta

### RELEASE 0.1.8-alpha

CHANGES:

1. Scaling now applied by default (`scaling=True`)

### RELEASE 0.1.7-alpha

CHANGES:

1. RTCMMessage constructor uses keyword argument for payload for consistency with other SEMU GNSS libraries, i.e.:
```python
msg = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
```
rather than:
```python
msg = RTCMMessage(b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
```

2. `scaling` boolean keyword argument added to `RTCMReader` and `RTCMMessage` constructors and `RTCMReader.parse()` method to turn attribute scaling on or off. Defaults to False (no scaling) during current alpha testing (*refer to Sphinx API documentation for usage*); will default to True in final version once the correct scaling factors have been verified (the RTCM 10403.n standard itself does not appear to state the applied scaling factors explicitly, but only indirectly via the 'resolution' parameter).

### RELEASE 0.1.6-alpha

FIXES:

1. Fix several grouped payload definitions for 1001-1004, 1009-1012, 1015-1017, 1021-1022, 1037-1039.

### RELEASE 0.1.5-alpha

FIXES:

1. Fix typo in payload definitions containing DF149.

### RELEASE 0.1.4-alpha

FIXES:

1. Fix 1013 message payload definition.
2. Fix nested group handling for messages 1059 & 1065.

### RELEASE 0.1.3-alpha

1. Additional message types added (message types 1020 - 1068).

### RELEASE 0.1.2-alpha

1. MSM (Multiple Signal Messages) message definitions & handling added (message types 1071 - 1127).

### RELEASE 0.1.1-alpha

1. Initial Alpha release. Core parsing functionality is reasonably solid, but only a limited number of message types are currently implemented and tested. In theory, missing types simply require appropriate definitions added to the `RTCM_PAYLOADS_GET` dictionary in `rtcmtypes_get.py` (** subject to further testing **).
2. In the meantime, `pyrtcm2` will return `<RTCM(nnnn, DF002=nnnn, status=Not_Yet_Implemented)>` for any RTCM messages types not yet defined.

### RELEASE 0.1.0-alpha

1. Initial release 