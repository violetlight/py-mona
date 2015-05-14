#!/usr/bin/env python

import mona
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "ERROR: Provide a path to an image as the only argument."
        sys.exit()

    controller = mona.Control(sys.argv[1])
    controller.loop()
