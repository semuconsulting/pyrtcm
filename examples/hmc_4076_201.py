"""
hmc_4076_201.py

Produces multi-dimensional array of harmonic coefficients from
binary NTRIP log containing 4076_201 message.

Dimensions of hmc array are [layer][coefficent][value].

Usage:

python3 hmc_4076_201.py "inputfile"

"""

from sys import argv

from pyrtcm import RTCMReader

COEFFS = {
    0: ("IDF039", "Cosine"),
    1: ("IDF040", "Sine"),
}


def main(fname):
    """
    Main routine.

    :param str fname: fully qualified path to input file
    """

    with open(fname, "rb") as infile:
        rtr = RTCMReader(infile)
        for _, parsed in rtr:
            if parsed.identity == "4076_201":
                layers = parsed.IDF035 + 1  # number of ionospheric layers
                hmc = []
                # for each ionospheric layer
                for lyr in range(layers):
                    lyrheight = getattr(parsed, f"IDF036_{lyr+1:02d}")
                    hmc.append(lyr)
                    hmc[lyr] = []
                    # for each coefficient (cosine & sine)
                    for c, coeff in enumerate(COEFFS.values()):
                        hmc[lyr].append(c)
                        hmc[lyr][c] = []
                        i = 0
                        eof = False
                        # for each coefficient value
                        while not eof:
                            try:
                                hmc[lyr][c].append(
                                    getattr(
                                        parsed,
                                        f"{coeff[0]}_{lyr+1:02d}_{i+1:02d}",
                                    )
                                )
                                i += 1
                            except AttributeError:
                                eof = True

                        print(
                            f"Layer {lyr+1} {lyrheight} km -",
                            f"Harmonic Coefficients {coeff[1]} ({len(hmc[lyr][c])})",
                        )
                        for i, hc in enumerate(hmc[lyr][c]):
                            print(f"{i+1}: {hc}")


if __name__ == "__main__":

    main(argv[1])
