#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipaddr
import yaml
import sys
import os
import glob
from jinja2 import Environment, FileSystemLoader
from termcolor import colored

def parse_peers(peer_file):
    """parse_peers: Just a simple function for peers parsing
    :peer_file: The YAML peer file to parse
    :returns: Just a return code if the file is correctly parsed or not

    """

    peering_flat = open(peer_file).read()
    ixp = os.path.splitext(os.path.basename(peer_file))[0]

    try:
        peerings = yaml.safe_load(peering_flat)
    except:
        print colored('ERROR', 'red') + ": the peers.yaml file could not be parsed.. please check \
    your syntax"
        sys.exit(2)

    print "remarks:\nremarks:    ======== %s ========\nremarks:" % ixp.upper()
    del peerings['ID']
    for asn in peerings:
        for keyword in ['export', 'import', 'description']:
            if keyword not in peerings[asn]:
                print colored('ERROR', 'red') + ": missing %s statement in stanza %s" % (keyword, asn)
                sys.exit(2)

        acceptable_exports = ['MDW-MAIN-AS', 'NOT ANY', 'ANY']
        if not peerings[asn]['export'] in acceptable_exports:
            print colored('ERROR', 'red') + ": export must be one of the following: %s" \
                % " ".join(acceptable_exports)
            sys.exit(2)

        env = Environment(loader=FileSystemLoader('./'))
        tpl = env.get_template('templates/ripe.j2')

        print tpl.render(neighbor_as = asn, description =
                peerings[asn]['description'], export_as = peerings[asn]['export'],
                import_as = peerings[asn]['import']).encode('utf-8').strip()

sys.stdout.write(open('templates/AS204708.pre', 'r').read())

for peer_files in glob.glob('peers/*.yml'):
    parse_peers(peer_files)

sys.stdout.write(open('templates/AS204708.post', 'r').read())
