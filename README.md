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

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyrtcm](https://www.semuconsulting.com/pyrtcm).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyrtcm/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pyrtcm Discussions](https://github.com/semuconsulting/pyrtcm/discussions) channels.

---
## <a name="installation">Installation</a>

`pyrtcm` is compatible with Python >=3.8 and has no third-party library dependencies.

In the following, `python3` & `pip` refer to the Python 3 executables. You may need to type 
`python` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pyrtcm.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyrtcm.svg?style=flat)](https://pypi.org/project/pyrtcm/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyrtcm.svg?style=flat)

The recommended way to install the latest version of `pyrtcm` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python3 -m pip install --upgrade pyrtcm
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

For [Conda](https://docs.conda.io/en/latest/) users, `pyrtcm` is also available from [conda-forge](https://github.com/conda-forge/pyrtcm-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyrtcm/badges/version.svg)](https://anaconda.org/conda-forge/pyrtcm)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyrtcm/badges/downloads.svg)](https://anaconda.org/conda-forge/pyrtcm)

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
  print(parsed_data)
```
```
 <RTCM(1077, DF002=1077, DF003=0, GNSSEpoch=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=760738918298550272, NSat=10, DF395=1073807360, NSig=2, DF396=1044459, DF397_01(005)=75, DF397_02(007)=75, DF397_03(009)=81, ..., DF404_19(030,1C)=0.0, DF404_20(030,2L)=0.0)>,
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

The `RTCMMessage` object exposes different public attributes depending on its message type or 'identity'. Attributes are defined as data fields (`DF002`, `DF003`, etc.) e.g. the `1087` multiple signal message (MSM) contains the following data fields:

```python
print(msg)
print(msg.identity)
print(msg.DF034)
print(msg.DF419_03)
```
```
<RTCM(1087, DF002=1087, DF003=0, DF416=2, DF034=42119001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=4039168114821169152, NSat=7, DF395=1090519040, NSig=2, DF396=16382, NCell=13, PRN_01=003, PRN_02=004, PRN_03=005, PRN_04=013, PRN_05=014, PRN_06=015, PRN_07=023, DF397_01=69, DF397_02=64, DF397_03=73, DF397_04=76, DF397_05=66, DF397_06=70, DF397_07=78, DF419_01=12, DF419_02=13, DF419_03=8, DF419_04=5, DF419_05=0, DF419_06=7, DF419_07=10, DF398_01=0.6337890625, DF398_02=0.3427734375, DF398_03=0.25390625, DF398_04=0.310546875, DF398_05=0.5126953125, DF398_06=0.8271484375, DF398_07=0.8837890625, DF399_01=-665, DF399_02=29, DF399_03=672, DF399_04=-573, DF399_05=-211, DF399_06=312, DF399_07=317, CELL_01=('003', 'G1'), CELL_02=('003', 'G2'), CELL_03=('004', 'G1'), CELL_04=('004', 'G2'), CELL_05=('005', 'G1'), CELL_06=('005', 'G2'), CELL_07=('013', 'G1'), CELL_08=('013', 'G2'), CELL_09=('014', 'G1'), CELL_10=('014', 'G2'), CELL_11=('015', 'G1'), CELL_12=('015', 'G2'), CELL_13=('023', 'G1'), DF405_01=0.00024936161935329437, DF405_02=0.0002511627972126007, DF405_03=-4.678964614868164e-05, DF405_04=-5.141831934452057e-05, DF405_05=1.1144205927848816e-05, DF405_06=2.15042382478714e-05, DF405_07=0.00047079287469387054, DF405_08=0.0004794951528310776, DF405_09=-0.0003879182040691376, DF405_10=-0.00037603825330734253, DF405_11=0.0002771839499473572, DF405_12=0.0002871435135602951, DF405_13=-0.00023611821234226227, DF406_01=0.00024937279522418976, DF406_02=0.00025077443569898605, DF406_03=-4.834495484828949e-05, DF406_04=-5.1246024668216705e-05, DF406_05=1.1149328202009201e-05, DF406_06=2.1803192794322968e-05, DF406_07=0.00047026341781020164, DF406_08=0.0004848274402320385, DF406_09=-0.0003876127302646637, DF406_10=-0.0003757951781153679, DF406_11=0.0002778824418783188, DF406_12=0.0002880701795220375, DF406_13=-0.00023698341101408005, DF407_01=341, DF407_02=341, DF407_03=340, DF407_04=340, DF407_05=341, DF407_06=341, DF407_07=340, DF407_08=341, DF407_09=341, DF407_10=341, DF407_11=341, DF407_12=341, DF407_13=340, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=0, DF420_09=0, DF420_10=0, DF420_11=0, DF420_12=0, DF420_13=0, DF408_01=47.0, DF408_02=40.0, DF408_03=47.0, DF408_04=42.0, DF408_05=47.0, DF408_06=39.0, DF408_07=36.0, DF408_08=33.0, DF408_09=48.0, DF408_10=43.0, DF408_11=48.0, DF408_12=40.0, DF408_13=41.0, DF404_01=-0.8193, DF404_02=-0.8173, DF404_03=0.8539, DF404_04=0.8501000000000001, DF404_05=0.7333000000000001, DF404_06=0.7311000000000001, DF404_07=-0.24930000000000002, DF404_08=-0.2543, DF404_09=-0.21580000000000002, DF404_10=-0.21780000000000002, DF404_11=0.3924, DF404_12=0.3947, DF404_13=0.6146)>    
'1087'
42119001
8
```

Attributes within repeating groups are parsed with a two-digit suffix (`DF419_01`, `DF419_02`, etc. See [example below](#iterating) for an illustration of how to iterate through grouped attributes).

Helper methods are available to interpret the individual datafields:

```python
from pyrtcm import RTCM_DATA_FIELDS, datasiz, datascale, datadesc
dfname = "DF012"
print(RTCM_DATA_FIELDS[dfname])
print(datasiz(dfname))
print(datascale(dfname))
print(datadesc(dfname))
```
```
(INT20, 0.0001, "GPS L1 PhaseRange - L1 Pseudorange")
20
0.0001
'GPS L1 PhaseRange - L1 Pseudorange'
```

The `payload` attribute always contains the raw payload as bytes.

#### <a name="iterating">Iterating Through Group Attributes</a>

To iterate through a group of one or more repeating attributes in a given `RTCMMessage` object, the following construct can be used (in this illustration, repeating attributes DF405, DF406, DF407, DF408, DF420 and DF404 are extracted from an MSM 1077 message `msg` and collated in the array `msmarray`):

```python
msmarray = []
for i in range(msg.NCell): # msg = MSM 1077, number of cells = NCell
  vals = []
  for attr in ("DF405", "DF406", "DF407", "DF408", "DF420", "DF404"):
    val = getattr(msg, f"{attr}_{i+1:02d}")
    vals.append(val)
  msmarray.append(vals)
print(msmarray)
```
```shell
[[0.00014309026300907135, 0.00014193402603268623, 341, 45.0, 0, -0.9231], [0.00014183297753334045, 0.00014339853078126907, 341, 38.0, 0, -0.9194], ... etc.]
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

`pyrtcm` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the library useful, a small donation would be greatly appreciated!

[![Donations](https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?business=UL24WUA4XHNRY&no_recurring=0&item_name=The+SEMU+GNSS+Python+libraries+are+maintained+entirely+by+unpaid+volunteers.+All+donations+are+greatly+appreciated.&currency_code=GBP)