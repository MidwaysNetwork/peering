#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipaddr
import yaml
import sys
import glob
from termcolor import colored

def parse_peers(peer_file):
    """parse_peers: Just a simple function for peers parsing
    :peer_file: The YAML peer file to parse
    :returns: Just a return code if the file is correctly parsed or not

    """

    peering_flat = open(peer_file).read()

    try:
        peerings = yaml.safe_load(peering_flat)
    except:
        print colored('ERROR', 'red') + ": the peers.yaml file could not be parsed... please check \
    your syntax"
        sys.exit(2)

    # IXPs Gitoyen is connected to

    connected_ixps = {
        "amsix": [ipaddr.IPNetwork('80.249.210.195/21'),
                ipaddr.IPNetwork('2001:7f8:1::a502:766:1/64')],
        "franceix": [ipaddr.IPNetwork('37.49.236.190/23'),
                ipaddr.IPNetwork('2001:7f8:54::190/64')],
        "equinix": [ipaddr.IPNetwork('195.42.145.64/23'),
                ipaddr.IPNetwork('2001:7f8:43::2:766:1/64')],
        "sfinx": [ipaddr.IPNetwork('194.68.129.186/24'),
                ipaddr.IPNetwork('2001:7f8:4e:2::186/64')]}

    for asn in peerings:
        for keyword in ['export', 'import', 'description', 'peerings']:
            if keyword not in peerings[asn]:
                print colored('ERROR', 'red') + ": missing %s statement in stanza %s" % (keyword, asn)
                sys.exit(2)

        for peer in peerings[asn]['peerings']:
            try:
                peer_ip = ipaddr.IPAddress(peer)
            except ValueError:
                print colored('ERROR', 'red') + ": %s in %s is not a valid IP" % (peer, asn)
                sys.exit(2)

            # search if we can reach the peer
            found = False
            for ixp in connected_ixps:
                for subnet in connected_ixps[ixp]:
                    if ipaddr.IPAddress(peer) in subnet:
                        print colored('OK', 'green') + ": found %s (%s) in %s" % (peer, asn, ixp)
                        found = True
            if not found:
                print colored('ERROR', 'red') + ": AS 20766 cannot reach %s through %s, either a typo \
    or we are not connected to the same internet exchange" \
                    % (peer, " ".join(connected_ixps))
                sys.exit(2)

        acceptable_exports = ['AS-GITOYEN', 'NOT ANY', 'ANY']
        if not peerings[asn]['export'] in acceptable_exports:
            print colored('ERROR', 'red') + ": export must be one of the following: %s" \
                % " ".join(acceptable_exports)
            sys.exit(2)

    print colored('HOORAY', 'yellow') + ": Ready for production!!!"

for peer_files in glob.glob('peers/*.yml'):
    parse_peers(peer_files)
