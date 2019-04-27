from pyblnet import BLNETDirect

ip='10.0.0.170'
blnet=BLNETDirect(ip)
print(blnet.get_latest())
