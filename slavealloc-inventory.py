#!/usr/bin/env python
import requests
import json

# This needs auth...
# API_ROOT = "https://secure.pub.build.mozilla.org/slavealloc/api/"j
# This doesn't; but requires VPN
API_ROOT = "http://slavealloc.build.mozilla.org/api"


def get_pools():
    url = "{}/pools".format(API_ROOT)
    resp = requests.get(url)
    resp.raise_for_status()
    return dict((p['poolid'], p['name']) for p in resp.json())


def get_slaves():
    url = "{}/slaves".format(API_ROOT)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def list_hosts():
    hosts = {}
    hosts['_meta'] = {'hostvars': {}}
    slaves = get_slaves()
    pools = get_pools()
    for slave in slaves:
        # TODO: Probably want to put these in a different bucket so we can work
        # on them if necessary
        if not slave['enabled']:
            continue

        pool_name = pools[slave['poolid']]
        slave_name = slave['name']
        distro_name = slave['distro']
        fqdn = "{}.build.mozilla.org".format(slave_name)
        hosts.setdefault(pool_name, []).append(fqdn)
        hosts.setdefault(distro_name, []).append(fqdn)
        hosts['_meta']['hostvars'][fqdn] = {}
    return hosts


def main():
    import sys
    if '--list' in sys.argv:
        result = list_hosts()
        print json.dumps(result, indent=2)


if __name__ == '__main__':
    main()
