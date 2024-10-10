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
- [pyubx2](http://github.com/semuconsulting/pyubx2)
- [pynmeagps](http://github.com/semuconsulting/pynmeagps)

## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pyrtcm)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyrtcm?include_prereleases)
![Build](https://img.shields.io/github/actions/workflow/status/semuconsulting/pyrtcm/main.yml?branch=main)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyrtcm)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyrtcm)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyrtcm)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyrtcm.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyrtcm)

Parses RTCM3 messages into their constituent data fields - `DF002`, `DF003`, etc. Refer to the `RTCM_MSGIDS` dictionary in [`rtcmtypes_core.py`](https://github.com/semuconsulting/pyrtcm/blob/main/src/pyrtcm/rtcmtypes_core.py#L695) for a list of message types currently implemented. Additional message types can be readily added - see [Extensibility](#extensibility).

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyrtcm/](https://www.semuconsulting.com/pyrtcm/)

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyrtcm/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pyrtcm Discussions](https://github.com/semuconsulting/pyrtcm/discussions) channels.

---
## <a name="installation">Installation</a>

![Python version](https://img.shields.io/pypi/pyversions/pyrtcm.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyrtcm.svg?style=flat)](https://pypi.org/project/pyrtcm/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyrtcm.svg?style=flat)

`pyrtcm` is compatible with Python 3.9 - 3.13 and has no third-party library dependencies.

In the following, `python3` & `pip` refer to the Python 3 executables. You may need to substitute `python` for `python3`, depending on your particular environment (*on Windows it's generally `python`*).

The recommended way to install the latest version of `pyrtcm` is with [pip](http://pypi.python.org/pypi/pip/):

```shell
python3 -m pip install --upgrade pyrtcm
```

If required, `pyrtcm` can also be installed into a virtual environment, e.g.:

```shell
python3 -m pip install --user --upgrade virtualenv
python3 -m virtualenv env
source env/bin/activate (or env\Scripts\activate on Windows)
python3 -m pip install --upgrade pyrtcm
...
deactivate
```

For [Conda](https://docs.conda.io/en/latest/) users, `pyrtcm` is also available from [conda-forge](https://github.com/conda-forge/pyrtcm-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyrtcm/badges/version.svg)](https://anaconda.org/conda-forge/pyrtcm)
[![Anaconda-Server Badge](https://img.shields.io/conda/dn/conda-forge/pyrtcm)](https://anaconda.org/conda-forge/pyrtcm)

```shell
conda install -c conda-forge pyrtcm
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
from serial import Serial
from pyrtcm import RTCMReader
with Serial('/dev/tty.usbmodem14101', 9600, timeout=3) as stream:
  rtr = RTCMReader(stream)
  raw_data, parsed_data = rtr.read()
  if parsed_data is not None:
    print(parsed_data)
```
```
"<RTCM(1077, DF002=1077, DF003=0, DF004=204137001, DF393=1, DF409=0, DF001_7=0, ..., DF404_15=-9556, DF404_16=-2148, DF404_17=-2174)>",     
```

Example - File input (using iterator).
```python
from pyrtcm import RTCMReader
with open('rtcmdata.log', 'rb') as stream:
  rtr = RTCMReader(stream)
  for raw_data, parsed_data in rtr:
    print(parsed_data)
```

Example - Socket input (using iterator):
```python
import socket
from pyrtcm import RTCMReader
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("localhost", 50007))
  rtr = RTCMReader(stream)
  for raw_data, parsed_data in rtr:
    print(parsed_data)
```

---
## <a name="parsing">Parsing</a>

You can parse individual RTCM messages using the static `RTCMReader.parse(data)` function, which takes a bytes array containing a binary RTCM message and returns a `RTCMMessage` object.

**NB:** Once instantiated, an `RTCMMessage` object is immutable.

Example:
```python
from pyrtcm import RTCMReader
msg = RTCMReader.parse(b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7")
print(msg)
```
```
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
```

The `RTCMMessage` object exposes different public attributes depending on its message type or 'identity'. Attributes are defined as data fields (`DF002`, `DF003`, etc.) e.g. the `1097` multiple signal message (MSM) contains the following data fields:

```python
print(msg)
print(msg.identity)
print(msg.DF248)
print(msg.DF404_07)
```
```
"<RTCM(1097, DF002=1097, DF003=0, DF248=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=216181732825628672, NSat=5, DF395=1073872896, NSig=2, DF396=1023, NCell=10, PRN_01=007, PRN_02=008, PRN_03=021, PRN_04=027, ..., DF404_07=5534, DF404_08=5545, DF404_09=-7726, DF404_10=-7733)>",             
'1097'
204137001
5534
```

Attributes within repeating groups are parsed with a two-digit suffix (`DF419_01`, `DF419_02`, etc. See [example below](#iterating) for an illustration of how to iterate through grouped attributes).

Helper methods are available to interpret the individual datafields:

```python
from pyrtcm import RTCM_DATA_FIELDS, datadesc
dfname = "DF012"
print(RTCM_DATA_FIELDS[dfname])
print(datadesc(dfname))
```
```
(INT20, 0.0001, "GPS L1 PhaseRange - L1 Pseudorange")
'GPS L1 PhaseRange - L1 Pseudorange'
```

The `payload` attribute always contains the raw payload as bytes.

#### <a name="iterating">Iterating Through Group Attributes</a>

To iterate through a group of one or more repeating attributes in a given `RTCMMessage` object, the following construct can be used (in this illustration, repeating attributes CELLPRN, CELLSIG, DF405, DF406, DF407, DF408, DF420 and DF404 are extracted from an MSM 1077 message `msg` and collated in the array `msmarray`):

```python
msmarray = []
for i in range(msg.NCell): # msg = MSM 1077, number of cells = NCell
  vals = []
  for attr in ("CELLPRN", "CELLSIG", "DF405", "DF406", "DF407", "DF408", "DF420", "DF404"):
    val = getattr(msg, f"{attr}_{i+1:02d}")
    vals.append(val)
  msmarray.append(vals)
print(msmarray)
```
```shell
[['005', '1C', 0.00014309026300907135, 0.00014193402603268623, 341, 45.0, 0, -0.9231], ..., ['030', '2L', -0.00030865520238876343, -0.00030898721888661385, 341, 41.0, 0, -0.2174]]
```

The following dedicated helper methods are available to parse selected RTCM3 message types into a series of iterable data arrays:
- `parse_msm` - for MSM message types (e.g. 1077, 1125, etc.).
- `parse_4076_201` - for 4076_201 SSR (harmonic coefficients) message types.

---
## <a name="generating">Generating</a>

```
class pyrtcm.rtcmmessage.RTCMMessage(**kwargs)
```

You can create an `RTCMMessage` object by calling the constructor with the following keyword arguments:
1. payload as bytes

Example:

```python
from pyrtcm import RTCMMessage
msg = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
print(msg)
```
```
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
```

---
## <a name="serializing">Serializing</a>

The `RTCMMessage` class implements a `serialize()` method to convert a `RTCMMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `1005` message type:

```python
from serial import Serial
from pyrtcm import RTCMMessage
serialOut = Serial('COM7', 38400, timeout=5)
msg = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
print(msg)
output = msg.serialize()
print(output)
serialOut.write(output)
```
```
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.8028, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
b'\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7'
```

---
## <a name="examples">Examples</a>

The following examples are available in the /examples folder:

1. `rtcmpoller.py` - illustrates how to read and display RTCM messages 'concurrently' with other tasks using threads and queues. This represents a useful generic pattern for many end user applications.
1. `rtcmfile.py` - illustrates how to stream RTCM data from binary log file.
1. `rtcmsocket.py` - illustrates how to implement a TCP Socket reader for RTCM messages using RTCMReader iterator functionality.
1. `msmparser.py` - illustrates how to parse RTCM3 MSM (multiple signal messages) into a series of iterable data arrays keyed on satellite PRN and signal ID.
1. `rtcm_ntrip_client.py` - illustrates a simple [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) client using pyrtcm to parse the RTCM3 output.

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

A python/tkinter graphical GPS client which supports NMEA, UBX, RTCM3, NTRIP and SPARTN protocols is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyrtcm.svg)

`pyrtcm` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the utility useful, please consider sponsoring the project with the price of a coffee...

[![Sponsor](https://github.com/semuconsulting/pyubx2/blob/master/images/sponsor.png?raw=true)](https://buymeacoffee.com/semuconsulting)