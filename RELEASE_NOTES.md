# pyrtcm Release Notes

### RELEASE 0.1.2-alpha

1. MSM (Multiple Signal Messages) message definitions & handling added (message types 1071 - 1127).

### RELEASE 0.1.1-alpha

1. Initial Alpha release. Core parsing functionality is reasonably solid, but only a limited number of message types are currently implemented and tested. In theory, missing types simply require appropriate definitions added to the `RTCM_PAYLOADS_GET` dictionary in `rtcmtypes_get.py` (** subject to further testing **).
2. In the meantime, `pyrtcm2` will return `<RTCM(nnnn, DF002=nnnn, status=Not_Yet_Implemented)>` for any RTCM messages types not yet defined.

### RELEASE 0.1.0-alpha

1. Initial release 