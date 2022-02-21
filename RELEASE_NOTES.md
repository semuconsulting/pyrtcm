# pyrtcm Release Notes

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