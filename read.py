#!/usr/bin/python

import sys, smbus, time

if len(sys.argv) != 3:
    print 'Usage:', sys.argv[0], '<bus> <file>'
    sys.exit(1)


b = smbus.SMBus(int(sys.argv[1]))
sff = r''
for i in range(256):
    sff += chr(b.read_byte_data(0x50, i))

open(sys.argv[2], "wb").write(sff)

print 'Done!'