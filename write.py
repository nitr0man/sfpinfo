#!/usr/bin/python

import sys, smbus, time

if len(sys.argv) != 3:
    print 'Usage:', sys.argv[0], '<bus> <file>'
    sys.exit(1)

sff = open(sys.argv[2], "rb").read()

b = smbus.SMBus(int(sys.argv[1]))
k = 0
write = {}
for i in sff:
    byte = b.read_byte_data(0x50,k)
    if byte != ord(i):
	print "%s:" % hex(k), hex(byte), hex(ord(i))
	write[k] = ord(i)
    k += 1

for i, j in write.items():
    print i, j
    b.write_byte_data(0x50, i, j)
    time.sleep(0.01)

print 'Done!'