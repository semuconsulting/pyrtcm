"""
hmc_4076_201.py

Produces multi-dimensional array of harmonic coefficients from
binary NTRIP log containing 4076_201 message.

Dimensions of hmc array are {layer:{coefficent:[values]}}.

Usage:

python3 hmc_4076_201.py infile="../tests/pygpsdata-NTRIP-4076.log"

"""

from sys import argv

from pyrtcm import RTCMReader, parse_4076_201


def main(**kwargs):
    """
    Main routine.

    :param str fname: fully qualified path to input file
    """

    infile = kwargs.get("infile", "../tests/pygpsdata-NTRIP-4076.log")

    with open(infile, "rb") as infile:
        rtr = RTCMReader(infile)
        for _, parsed in rtr:
            coeffs = parse_4076_201(parsed)
            if coeffs is not None:
                print(coeffs)


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
