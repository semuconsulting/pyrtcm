# pyrtcm

[Current Status](#currentstatus) |
[Installation](#installation) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Command Line Utility](#cli) |
[Graphical Client](#gui) |
[Author & License](#author)

`pyrtcm` is an original Python 3 parser for the RTCM3 &copy; GPS/GNSS protocol. RTCM3 is a proprietary GPS/GNSS [differential correction or DGPS](https://en.wikipedia.org/wiki/Differential_GPS) protocol published by the Radio Technical Commission for Maritime Services.

[RTCM STANDARD 10403.n DIFFERENTIAL GNSS (GLOBAL NAVIGATION SATELLITE SYSTEMS) SERVICES – VERSION 3](https://rtcm.myshopify.com/collections/differential-global-navigation-satellite-dgnss-standards/products/rtcm-10403-3-differential-gnss-global-navigation-satellite-systems-services-version-3-amendment-2-may-20-2021).

The `pyrtcm` homepage is located at [https://github.com/semuconsulting/pyrtcm](https://github.com/semuconsulting/pyrtcm).

This is an independent project and we have no affiliation whatsoever with the Radio Technical Commission for Maritime Services.

**FYI** There are companion libraries which handle standard NMEA 0183 &copy; and UBX &copy; (u-blox) GNSS/GPS messages:
- [pyubx2](http://github.com/semuconsulting/pyubx2) (**FYI** installing `pyubx2` via pip also installs `pynmeagps` and `pyrtcm`)
- [pynmeagps](http://github.com/semuconsulting/pynmeagps)

## <a name="currentstatus">Current Status</a>

<!--![Status](https://img.shields.io/pypi/status/pyrtcm)-->
![Release](https://img.shields.io/github/v/release/semuconsulting/pyrtcm?include_prereleases)
![Build](https://img.shields.io/github/actions/workflow/status/semuconsulting/pyrtcm/main.yml?branch=main)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyrtcm)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyrtcm)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyrtcm)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyrtcm.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyrtcm)

Parses RTCM3 messages into their constituent data fields. Refer to the `RTCM_MSGIDS` dictionary in [`rtcmtypes_core.py`](https://github.com/semuconsulting/pyrtcm/blob/main/pyrtcm/rtcmtypes_core.py) for a list of message types currently implemented. Additional message types can be readily added - see [Extensibility](#extensibility)).

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyrtcm](https://www.semuconsulting.com/pyrtcm).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyrtcm/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided.

---
## <a name="installation">Installation</a>

`pyrtcm` is compatible with Python >=3.7 and has no third-party library dependencies.

In the following, `python` & `pip` refer to the Python 3 executables. You may need to type 
`python3` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pyrtcm.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyrtcm.svg?style=flat)](https://pypi.org/project/pyrtcm/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyrtcm.svg?style=flat)

The recommended way to install the latest version of `pyrtcm` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python -m pip install --upgrade pyrtcm
```

If required, `pyrtcm` can also be installed into a virtual environment, e.g.:

```shell
python3 -m pip install --user --upgrade virtualenv
python3 -m virtualenv env
source env/bin/activate (or env\Scripts\activate on Windows)
(env) python3 -m pip install --upgrade pyrtcm
...
deactivate
```

---
## <a name="reading">Reading (Streaming)</a>

```
class pyrtcm.rtcmreader.RTCMReader(stream, **kwargs)
```

You can create a `RTCMReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper). `pyrtcm` implements an internal `SocketStream` class to allow sockets to be read in the same way as other streams (see example below).

Individual RTCM messages can then be read using the `RTCMReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `RTCMMessage`, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `RTCMReader` also implements an iterator.

Example -  Serial input:
```python
>>> from serial import Serial
>>> from pyrtcm import RTCMReader
>>> stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
>>> rtr = RTCMReader(stream)
>>> (raw_data, parsed_data) = rtr.read()
>>> print(parsed_data)
 <RTCM(1077, DF002=1077, DF003=0, GNSSEpoch=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=760738918298550272, NSat=10, DF395=1073807360, NSig=2, DF396=1044459, DF397_01(005)=75, DF397_02(007)=75, DF397_03(009)=81, ..., DF404_19(030,1C)=0.0, DF404_20(030,2L)=0.0)>,
```

Example - File input (using iterator).
```python
>>> from pyrtcm import RTCMReader
>>> stream = open('rtcmdata.log', 'rb')
>>> rtr = RTCMReader(stream)
>>> for (raw_data, parsed_data) in rtr: print(parsed_data)
...
```

Example - Socket input (using enhanced iterator):
```python
>>> import socket
>>> from pyrtcm import RTCMReader
>>> stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
>>> stream.connect(("localhost", 50007))
>>> rtr = RTCMReader(stream)
>>> for (raw_data, parsed_data) in rtr.iterate(): print(parsed_data)
```

---
## <a name="parsing">Parsing</a>

You can parse individual RTCM messages using the static `RTCMReader.parse(data)` function, which takes a bytes array containing a binary RTCM message and returns a `RTCMMessage` object.

**NB:** Once instantiated, an `RTCMMessage` object is immutable.

Example:
```python
>>> from pyrtcm import RTCMReader
>>> msg = RTCMReader.parse(b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7")
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
```

The `RTCMMessage` object exposes different public attributes depending on its message type or 'identity'. Attributes are defined as data fields ("DF002", "DF003", etc.) e.g. the `1005` message contains the following data fields:

```python
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
>>> msg.identity
'1005'
>>> msg.DF024
1
```

Helper methods are available to interpret the individual datafields:

```python
>>> from pyrtcm import RTCM_DATA_FIELDS, datasiz, datascale, datadesc
>>> dfname = "DF012"
>>> RTCM_DATA_FIELDS[dfname]
(INT20, 0.0001, "GPS L1 PhaseRange - L1 Pseudorange")
>>> datasiz(dfname) # size in bits
20
>>> datascale(dfname) # scaling factor
0.0001
>>> datadesc(dfname) # description
'GPS L1 PhaseRange - L1 Pseudorange'
```

The `payload` attribute always contains the raw payload as bytes.

Attributes within repeating groups are parsed with a two-digit suffix ("DF030_01", "DF030_02", etc.). 

**Tip:** To iterate through a repeating group of attributes (*e.g., DF406 (GNSS signal fine PhaseRange)*), the following construct can be used:

```
df406group = [] # list of DF406 ((GNSS signal fine PhaseRange) values from repeating group in MSM 1077 message
ncell = msg.NSat * msg.NSig # size of repeating group
for i in range(ncell):
    df406 = getattr(msg, f"DF406_{i+1:02}")
    df406group.append(df406)
```

Attributes within MSM NSAT and NCELL repeating groups can optionally be labelled with their corresponding satellite PRN and signal ID when the `__str__()` method is invoked, by setting the keyword argument `labelmsm` to True (e.g. `DF405_10(014,2C)` signifies that the 10th item in the DF405 group refers to satellite PRN 014, signal ID 2C).

---
## <a name="generating">Generating</a>

```
class pyrtcm.rtcmmessage.RTCMMessage(**kwargs)
```

You can create an `RTCMMessage` object by calling the constructor with the following keyword arguments:
1. payload as bytes

Example:

```python
>>> from pyrtcm import RTCMMessage
>>> msg = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
```

---
## <a name="serializing">Serializing</a>

The `RTCMMessage` class implements a `serialize()` method to convert a `RTCMMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `1005` message type:

```python
>>> from serial import Serial
>>> serialOut = Serial('COM7', 38400, timeout=5)
>>> from pyrtcm import RTCMMessage
>>> msg = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
>>> output = msg.serialize()
>>> output
b'\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7'
>>> serialOut.write(output)
```

---
## <a name="examples">Examples</a>

The following examples are available in the /examples folder:

1. `rtcmserial.py` - illustrates how to stream RTCM data from serial/UART port.
1. `rtcmfile.py` - illustrates how to stream RTCM data from binary log file.
1. `rtcmsocket.py` illustrates how to implement a TCP Socket reader for RTCM messages using RTCMReader iterator functionality.
1. `rtcmbuild.py` - illustrates how to construct RTCM payload from constituent datafields.
1. `ntripclient.py` - illustrates a simple [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) client using pyrtcm to parse the RTCM3 output.

---
## <a name="extensibility">Extensibility</a>

The RTCM protocol is principally defined in the modules `rtcmtypes_core.py` and `rtcmtypes_get.py` as a series of dictionaries. RTCM uses a series of pre-defined data fields ("DF002", DF003" etc.), each of which has a designated data type (UINT32, etc.). Message payload definitions must conform to the following rules:

```
1. datafield names must be unique within each message class
2. datafield types must be one of the valid data fields ("DF026", "DF059", etc.)
3. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'DF029'
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix ("DF030_01", "DF030_02", etc.). Nested repeating groups are supported.

---
## <a name="cli">Command Line Utility</a>

A command line utility `gnssdump` is available via the `pygnssutils` package. This is capable of reading and parsing NMEA, UBX and RTCM3 data from a variety of input sources (e.g. serial, socket and file) and outputting to a variety of media in a variety of formats. See https://github.com/semuconsulting/pygnssutils for further details.

To install `pygnssutils`:
```
python3 -m pip install --upgrade pygnssutils
```

For help with the `gnssdump` utility, type:
```
gnssdump -h
```

---
## <a name="gui">Graphical Client</a>

A python/tkinter graphical GPS client which supports NMEA, UBX and RTCM3 protocols is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyrtcm.svg)

`pyrtcm` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the library useful, a small donation would be greatly appreciated!

[![Donations](https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?business=UL24WUA4XHNRY&no_recurring=0&item_name=The+SEMU+GNSS+Python+libraries+are+maintained+entirely+by+unpaid+volunteers.+All+donations+are+greatly+appreciated.&currency_code=GBP)