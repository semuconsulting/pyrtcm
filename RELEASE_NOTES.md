# pyrtcm Release Notes

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