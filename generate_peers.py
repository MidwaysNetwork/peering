import requests
import yaml
import ping

GITOYEN_ASN = 0
PEER_ASN_LIST = []

gitoyen_peering_factory = []
ses = requests.session()
peer = dict()

# Load config
try:
    config = yaml.load(open('config/settings.yml'))
    GITOYEN_ASN = config['ASN']
    PEER_ASN_LIST = config['PEERS']
except:
    print("Failed to load config exiting..")
    exit(1)

# List Gitoyen Factory with IPv6 avaidable
factory_request = ses.get("https://peeringdb.com//api/netixlan?asn=" + str(GITOYEN_ASN))
for factory in factory_request.json()['data']:
    if factory['ipaddr6'] is not None:
        gitoyen_peering_factory.append(factory)

for factory in gitoyen_peering_factory:
    name = (str(factory['name'])).split(' ')[0].lower()
    print("Generation en cours pour " + name)
    peer[name] = dict()
    for asn in PEER_ASN_LIST:
        info_request = ses.get(
            "https://peeringdb.com/api/netixlan?asn=" + str(asn) + "&ix_id=" + str(factory['ix_id']))
        result = info_request.json()['data']
        if len(result) > 0:
            name_request = ses.get('https://peeringdb.com/api/net?asn=' + str(asn)).json()
            peer[name][asn] = dict()
            peer[name][asn]['description'] = name_request['data'][0]['name']
            if name_request['data'][0]['irr_as_set'] is not None and len(name_request['data'][0]['irr_as_set']) > 0:
                peer[name][asn]['import'] = name_request['data'][0]['irr_as_set']
            else:
                peer[name][asn]['import'] = "AS" + str(asn)
            peer[name][asn]['export'] = "MDW-MAIN-AS"
            peer[name][asn]['peerings'] = []
            if name_request['data'][0]['info_prefixes4'] is not None:
                peer[name][asn]['limit_ipv4'] = int(name_request['data'][0]['info_prefixes4'])
            if name_request['data'][0]['info_prefixes6'] is not None:
                peer[name][asn]['limit_ipv6'] = int(name_request['data'][0]['info_prefixes6'])
            delete = True
            for routeur in result:
                if routeur['ipaddr4'] is not None:
                    peer[name][asn]['peerings'].append(routeur['ipaddr4'])
		    latency = ping.quiet_ping(routeur['ipaddr4'])[1]
                    if latency is None:
                        latency = 0
		    peer[name][asn]['med'] = int(200 + latency)
		    peer[name][asn]['local_pref'] = int(220 - latency)
                    print(
                        "Generating configuration at " + name + " for the router " + str(routeur['ipaddr4']) + " of the AS " + str(
                            asn) + " " + peer[name][asn]['description']+ " " + str(latency) + " med " + str(peer[name][asn]['med']) + " pref "+ str(peer[name][asn]['local_pref']))
                if routeur['ipaddr6'] is not None:
                    peer[name][asn]['peerings'].append(routeur['ipaddr6'])
                    print(
                        "Generating configuration at " + name + " for the router " + str(routeur['ipaddr6']) + " of the AS " + str(
                            asn) + " " + peer[name][asn]['description'])
                delete = False
            if delete:
                peer[name].pop(asn, None)

for gix in peer:
    with open("peers/" + gix + '.yml', 'w+') as outfile:
        yaml.safe_dump(peer[gix], outfile, default_flow_style=False)
        outfile.close()
