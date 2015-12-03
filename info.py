#!/usr/bin/python
import sys, struct


mod_id = {
	  '\x00': 'Unknown',
	  '\x01': 'GBIC',
	  '\x02': 'SFF',
	  '\x03': 'SFP/SFP+',
	 }

connector = {
	     '\x00': 'Unknown connector',
	     '\x01': 'SC',
	     '\x02': 'FC Type 1',
	     '\x03': 'FC type 2',
	     '\x04': 'BNC/TNC',
	     '\x07': 'LC',
	    }

compliance = {

	      1 << 0: '1X copper passive',
	      1 << 1: '1X copper active',
	      1 << 2: '1X LX',
	      1 << 3: '1X SX',
	      1 << 4: '10G Base-SR',
	      1 << 5: '10G Base-LR',
	      1 << 6: '10G Base-LRM',
	      1 << 7: '10G Base-ER',
	      1 << 8: 'OC-3 short reach',
	      1 << 9: 'OC-3 SM, intermediate reach',
	      1 << 10: 'OC-3 SM, long reach',
	      1 << 12: 'OC-12 short reach',
	      1 << 13: 'OC-12 SM, intermediate reach',
	      1 << 14: 'OC-12 SM, long reach',
	      1 << 16: 'OC-48 short reach',
	      1 << 17: 'OC-48 intermediate reach',
	      1 << 18: 'OC-48 long reach',
	      1 << 19: 'SONET reach bit 1',
	      1 << 20: 'SONET reach bit 2',
	      1 << 21: 'OC-192 short reach',
	      1 << 22: 'ESCON SMF, 1310nm laser',
	      1 << 23: 'ESCON MMF, 1310nm LED',
	      1 << 24: '1000Base-SX',
	      1 << 25: '1000Base-LX',
	      1 << 26: '1000Base-CX',
	      1 << 27: '1000Base-T',
	      1 << 28: '100Base-LX/LX10',
	      1 << 29: '100Base-FX',
	      1 << 30: 'Base-BX/10',
	      1 << 31: 'Base-PX',
	      1 << 32: 'FC: electrical inter-enclosure (EL)',
	      1 << 33: 'FC: longwave laser (LC)',
	      1 << 34: 'FC: shortwave laser, linear Rx (SA)',
	      1 << 35: 'FC: medium distance (M)',
	      1 << 36: 'FC: long distance (L)',
	      1 << 37: 'FC: intermediate distance (I)',
	      1 << 38: 'FC: short distance (S)',
	      1 << 39: 'FC: very long distance (V)',
	      1 << 42: 'SFP+ Passive cable',
	      1 << 43: 'SFP+ Active cable',
	      1 << 44: 'FC: Longwave laser (LL)',
	      1 << 45: 'FC: Shortwave laser with OFC (SL)',
	      1 << 46: 'FC: Shortwave laser w/o OFC (SN)',
	      1 << 47: 'FC: Electrical intra-inclosure (EL)',
	      1 << 48: 'FC media: Single mode (SM)',
	      1 << 50: 'FC media: Multimode, 50um (M5, M5E)',
	      1 << 51: 'FC media: Multimode, 62.5um (M6)',
	      1 << 52: 'FC media: Video coax (TV)',
	      1 << 53: 'FC media: Miniature coax (MI)',
	      1 << 54: 'FC media: Twisted pair (TP)',
	      1 << 55: 'FC media: Twin axial pair (TW))',
	      1 << 56: 'FC speed: 100MB/sec',
	      1 << 58: 'FC speed: 200MB/sec',
	      1 << 60: 'FC speed: 400MB/sec',
	      1 << 61: 'FC speed: 1600MB/sec',
	      1 << 62: 'FC speed: 800MB/sec',
	      1 << 63: 'FC speed: 1200MB/sec',
	     }

encoding = {
	    '\x00': 'Unspecified',
	    '\x01': '8B/10B',
	    '\x02': '4B/5B',
	    '\x03': 'NRZ',
	    '\x04': 'Manchester',
	    '\x05': 'SONET Scrambled',
	    '\x06': '64B/66B',
	   }

rate_id = {
	    '\x00': 'Unspecified',
	    '\x01': 'SFF-8079 (4/2/1G Rate_Select & AS0/AS1)',
	    '\x02': 'SFF-8431 (8/4/2G Rx Rate_Select only)',
	    '\x04': 'SFF-8431 (8/4/2G Tx Rate_Select only)',
	    '\x06': 'SFF-8431 (8/4/2G Independent Rx & Tx Rate_select)',
	    '\x08': 'FC-PI-5 (16/8/4G Rx Rate_select only) High=16G only, Low=8G/4G',
	    '\x0A': 'FC-PI-5 (16/8/4G Independent Rx, Tx Rate_select) High=16G only, Low=8G/4G',
	  }

options = {
	    1 << 0: 'Linear Receiver Output Implemented',
	    1 << 1: 'Power level 2 required',
	    1 << 2: 'Cooled laser transmitter',
	    1 << 9: 'Rx_LOS',
	    1 << 10: 'Signal detect (inverted Rx_LOS)',
	    1 << 11: 'TX_FAULT',
	    1 << 12: 'TX_DISABLE',
	    1 << 13: 'RATE_SELECT',
	  }

DDM = {
	1 << 2: 'Address change required',
	1 << 3: 'Average input power',
	1 << 4: 'Internally calibrated',
	1 << 5: 'Externally calibrated',
	1 << 6: 'DDM present',
      }

enh_opts = {
	    1 << 7: 'Optional Alarm/warning flags implemented',
	    1 << 6: 'Soft TX_DISABLE control and monitoring implemented',
	    1 << 5: 'Soft TX_FAULT monitoring implemented',
	    1 << 4: 'Soft RX_LOS monitoring implemented',
	    1 << 3: 'Soft RATE_SELECT control and monitoring implemented',
	    1 << 2: 'Application Select control implemented per SFF-8079',
	    1 << 1: 'Soft Rate Select control implemented per SFF-8431',
	   }

sff8472 = {
	    '\x00': 'No DDM',
	    '\x01': 'Rev 9.3 of SFF-8472.',
	    '\x02': 'Rev 9.5 of SFF-8472.',
	    '\x03': 'Rev 10.2 of SFF-8472.',
	    '\x04': 'Rev 10.4 of SFF-8472.',
	    '\x05': 'Rev 11.0 of SFF-8472.',
	    ' '   : 'WRONG!',
	  }

if len(sys.argv) == 0:
    print 'Usage:', sys.argv[0], ' <file>'
    sys.exit(1)

sff = open(sys.argv[1], "rb").read()

print 'Module:', mod_id[sff[0]], connector[sff[2]]
comp = struct.unpack('<Q',sff[3:11])[0]
print 'Compliance:', hex(comp), 'values:'
for i, s in compliance.items():
    if comp & i:
	print '*', s
print 'Encoding:', encoding[sff[11]]
print 'Baud rate, x100MBd:', ord(sff[12])
print 'Rate identifier:', rate_id[sff[13]]
print 'Length, km:', ord(sff[14])
print 'Length, x100m:', ord(sff[15])
print 'Length 50um OM2, x10m:', ord(sff[16])
print 'Length 62.5um OM1, x10m:', ord(sff[17])
print 'Length (Active cable/copper), m:', ord(sff[18])
print 'Length 50um OM2, x10m:', ord(sff[19])
print 'Vendor name:', sff[20:36]
print 'Vendor OUI:', hex(ord(sff[37])), hex(ord(sff[38])), hex(ord(sff[39]))
print 'Vendor PN:', sff[40:56]
print 'Vendor rev:', sff[56:60]
crc = 0
for i in sff[0:63]:
    crc += ord(i)
    crc &= 255
if crc == ord(sff[63]):
    print 'Base CRC correct'
else:
    print 'Base CRC incorrect (expected %s, got %s)' % (hex(crc), hex(ord(sff[63])))

opts = struct.unpack('<H',sff[64:66])[0]
print 'options:', hex(opts), 'values:'
for i, s in options.items():
    if opts & i:
	print '*', s

print 'Baud rate max: +%d%%' % ord(sff[66])
print 'Baud rate min: -%d%%' % ord(sff[67])
print 'Vendor s/n:', sff[68:84]
print 'Vendor date code: 20%s-%s-%s' % (sff[84:86], sff[86:88], sff[88:90])

ddm_opts = ord(sff[92])
print 'DDM options:', hex(ddm_opts), 'values:'
for i, s in DDM.items():
    if ddm_opts & i:
	print '*', s

eopts = ord(sff[92])
print 'Enhanced options:', hex(eopts), 'values:'
for i, s in enh_opts.items():
    if eopts & i:
	print '*', s

print 'SFF8472 compatibility:', sff8472[sff[94]]

ecrc = 0
for i in sff[64:95]:
    ecrc += ord(i)
    ecrc &= 255
if ecrc == ord(sff[95]):
    print 'Ext CRC correct'
else:
    print 'Ext CRC incorrect (expected %s, got %s)' % (hex(crc), hex(ord(sff[63])))
