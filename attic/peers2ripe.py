from xml.dom.ext.reader import Sax
from xml.dom import Node

peersfile = "/usr/local/gitoyen-peers/peers.xml"
neighbors = {}

def visit(node):
    if node.nodeType == Node.ELEMENT_NODE:
        if node.nodeName == "peer":
            neighbor = {}
            for element in node.childNodes:
                if element.nodeName == "name":
                    neighbor["name"] = element.childNodes[0].nodeValue
                elif element.nodeName == "as":
                    neighbor["as"] = element.childNodes[0].nodeValue
                elif element.nodeName == "as-set":
                    neighbor["as-set"] = element.childNodes[0].nodeValue
        if (not neighbors.has_key(neighbor["name"])):
            neighbors[neighbor["name"]] = neighbor
    return None

if __name__ == '__main__':
    tree = Sax.FromXmlFile(peersfile)    
    for peer in tree.documentElement.childNodes:
        visit(peer)
    for name in neighbors.keys():
        peer = neighbors[name]
        print "import:    from AS" + str(peer["as"])
        print "     action pref=100;"
        if (peer.has_key("as-set")):
            print "     accept AS-" + str(peer["as-set"])
        else:
            print "     accept AS" + str(peer["as"])
        
