"""
hmc_4076_201.py

Produces multi-dimensional array of harmonic coefficients from
binary NTRIP log containing 4076_201 message.

Dimensions of hmc array are {layer:{coefficent:[values]}}.

Usage:

python3 hmc_4076_201.py "inputfile"

"""

from sys import argv

from pyrtcm import RTCMReader, RTCMMessage

COEFFS = {
    0: ("IDF039", "Cosine"),
    1: ("IDF040", "Sine"),
}


def process_message(parsed: RTCMMessage):
    """
    Process individual 4076_201 message.

    :param RTCMMessage parsed: parsed 4076_201 message
    """

    layers = parsed.IDF035 + 1  # number of ionospheric layers
    hmc = {}
    # for each ionospheric layer
    for lyr in range(layers):
        lyrheight = getattr(parsed, f"IDF036_{lyr+1:02d}")
        hmc[lyr] = {}
        # for each coefficient (cosine & sine)
        for field, coeff in COEFFS.values():
            hmc[lyr][coeff] = []
            i = 0
            eof = False
            # for each coefficient value
            while not eof:
                try:
                    hmc[lyr][coeff].append(
                        getattr(parsed, f"{field}_{lyr+1:02d}_{i+1:02d}")
                    )
                    i += 1
                except AttributeError:
                    eof = True

            print(
                f"\nLayer {lyr+1} {lyrheight} km -",
                f"Harmonic Coefficients {coeff} ({len(hmc[lyr][coeff])}):",
            )
            for i, hc in enumerate(hmc[lyr][coeff]):
                print(f"{i+1:03d}: {hc}")

    print("\nEntire contents of hmc array:")
    print(hmc)


def main(fname: str):
    """
    Main routine.

    :param str fname: fully qualified path to input file
    """

    with open(fname, "rb") as infile:
        rtr = RTCMReader(infile)
        for _, parsed in rtr:
            if parsed.identity == "4076_201":
                process_message(parsed)


if __name__ == "__main__":

    main(argv[1])
