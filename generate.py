import urllib2
import json
import sys
AS = [
## http://bgp.he.net/irr/as-set/AS-GOOGLE
"AS15169",
"AS26910",
"AS36561",
"AS6432",
"AS36492",
"AS43515",
"AS11344",
"AS40873",
"AS22577",
"AS36040",
"AS13949",
"AS19425",
"AS1424",
"AS1406",
"AS22244",
"AS55023",
## Dropbox
"AS19679",
]

IPs = [
## "1.2.3.4/32"
"2.120.0.0/13",
]

Blacklists = set([
"8.8.8.0/24",
"8.8.4.0/24"
])

i = 0
prefixes = list(IPs)
for asn in AS:
    i += 1
    print >> sys.stderr, "Loading", asn, "%d / %d" % (i, len(AS)) 
    data = json.loads(urllib2.urlopen("https://stat.ripe.net/data/announced-prefixes/data.json?resource=" + asn).read())
    data = data['data']['prefixes']
    for item in data:
        p = item['prefix']
        if '::/' in p:
            ##Skip IPV6
            continue
        prefixes.append(item['prefix'])

prefixes.sort()
#print "#!/bin/sh"
for prefix in prefixes:
    if not prefix in Blacklists:
        print "route add -net %s gw 10.20.10.2 dev br-lan" % prefix
