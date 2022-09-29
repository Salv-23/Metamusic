#!/usr/bin/env python3
"""
Author : Salvador <Salvador@fedora>
Date   : 2022-09-27
Purpose: New program
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
            description="New program",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
            "positional",
            metavar="str",
            help="A positional argument",
            )

    parser.add_argument(
            "-a",
            "--arg",
            help="A named string argument",
            metavar="str",
            type=str,
            default="",
            )

    parser.add_argument(
            "-i",
            "--int",
            help="A named integer argument",
            metavar="int",
            type=int,
            default=0,
            )

    parser.add_argument(
            "-f",
            "--file",
            help="A readable file",
            metavar="FILE",
            type=argparse.FileType("rt"),
            default=None,
            )

    parser.add_argument(
            "-o",
            "--on",
            help="A boolean flag",
            action="store_true",
            )

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Main function for program"""

    args = get_args()
    str_arg = args.arg
    int_arg = args.int
    file_arg = args.file
    flag_arg = args.on
    pos_arg = args.positional


# --------------------------------------------------
if __name__ == '__main__':
    main()
