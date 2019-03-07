# Links

## RIS/IRR
* https://stat.ripe.net/widget/as-routing-consistency#w.resource=AS20766
* https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/routing-information-service-ris
* http://www.ris.ripe.net/cgi-bin/peerreg.cgi

## Network scripts
* http://keepingitclassless.net/2014/03/network-config-templates-jinja2/
* https://sreeninet.wordpress.com/2014/09/28/network-device-configuration-using-templates-with-jinja2-and-yaml/
* http://jedelman.com/home/ansible-for-networking/
* rtconfig
* http://irrtoolset.isc.org/
* http://www.linux.it/~md/text/rpsltool-trex.pdf
* https://github.com/job/rpsltool
* https://github.com/job/peeringmatcher
* http://irrexplorer.nlnog.net/search/20766
* https://github.com/RIPE-NCC/peertools
* http://irrd.net/
* https://github.com/daenney/napalm
* https://github.com/daenney/netmiko

* https://github.com/manuelkasper/AS-Stats
* https://abuse.io/
* https://github.com/respawner/peering-manager
* https://www.ixpdb.net/en/ixpdb/participant/20766/providers/
* https://github.com/respawner/looking-glass

# Generate

    $ ./generate_config_ripe.py|gpg2 --clearsign --no-verbose --batch --output - --textmode|EMAIL=noc_at_gitoyen.net mutt -s as20766 auto-dbm_at_ripe.net
