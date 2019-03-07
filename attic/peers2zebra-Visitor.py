from xml.dom.ext.reader import PyExpat
from xml.dom import Node
from xml.dom.ext import Visitor
from xml.dom.ext.reader import Sax2
from xml.dom.ext import ReleaseNode

peersfile = "/usr/local/gitoyen-peers/peers.xml"
ix = "sfinx"

class NsVisitor(Visitor.Visitor):
    def visit(self, node):
        if node.nodeType == Node.ELEMENT_NODE:
            #if node.nodeName == "peer" and node.getAttribute ('ix') == ix:
            if node.nodeName == "peer":
                neighbor = {}
                for element in node.childNodes:
                    if element.nodeName == "name":
                        neighbor["name"] = element.childNodes[0].nodeValue
                    elif element.nodeName == "ip":
                        neighbor["ip"] = element.childNodes[0].nodeValue
                    elif element.nodeName == "as":
                        neighbor["as"] = element.childNodes[0].nodeValue
                    elif element.nodeName == "prefix-in":
                        neighbor["prefix-in"] = element.childNodes[0].nodeValue

                print "neighbor ", neighbor["ip"], \
                      " description ", neighbor["name"]
                print "neighbor ", neighbor["ip"], \
                      " remote-as ", neighbor["as"]
                print "neighbor ", neighbor["ip"], "soft-reconfiguration inbound"
                if neighbor.has_key("prefix-in"):
                    print "neighbor ", neighbor["ip"], "prefix-list ", \
                          neighbor["prefix-in"], " in"
                else:
                    print "neighbor ", neighbor["ip"], "prefix-list peer-in in"
                print "neighbor ", neighbor["ip"], "prefix-list announce-out out"
                print "neighbor ", neighbor["ip"], "filter-list 1 out"
                print "neighbor ", neighbor["ip"],  "route-map " + ix + "-in in"
                print ""
        return None

def Walk(xml_dom_object):

    visitor = NsVisitor()
    walker = Visitor.Walker(visitor, xml_dom_object)
    walker.run()

if __name__ == '__main__':
    import sys
    reader = PyExpat.Reader()
    xml_dom_object = reader.fromUri(peersfile)
    print "! Peers at " + ix
    Walk(xml_dom_object)
    reader.releaseNode(xml_dom_object)

