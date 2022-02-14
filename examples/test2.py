from pyrtcm import RTCMReader

with open(
    "/Users/stevensmith/Dropbox/Development/workspace_vscode/pyrtcm/references/logs/RTCM3_MIX.log",
    "rb",
) as stream:
    rtr = RTCMReader(stream)
    for (raw, parsed) in rtr:
        print(parsed)
