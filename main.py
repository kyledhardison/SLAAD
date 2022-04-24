#!/usr/bin/env python3

import argparse
import sys
from lib.Parser import Parser, Verbosity

def main():

    parser = argparse.ArgumentParser("Disassemble a Lua 5.4.4 bytecode file")
    
    parser.add_argument("infile", metavar="<file>", 
                        help="The file to be disassembled")
    parser.add_argument("-v", "--verbose", dest="info",
                        action="store_true",
                        help="Verbose (print significant data member parsed)")
    parser.add_argument("-vv", "--very-verbose", dest="verbose",
                        action="store_true",
                        help="Very Verbose (print all data member parsed)")

    args = parser.parse_args()
    verbosity = Verbosity.OFF
    if args.info:
        verbosity = Verbosity.INFO
    elif args.verbose:
        verbosity = Verbosity.VERBOSE
    p = Parser(args.infile, verbosity)
    p.parse()


if __name__ == "__main__":
    main()

