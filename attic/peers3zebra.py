import sys
import re
#from xml.dom.ext.reader import Sax
import xml.sax
from xml.dom import Node

peersfile = "/usr/local/gitoyen-peers/peers.xml"
default_max_prefixes = 1000

def visit(node):
    if node.nodeType == Node.ELEMENT_NODE:
        if node.nodeName == "peer" and node.getAttribute ('ix') == ix:
            neighbor = {}
	    neighbor["map-in"] = []
	    neighbor["map-out"] = []
            for element in node.childNodes:
                if element.nodeName == "name":
                    neighbor["name"] = element.childNodes[0].nodeValue
                elif element.nodeName == "ip":
                    neighbor["ip"] = element.childNodes[0].nodeValue
                elif element.nodeName == "as":
                    neighbor["as"] = element.childNodes[0].nodeValue
                elif element.nodeName == "prefix-in":
                    neighbor["prefix-in"] = element.childNodes[0].nodeValue
                elif element.nodeName == "prefix-out":
                    neighbor["prefix-out"] = element.childNodes[0].nodeValue
                elif element.nodeName == "map-in":
                    neighbor["map-in"] += [ element.childNodes[0].nodeValue ]
                elif element.nodeName == "map-out":
                    neighbor["map-out"] += [ element.childNodes[0].nodeValue ]
                elif element.nodeName == "max-prefixes":
                    neighbor["max-prefixes"] = element.childNodes[0].nodeValue

            if re.search (":", neighbor["ip"]):
                # IPv6
                neighbor_tag = "ipv6 bgp neighbor "
                peer_in = "peer-ip6-in"
                announce_out = "announce-ip6-out"
            else:
                neighbor_tag = "neighbor "
                peer_in = "pfx-all-but-gitoyen"
                peer_out = "pfx-all"
                announce_out = "announce-out"
            print neighbor_tag, neighbor["ip"], \
                  " remote-as ", neighbor["as"]
            print neighbor_tag, neighbor["ip"], \
                  " description ", neighbor["name"]
            print neighbor_tag, neighbor["ip"], "soft-reconfiguration inbound"
            if neighbor.has_key("prefix-in"):
                print neighbor_tag, neighbor["ip"], "prefix-list ", \
                      neighbor["prefix-in"], " in"
            else:
                print neighbor_tag, neighbor["ip"], "prefix-list ", peer_in, " in"
            if neighbor.has_key("prefix-out"):
                print neighbor_tag, neighbor["ip"], "prefix-list ", \
                      neighbor["prefix-out"], " out"
            else:
                print neighbor_tag, neighbor["ip"], "prefix-list ", \
		      peer_out, " out"
            if len(neighbor["map-in"]) != 0:
                for map in neighbor["map-in"]:
		    print neighbor_tag, neighbor["ip"], "route-map ", map, " in"
            else:
                print neighbor_tag, neighbor["ip"],  "route-map " + ix + "-in in"
            if len(neighbor["map-out"]) != 0:
                for map in neighbor["map-out"]:
                    print neighbor_tag, neighbor["ip"], "route-map ", map, " out"
            else:
                print neighbor_tag, neighbor["ip"],  "route-map " + ix + "-out out"
            if not re.search (":", neighbor["ip"]): # max-prefixes not supported for IPv6?
                if not neighbor.has_key("max-prefixes"):
                    max_prefixes = default_max_prefixes
                else:
                    max_prefixes = neighbor["max-prefixes"]
                print neighbor_tag, neighbor["ip"], "maximum-prefix ", max_prefixes
            print ""
    return None

if __name__ == '__main__':
    tree = Sax.FromXmlFile(peersfile)
    try:
        ix = sys.argv[1]
    except IndexError:
        sys.stderr.write ("Usage: " + sys.argv[0] + " ix\n")
        sys.exit(1)
    print "! Peers at " + ix
    print "! Do NOT edit by hand. Edit ",
    print str(peersfile) + " on machoke instead."
    print ""
    for peer in tree.documentElement.childNodes:
        visit(peer)


