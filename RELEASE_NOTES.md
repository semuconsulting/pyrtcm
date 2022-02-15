# pyrtcm Release Notes

## RELEASE 0.1.1

1. Initial Alpha release. Core parsing functionality is there, but lacks comprehensive RTCM payload definitions. In theory, these simply need adding to the `RTCM_PAYLOADS_GET` dictionary in `rtcmtypes_get.py` - no code changes should be necessary in `RTCMReader` or `RTCMMessage` (*subject to more comprehensive testing*). 
2. In the meantime, will return `<RTCM(nnnn, DF002=nnnn, status=Not_Yet_Implemented)>` for any RTCM messages types not yet defined.

### RELEASE 0.1.0

1. initial release 