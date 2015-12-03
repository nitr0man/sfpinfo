#!/bin/sh

rmmod lp 2>/dev/null
modprobe i2c-parport type=0 || exit 1
modprobe i2c-dev
echo -n I2C bus number:
grep Parallel /sys/class/i2c-adapter/i2c-*/name | sed 's,.*/i2c-\([0-9]\+\)/.*,\1,'