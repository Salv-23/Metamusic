"""
Author : Salvador <Salvador@fedora>
Date   : 2022-10-05
Purpose: Command-line interface for metamusic
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Retrieve arguments to work with the cli",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-a",
        "--artist",
        help="An artist to search for",
        metavar="str",
        type=str,
        required=True,
    )

    return parser.parse_args()
