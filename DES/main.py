from Des import DES as Des

data = "Diamante"
key = "Asegurar"
des = Des()
rip = des.ipermutation(data)
print "IP: ", rip

re = des.expand(rip)
print "E: ", re

rpc1 = des.expand(data)
print "PC1: ", rpc1
