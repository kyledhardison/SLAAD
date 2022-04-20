#!/usr/bin/env python3

import sys
from lib.Parser import Parser

def main():
    if len(sys.argv) != 2:
        # TODO Usage
        pass 
    
    p = Parser(sys.argv[1])
    p.parse()


if __name__ == "__main__":
    main()

