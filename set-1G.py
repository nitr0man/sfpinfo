#!/usr/bin/python

import sys, smbus, time
import os.path
if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '<bus>'
    sys.exit(1)

b = smbus.SMBus(int(sys.argv[1]))
sff = r''
for i in range(256):
    sff += chr(b.read_byte_data(0x50, i))

speed = ''
if ord(sff[12]) < 3:
    speed = '100M'
elif ord(sff[12]) > 9 and ord(sff[12]) < 14:
    speed = '1G'
else:
    speed = str(ord(sff[12])/10.0) + 'G'

name = sff[20:36].strip() + '_' + sff[40:56].strip() + '_' + sff[68:84].strip() + '_' + speed + '.bin'
i = 1
while os.path.isfile(name):
    name = sff[20:36].strip() + '_' + sff[40:56].strip() + '_'  + sff[68:84].strip() + '_' + speed + '_' + str(i) + '.bin'
    i += 1

print name

open(name, "wb").write(sff)

sff = sff[0:7] + '\x12\x00\x01\x01\x01\x0d' + sff[13:]

crc = 0
for i in sff[0:63]:
    crc += ord(i)
    crc &= 255
sff = sff[0:63] + chr(crc) + sff[64:]

k = 0
write = {}
for i in sff:
    byte = b.read_byte_data(0x50,k)
    if byte != ord(i):
	print "%s:" % hex(k), hex(byte), hex(ord(i))
	write[k] = ord(i)
    k += 1

for i, j in write.items():
    print hex(i), hex(j)
    b.write_byte_data(0x50, i, j)
    time.sleep(0.01)

print 'Done!'