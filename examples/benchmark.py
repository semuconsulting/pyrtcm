"""
pyrtcm Performance benchmarking utility

Usage (kwargs optional): python3 benchmark.py cycles=10000

Created on 18 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

# pylint: disable=line-too-long

from platform import python_version
from platform import version as osver
from sys import argv
from time import process_time_ns

from pyrtcm._version import __version__ as rtcmver
from pyrtcm.rtcmreader import RTCMReader

RTCMMESSAGES = [
    b"\xd3\x00\x93>\xb0\x00L\n\xdb\xa2\xb0\t\xaec\xb1\xe1\xde\x7f\xf0hz\x9c{\xf8`T\x15\x9f\x99>\xff\x83\x17\xf3d_\xd5\x06\x93,s\xad\xc7\xfc0-\xe7k\xfe!\xb9\xbcd\x02\xe4\x7f\xe0\x8b\x01\xdb\xb7\xf2I\x17\xfa\xe0y#\xff\x06\x1c$E?\x8c\t\xff\x91\x01c\x0f\xf8G\xe0\xf7\x8f\xfd0\x851\xc7\xdd\x8c\xff\xc1h\xf9\x7f?\xef\x85w\x00\xfe\xe1\xe3\xfe\x10\xb7\xf1Y\xffDNL\xef\xef\xf7\xbf\xf0|\xbd\x88\xd7\xf8\xe7e\x19\x90\x02@e\x87,\x10.\xaaAB_\x8c}k7\xfc\x1ao\xba\xf5\xfe\xe5\x8c/",
    b"\xd3\x00\xb4>\xc0\x00L\n\xdb\xa2\xb0\t\xaec\xb1\xe1\xde\x7f\xd2\xeb0hz\x9c{\xfb\xe8`T\x15\x9f\x99>\xfe\x8d\x8d\x83\x17\xf3d_\xf4\x15\x06\x93,s\xad\xc7\xf4\xf9\xac0-\xe7k\xfe\x9c!\xb9\xbcd\x02\xe4\x7f\xa1\xe2`\x8b\x01\xdb\xb7\xfa\xf2I\x17\xfa\xe0y#\xfd\x1f\x03\x06\x1c$E?\xe5\x0c\t\xff\x91\x01c\x0f\xe9\xd3\xf8G\xe0\xf7\x8f\xfe=0\x851\xc7\xdd\x8c\xffN\xa3\xc1h\xf9\x7f?\xed\xcf\x85w\x00\xfe\xe1\xe3\xfa}V\x10\xb7\xf1Y\xff\x94DNL\xef\xef\xf7\xbf\xd3(\xb0|\xbd\x88\xd7\xfcX\xe7e\x19\x90\x02@d\xa7\x11\x87,\x10.\xaaR\xc1B_\x8c}k7\xf4Ll\x1ao\xba\xf5\xff\xa0\xd4\x82+",
    b"\xd3\x00\x13>\xd0\x00\x03\x84\x1a\x86\x92\xbf\xb4KK\xf4\xfa\xb7\xdc7b\x8a3\x84y",
    b"\xd3\x00\x15>\xe0\x00\x03\x84\x1a\x86\x92\xbf\xb4KK\xf4\xfa\xb7\xdc7b\x8a\x01W\x1b\xa9\xd6",
    b"\xd3\x00\x19>\xf0\x00\x14SEPCHOKE_B3E6   SPKE\x00\x07nf",
    b"\xd3\x00\x1e?\x00\x00\x14SEPCHOKE_B3E6   SPKE\x00\x045856\xffh\x94",
    b'\xd3\x00H?\x10\x00\x86\x85\x03\x14\x00$4\x07\xbaAt\x0b\xfa\xc2 3\x11=\xa0+\xfb\x04\xb8q\x80\xc0\xbd\xdf\xf9\x06\xb8\xd7U\x80u\xbb\xf8\xe6 \xc5\x18=#\xb7\xfa\xe5\\\x85\xd8\x80\\\x83\xf9@m\x8d%\x01\xb17\xf9"\xbdz\xc2\x81h\x03\xf8\x9f\xc6\xe6',
    b'\xd3\x00W? \x00\x86\x85\x03\x14\x00$4\x07\xbaAt\x0b\xfaZe\x84@f"{@W\xf4x\xec\x12\xe1\xc6\x03\x02\xf7\x7f\xe9m\xc85\xc6\xba\xac\x03\xad\xdf\xd0\xe9\x8eb\x0cQ\x83\xd2;\x7f\xa4\xc1\\\xab\x90\xbb\x10\x0b\x90\x7fA\x96P\x1bcI@lM\xfe\x96p\x91^\xbda@\xb4\x01\xfd-\x90\xbb\x83T',
    b"\xd3\x00s?0\x00\x86\x85\x03\x14\x00$4\x07\xbaAt\x0b\xf8\x17\x88KV\xe9XD\x06b'\xb4\x05\x7f\x02Y\xf7\xc6\x8f\xec\x12\xe1\xc6\x03\x02\xf7\x7f\xe0X\x01\xaf/\xfc\x83\\k\xaa\xc0:\xdd\xfc\x07h\x1f`\xbf\x8eb\x0cQ\x83\xd2;\x7f\x81\\z\x8fw\xf5\xca\xb9\x0b\xb1\x00\xb9\x07\xf2\x00\x08\x00\x00\x00P\x1bcI@lM\xfe@\x01\x00\x00\x00\t\x15\xeb\xd6\x14\x0b@\x1f\xc0\xe2\x859\x13\xf8'\xe0X",
    b"\xd3\x00\x8a?@\x00\x86\x85\x03\x14\x00$4\x07\xbaAt\x0b\xfaZ`/\x10\x96\xad\xd3\x1c\xb0\x88\x0c\xc4Oh\n\xfe\x8f\x1c\tg\xdf\x1a?\xdc\xb0K\x87\x18\x0c\x0b\xdd\xff\xa5\xb7\x02\xc0\ry\x7f\xf5d\x1a\xe3]V\x01\xd6\xef\xe8t\xc0v\x81\xf6\x0b\xfe0\xe6 \xc5\x18=#\xb7\xfaL\x10+\x8fQ\xee\xfff\xb9W!v \x17 \xfe\x83,\x80\x02\x00\x00\x00\x00\x14\x06\xd8\xd2P\x1b\x13\x7f\xa5\x9c \x00\x80\x00\x00\x00\x04\x8a\xf5\xeb\n\x05\xa0\x0f\xe9l\x80\xe2\x859\x13\xfd8\x0e\x8f\xad",
    b"\xd3\x00\t?P\x00\xeb\xdet\xa7\x80Hj\x9a\x85",
    b"\xd3\x00=?\xb0\x90\x10z\xa4\xb9O\x1a\x00\x006\xc2HX\xb9\xf1W.\tX\x1c\x10S\xf3\xa6\x08@\xcey\x11\xf0\xa1\r\xb5\xfdO\x1a\x00\x82\x87\x11\xb6\xbb\x00\t'n\xc4\x03\x1aJ\xce1[\x86\xff\xaa\xe6\xda\x00\x8eV+",
    b"\xd3\x00-?\xc2K\xb3x\xcf\xa0\xf4\x96L\xb5\xd1\xa0\r\x84\xba\x00!\x1b\xf2\xa7\xf6H\xbfY\x16c\x80-\x16\xf4\xa5\x01P\x92\xc2L\x00\x00\x00\x1a\x00\x00\x08\x00\xc2\xb9\xe5",
    b"\xd3\x00\x10@P\x00\xeb\xdet\xa7\x87\x07Unknown\x95\x8eL",
    b"\xd3\x009@\x90\x00\x14SEPCHOKE_B3E6   SPKE\x00\x045856\x0cSEPT POLARX5\x055.5.0\x073075024\xb9\x1f\xbd",
    b"\xd3\x00@A#\x07j\x1d\xae\r5a\xfd\xbf\xdd\xca\xe40\x86\x17\xcc\x82M}\xe2\xf5^\x87\xea\xa4\x00H\x1c\xa7\x85\x19T\xa2\xa1\x07)\xab\x00\x01a\xd1\x8av\x03\xff\xd8(\x0b\xc4\xdd\x11!\xb1\r\x0f\xce\x7f\xec\xfc\x01\x80\x10\r8\x18",
    b"\xd3\x00>AP\xd4\x04\x16k\xfb\xb9K@?\xfe\x89\xff\x97\x1c\x1b\xeb\xf0\xa0R\xea\xd2E\x93\xf0<\x00v5<#\xfa\xa8\x12\xf5\x11KO\xfe\xfe\n\x10\xff\x7f\xfe\xf2r8\xa5\xd1\xef\xdfR:5O\xfb\xf9\x904\x00\xe7/\xc4",
    b'\xd3\x00?AaT\x04\x16k\xfb\xb1K@\x00\x01\xf4\x13^h\xc3\xe9\xe8\xa0\xbc#7\x08?\xef`\x00}\xaa\xcc"\xe6\xa8\x12\xf4\x19KO\xff\xde\n\x11\x82\xcf\xff\xd2r:\xe3\xe1\xf0\\l\xc0|\x0f\xfb\xf1\xe0L\x15\x00%A\xd4',
    b'\xd3\x01\x89C@\x00L\n\xdb\xa2\x00 {@T\x00\x00\x00\x00\x00( \x81\x01}\xc7\xdf\xfd\xc7\xdeq\xc2"Z2\x1ar\x9a:br|\xa5\xe1\x83\x0fp[\t(\xc5x\x96\x1d\x93\xc2a:\xd9\x95\x9a\xe9Z\x05\x95y\xa9\xb9\xa3\x9bW\xf9\xd6\xd5a\xca\x1e\x1c\x02c\x83\xc6:}\xe3\xa1a\xa9?\x1a\x81\xb1\xbc\xb4\x9b\xd09\xc9H\x9a\x9a\x7f\x0c\xf5\xf0\xbe_5(s\x86\xd7>\x8cm\xcb\x8e\xdb\x8c\xf1\xce\xc6\xcdYl\xb7\x96\xe8\xa4\xee\x9f\xae\xeb\xcf\x91\xb3\x19\x19j\x13\xdf\xe9@\t\xe2\x83N#Pd\x16G|\xce\xf7\x85o\xb2\xa7\x84\\\xbd\x04\\\xbd\x04u\x04\x84{\xd9\x04^\x17\x856\xf6\x056\xf6\x04}\x05w\xbab\xf7\xbab\xf7\xbd\xc5\xf7\xcbn\xf7\xaf\x8c\x06\xb9\xb5\x06\xb9\xb5\x07\x0fy\x87F"\x87\x83\xc3\x86\xf9\x9d|[z|[z}\x11g\xfd\x078\xfd C\xfbv\xe8{v\xe8|Z\xb6\xfb\xa1\xc3\xfb\xa1\xc3\xfc9\x1c|[U|\x95\xb2\x83\x86\xf5\x03\x86\xf5\x03R\x12\x03j\tx%Tx%Tw\xe6b{1\x03{1\x03z2-O\xd3\xf4\xfd?O\xd45\rCOs\xdc\xf7=\xcfst\xdd7M\xf3|\xdf\x17\xc5\xd1t_\x17\xb0\xeb\xca\xf3#H\xd24\x91&Ms\\\xd75\xcb\x92\xe4\xb9D\xd14H\x00\x00\x00\x00\x01\x8b\xe8:\r\xb7\xb1\xd6\x0f\xab\xeb\x8cg\xf9\xfd\xb7\xaa\xe2\x15\xed{\x90\xedYD\xf9\x1eG\x93\xc5\x95\x11%IV\x01\x95eV^\x85D\xc5\x91d\xb3G6\xcd\xb4\xce\x9b&\xc0{\xf6\x0e',
    b"\xd3\x01\xeeCP\x00L\n\xdb\xa2\x00\x00{@T\x00\x00\x00\x00\x00( \x81\x01}\xc7\xdf\xfd\xc7\xdeq\xc2\"b2\x1ar\x9a:brx\x00\x00\x00\x00\x07\x84\x99\xb1\x1a\xf3;\xc1V\xd0\xfbv\xd5\x82V\x15\xe8\x0b\xe0L{\x11\xe8\x1f\xd9`\xd3\x00\xca\x19)V\xd4\x15X\x81t\\\x97K9rI\x1d=\x01\xcf\xac\x1f\x10\x1e7\x91co\x1eS+\xe5V\xd6U\x05\x9cA\xc9\xc2\xf8\x9dy!\xd7\xe1\x1eBa\xc4\x85r\x8c\xf7'\xbfu\x10\x1fTF\xf5\xa6f\xf8\xbdoy\x178\xf0\xee\x8c\xae\xe6\xea\xf0Ag\x05lpt\x115\xb8\x13?\x01X\x84\x95\xa9\x06C\"\xe3\xe3\xde\\Rym\xa7\x92a\xfc\xcb0LwPLwPM\xfb\xd0Ni\x18L\x8d\x00Y\xfa\x90Y\xfa\x90N[\x87\x82b\x0f\x82b\x0f\x82\x98?\x83r\xd7\x81\xb4\xa0rR\xb0rR\xb0w\xae\xf8{\x19\x80~\xf3\x90vQ/\xcc\xae\x0f\xcc\xae\x0f\xd8\x0c\xe7\xd7i\xef\xd8\xfa\xa7\xbeo\x9f\xbeo\x9f\xcc\xac\x87\xc0\xf8\xa7\xc0\xf8\xa7\xcan'\xcc\x91\xb7\xd07\x88?\x10\xe0?\x10\xe0;\xc2\xb8=B'\x89\x10\xbf\x89\x10\xbf\x85!\x9f\xb9\x93\x07\xb9\x93\x07\xa9\xa5\xa4\xfd?O\xd3\xf4\xfdCP\xd44\xf7=\xcfs\xdc\xf77M\xd3t\xdf7\xcd\xf1|]\x17E\xf1{\x0e\xbc\xaf24\x8d#I\x12d\xd75\xcds\\\xb9.K\x94M\x13D\x80\x00\x00\x00\x00\x18\xbe\x83\xa0\xdb{\x1d`\xfa\xbe\xb8\xc6\x7f\x9f\xdbz\xae!^\xd7\xb9\x0e\xd5\x94O\x91\xe4y<YQ\x12T\x95`\x19VUe\xe8TLY\x16K4sl\xdbL\xe9\xb2m\xd53\xaagT\xbe\xab\xddU\xfcJ\xf8\x95\xf1\x00Ad\x82\xc9\x05!\xfdD\x17:\xa9uR\xea\xb1\xd5\x0b\xaaOW Y\x00\xb2\x01n\x03_\x02\xfe\n\x0c\x14\x18*\x81\xc9#\x92G&\x0fk\x1dnC\xcc\x87\x99\x0e\xf27\x9b\xd6\xb7\xadoQ\xef{\xde\xf7\xbd\xa04A$",
    b"\xd3\x01\x0fC\xe0\x00p\xd0\xa0b\x00 A\xe0\x03\x80\x00\x00\x00\x000\xc0\x00\x00\x7f\xff\xe7\xe7\xa5$!%\xa5\xa3 \xa5t\x92_\xf4&\xf5R\x0c\xf3\xf9\xf0\xb5/\x0cxt\x00\x17B\x8b\xf6'\x7fa\xf7y2\xc7\x91\xfa\xfa\xa3\x0f\xac\x95|\xb4\xf7\xcb\r~\xc4\x17\xed\x08\x82\xb9\xd8({v\xb6\x87f2hb\xd6\x87)k\x03\xf6\xb1\xe2z\n_\xa0\x0br\xbc\x9f-\x0b\xf5\xd0w\\\x9e|\xd3\xc6\xfc\x8a\x81\xfd;\x0c\xfd-\xbd\xfcA\xf2\xfcaR|R\x12|l\xfa~\xddX\xfe\xdf\xfa\x7f\x89g\xffd{\x80R1\x00q\xa6\x82\x07\x9e\x02\x11\xd5~o\xb5\xfe_\xff\xf9\x08\x8a\xf9-@y-\x03\xf9\x12\x1f~\xac\x01~\x94{}\x04\x0f} \xdb~1#}\xed\xe2\xc3\x90\xeb\xbe\xe3\xd04\x05\x03@\xcd\xb3l\xdb6\xc8R\x14\x85!D\xb1$\xfb?O\xb3\xf4\xc92D\xd1,E\x11\x00\x00\x00\x053DG\x11\x96\x07{\xd9\xb6\xae\x95\xa4c8\xf5\x8f_\xd3t\x94\xdd4\xe3x\xc5\xcbx\xe5\xd9e\xb9fU\xb5XM\x94\x1b",
    b"\xd3\x01VC\xf0\x00p\xd0\xa0b\x00\x00A\xe0\x03\x80\x00\x00\x00\x000\xc0\x00\x00\x7f\xff\xe7\xe7\xa5\xa4!\xa5\xa6# \xa5\xc6j\x82T\xa2\x9d\xda\xd4\xde\xa3]\x8f\xd2\xb1\xfc\xfa\x0eP\n\x1f\xc5\xfb\xa0\x16\x80\x05\xfe\xc1rm\xdf(\x03u\xb8\xc7^\x16w\xcf'|rz\xdao\xacu|RW\xc7\x89~d?\xe6\x01\x00wP\x08<\x84m\x18C\xafxr\xaf\x81\xf4\xea\x05>\xa1O\xec\xa6^\xcc\x08\xfb\xbaO\xbb\ntzWH\xe7w\x8e/xy\xfdA\xf2\xfc\xf8\xad}\xa98}\x9b\xe9|\xab\xdd\xfc\xcb<\xfc\xbb\xfc\xfc\xd6\xe4\xffI*\x7fK\xcb\xff\xf59\x7f\xd0M\x00\xbf\x01\x00\xdev\x82tn\x02~\xa5~\xde\xbf\xfe\xcf\tyq%y\x95\xda\xf9\x95\x9eyz\xb9\xff\x17\xfd\xff\x00w\xfds}\xfd\x90I\xfe\xa0\x91\xfe]QC\x90\xeb\xbe\xe3\xd04\x05\x03@\xcd\xb3l\xdb6\xc8R\x14\x85!D\xb1$\xfb?O\xb3\xf4\xc92D\xd1,E\x11\x00\x00\x00\x053DG\x11\x96\x07{\xd9\xb6\xae\x95\xa4c8\xf5\x8f_\xd3t\x94\xdd4\xe3x\xc5\xcbx\xe5\xd9e\xb9fU\xb5^\xfd\x0e\x13[\xe0\xb8U\x8fb\x1f\xa8?\xb8\x8b\xa9\x0c\xd2\x1e\x04C\xc9:p\x94\xe27\xbf\x97\x8f\x10B\xe0\x9f\xbe\xb1\xbdl\xfa\xb7\xfa`\x13\xb4%\xbf\x83/\t\xfe-\xbc\xe2\x807\xcbM",
    b'\xd3\x01FD\x80\x00L\n\xdb\xa2\x00 \x14\x85 \x00 \x00\x00\x00 \x81\x11\x00\x7f\xff\xff\xff\xf4\xf5u\x054\xd5\xc5i\xe0\x8fg\xf2\xcd\xf39\xe0\xf61\xf7l\xf2w\x02{qG\xf77`\x01?\xc1\x93 "|\x02^<)\xbc\x8d-D\xdc\x1e\x8d\xd7\x04\xde\xbd\xce\x0fx*.\x83N`9\xfa\x83\xb9\xe8=\xce\xc9=x\x9d\xc0J\x16H\xa2\xa4\xcaM\xd8\xa5\xc9KO\xf4\xb9\xbbK\xbfd\xbew\x8c:t\xd7\xa4\x8d\xd8\x0c\xdf\x01N\x1c\xfb\xd5\x08o\xd5U\xc7\xd5\x97\x87\xd5\x8cc\xd5\xb5\xc7\xe7pg\xe0\xb5\xdf\xde\xea{\xde\x85K\xde\x19\x9c6\xe4\x9c;\x88p<~\xdc=\x97$=\xb1\xd4\x0b\x98\xe8\x0e\xec\x9c\x10w\x90\x110\xb8\x11?<!\r\xc8 Z\xa4 ``!1X!\x1fd\x1c\xfdx\x1b\xd18\x1a\x98\xc4\x1a\xd1 \x1a\xcd\xa4 \xf3D\x1d\xe5 \x1cg\x9c\x1d\x16\x08\x1b\xfcF\x82\xa0\xe8:\x0e\x83\xa3h\xea:\x8e\xa3\xa6\x99\xa6i\x9af\x99^X\x96%\x89b\x83\xa0\xe8:\x0e\x83\xa1\xe8z\x1e\x87\xa1\xe9\x8an\x9b\xa6\xe9\xb0\x00\x00\x00\x01\x8a\xe7:N\xe5\x9d\xcb\xf2\xcc\xffW\xd0Xfk\x9c\xecye\xb9\x81aY\xc6\r\x89\xe8zN\xed\xa1\xd2\x15\x9dgnTt\xf5\x8bm\xe0\xb6h\xeb\x9f\x17',
    b"\xd3\x01\x97D\x90\x00L\n\xdb\xa2\x00\x00\x14\x85 \x00 \x00\x00\x00 \x81\x11\x00\x7f\xff\xff\xff\xf4\xf5u\x05D\xe5\xd5p\x00\x00\x00\xfa\x1f\xfc<\x9c;\n\x93\xcc\x0f0t\xffI\xf9\xd8\x07\x7f\xff\x82\t\xdc\x1f\xdd\xe9I\xdfa\xed\xfa\xa0\xe05\x809\xef\t\x9b\x80\xbe\xe0\x0c\xc7\xf0\xdb\xe28\x1eC\xa7\r:\xc53\xb1\x89;\xa7\x00\xdf\xd3\x10\xab!\x1f\x04\x12YA.T(R\xe2\xac\xd1+\xb6\"\xc0c,\x94b\xcdB0\xa1\xa3\x1d\n2_s/\xfb46\xa3\x93_:\xad\x03\xb0\xd2;\xc0\xbfa\x81\xcfb\xb7/c\xbe/c\x91\x9fd7/\xaa\xfd\xaf\x90\x13\x8f\x88\xe5\xef\x87Q/\x85\xa2\x80\xe97\x00\xfb\xc6P\xff\xa0\x01\x04\x01!\x04k\xe0<*\x10Ix\xe0O\xa4\xb0R\x89PR\xc3p\x91\xab \x8e\xde\x90\x8e\xf5\x90\x929p\x91\xf1\x90\x81}@|\xcc@w\xea\x80x\xcb\xf0x\xbe\x00\x91\x00P\x84\xc7\xd0~\xd1\xc0\x81\x8bp}$j\n\x83\xa0\xe8:\x0e\x8d\xa3\xa8\xea:\x8e\x9af\x99\xa6i\x9aeybX\x96%\x8a\x0e\x83\xa0\xe8:\x0e\x87\xa1\xe8z\x1e\x87\xa6)\xban\x9b\xa6\xc0\x00\x00\x00\x06+\x9c\xe9;\x96w/\xcb3\xfd_Aa\x99\xaes\xb1\xe5\x96\xe6\x05\x85g\x186'\xa1\xe9;\xb6\x87HVu\x9d\xb9Q\xd3\xd6-\xb7\x82\xd9\xbd\xb6\xfb\x94v\xb3\xed\xaf\xda\xff\xb9\xcf\x80\x0e\xcf]\x98\xfbM\x83\x1f\x06\x08\rx\x1c\xa89b\x15D0Hf\x10\x96 s\xb7ck\xb6\xd8]\xb5\xdbn\x05\xa2\n\xa2\x15\x84+\\X\x88Z\xb0\xbeAF\x82\xc2\x85\xb7a\xd0\r",
    b"\xd3\x003E \x00L\n\xdb\xa2\x00 \x00\x08\x00\x00\x01\x00\x00\x00 \x00\x01\x00t\x0b\xd4Q\xcc\x13\xb4\x99\x15i\x8b\xc8\x08A\xcc\xa0E\x15\x00&(\x05\x80\xdbAb\x8d\x99k\x90_\x8aa",
    b'\xd3\x00=E0\x00L\n\xdb\xa2\x00\x00\x00\x08\x00\x00\x01\x00\x00\x00 \x00\x01\x00t\x0b\xd8\x070\x84\x00\x00\x00\xa1VW\x93\x07\x80\xd7\x88\x84\x89\x03\x04\xbd\x88\x82\xce\x9fX\r\xb4\x16(\xd9\x96\xb9\x01"\x00S\xf3Hg"\xe5',
    b"\xd3\x00\x16E\xc0\x00L\n\xdb\xa2\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0\x9b:",
    b"\xd3\x00\x16E\xd0\x00L\n\xdb\xa2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe8\x9b\x7f",
    b"\xd3\x00\xedF`\x00L\n\x00\xe2\x00 \x00\x08\x1a\x04\x1c\n\x00@ \x82\x00\x00}\xb6\xdbm\x96\x12\x94T\x14S\x15U\x94\x94R\x91z\xe4\x0f,\xff\x828\xa7\xa0b\xa2hN'\x94\xd2\xc1.-\x90M\x01\x04\xd2S\xe1\xa7Z\x1e\x94\x80R\xe4\x07\xca\xe3\xcd\x86B\xb5+\xff\xc9\xc4-\xf0\x0f\xb9\x0bp<s\x12\xd0\xbc\xc1\x10x\x15\xe7s\xd3O@\x9e,\x90\xdc\x031\xf0\x99\"\x10\xa5\xba\x00\xaa\xc0_7?O;$`(9`\x13\xb3`\x1f+\xf0,\xe00\xb7r\xf0\xb0\x1c\xae\xf4\xe5\x9e\xfeQ\xc0\x14p`F\xb7\x7f\x1a1o= \xc0@\xfd`O\xb5\xa1\r\x141#\x93\x1f!q\x80\x08Y\x98\x16\x07\x81\xe7\xb9\xee\x8a\xa2\xa4\xe9:\x8a\xa2\xa6\xd9\xb6(\x8a\xe5)JE\x91$\xb9.a\x98@\x00\x00E\xb3\xc5O\xaag\xf7\x9d\xb7|\xdc\xf6=Q\x92`\x15E\x01K\xd1\xd5\xbd=m\xd8\xb7\xfd\xd8\x8e\xf3\x1a",
    b"\xd3\x011Fp\x00L\n\x00\xe2\x00\x00\x00\x08\x1a\x04\x1c\n\x00@ \x82\x00\x00}\xb6\xdbm\x96\x12\xd4T\x14\x93\x15U\x94\x94R\x80\x00\x00\x00\x00\x02\x87\nW\xf8\x8di\x7f\xa1\x7f\xc7\x9a\x82\xdb\xef\x84@6\x05\xa3\xec\xb0\x97\xc0\xa7\xf7P\x08o\xb3\xfe\xb5\xff\x04\xac*\x0b\xe2$\xc4\x17\xf4\xdb\xf7V\xce\x07r<\x87\x9f\x02'\x1c,\xe4p\x08o\x17\xfa0\xd5\xeb\x1e$\x01\x1c\xec;\xa1r\xa3cPd\x85\x1ddeV0)\x03\x104\xf3\x1c\x84\x1aY\x02\x9b\xe3\x02\xceB\xc2\xe2\\=\x12\xf6\xbd\"\x8b\x00\xd6\x1a\x00\x84\x02\x00\xb3\x92\xc0\xeac\xfb\x12a\xfa\xf5\x08|\tG\xbc.\xf8@\x89C\x81R_\xfc\x9e\x8b\xbd*I\x01:\xd6\x81u\xb7\xbckB<\xc5=\xfc\xbc\x0b\x80W\xab\xa0X\x1e\x07\x9e\xe7\xba*\x8a\x93\xa4\xea*\x8a\x9bf\xd8\xa2+\x94\xa5)\x16D\x92\xe4\xb9\x86a\x00\x00\x01\x16\xcf\x15>\xa9\x9f\xdev\xdd\xf3s\xd8\xf5FI\x80U\x14\x05/GV\xf4\xf5\xb7b\xdf\xf7`\xea\xb1\x93\xa3[Dj\tM!\xcaC\x18\x9cA5\xd0S\x80\xa1\xfc\xf3z\x0c%hI|v\x90\xed\x1d\xde\x9b\xafC\x9a\x07\xdc\xe19\xc3xH\xb53",
    b"\xd3\x00\x16G\x00\x00L\n\xdb\xa2\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00&\x8d\xc9",
    b"\xd3\x00\x16G\x10\x00L\n\xdb\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd979",
    b"\xd3\x00\x0cL\xe0\x00\x8f\x00\x00\x00\x00\x00\x00\x00\x00\xe0?a",
    b'\xd3\x00X>\x90\x00L\n\xebB\xb0\t\xafus\xe1\xde\xdf\xc3\x02\xa9\xff|\xc6\xbf\xf5A\xb8p\xbc\xeb\xdb\xfcCte\xe0\x05\xc5\x7f$\x91\x07"\x07\x8d\xdf\xc6\x04\xc2\x14\x00\xab\xdf\xf4\xc2\x17;\xffu\xbb\xfd\xf0\xb19g\xdc\x8e\x7fDN\xf1\xe5\xf0\x18\x7f\xc7:\xde\x1f\x00\x00S P\x9f.\x1f[]\xfc\xfb\xb5\x16',
    b'\xd3\x00n>\xa0\x00L\n\xebB\xb0\t\xafus\xe1\xde\xdf\xd2\xeb\x03\x02\xa9\xff|\xc6\xbf\xf4leA\xb8p\xbc\xeb\xdb\xfd>dCte\xe0\x05\xc5\x7fC\xc4$\x91\x07"\x07\x8d\xdf\xd1\xf0\x06\x04\xc2\x14\x00\xab\xdf\xf4\xe9\xe4\xc2\x17;\xffu\xbb\xfd:\x8d\xf0\xb19g\xdc\x8e\x7fO\xa9DN\xf1\xe5\xf0\x18\x7f\xd3(\x87:\xde\x1f\x00\x00S%8\x80P\x9f.\x1f[]\xfd\x13\x14\xd8\xe65',
]


def progbar(i: int, lim: int, inc: int = 20):
    """
    Display progress bar on console.

    :param int i: iteration
    :param int lim: max iterations
    :param int inc: bar increments (20)
    """

    i = min(i, lim)
    pct = int(i * inc / lim)
    if not i % int(lim / inc):
        print(
            f"{int(pct*100/inc):02}% " + "\u2593" * pct + "\u2591" * (inc - pct),
            end="\r",
        )


def benchmark(**kwargs) -> float:
    """
    pyrtcm Performance benchmark test.

    :param int cycles: (kwarg) number of test cycles (10,000)
    :returns: benchmark as transactions/second
    :rtype: float
    :raises: UBXStreamError
    """

    cyc = int(kwargs.get("cycles", 1000))
    txnc = len(RTCMMESSAGES)
    txnt = txnc * cyc

    print(
        f"\nOperating system: {osver()}",
        f"\nPython version: {python_version()}",
        f"\npyrtcm version: {rtcmver}",
        f"\nTest cycles: {cyc:,}",
        f"\nTxn per cycle: {txnc:,}",
    )

    start = process_time_ns()
    print(f"\nBenchmark test started at {start}")
    for i in range(cyc):
        progbar(i, cyc)
        for msg in RTCMMESSAGES:
            _ = RTCMReader.parse(msg)
    end = process_time_ns()
    print(f"Benchmark test ended at {end}.")
    duration = end - start
    rate = round(txnt * 1e9 / duration, 2)

    print(
        f"\n{txnt:,} messages processed in {duration/1e9:,.3f} seconds = {rate:,.2f} txns/second.\n"
    )

    return rate


def main():
    """
    CLI Entry point.

    args as benchmark() method
    """

    benchmark(**dict(arg.split("=") for arg in argv[1:]))


if __name__ == "__main__":
    main()
