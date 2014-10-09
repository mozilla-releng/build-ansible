#!/usr/bin/env python
import json
import urllib2
from collections import defaultdict

import logging
log = logging.getLogger(__name__)


DEFAULT_URL = "https://hg.mozilla.org/build/tools/raw-file/default/buildfarm/maintenance/production-masters.json"


def get_json(url):
    return json.load(urllib2.urlopen(url))


def list_all_masters(masters):
    retval = defaultdict(list)
    hostvars = defaultdict(dict)
    retval['_meta'] = {'hostvars': hostvars}
    for m in masters:
        if m['role'] == 'servo':
            continue

        if m['hostname'] not in hostvars:
            hostvars[m['hostname']] = {'masters': []}
        hostvars[m['hostname']]['masters'].append({'basedir': m['basedir']})

        if not m['enabled']:
            if m['hostname'] not in retval['disabled']:
                retval['disabled'].append(m['hostname'])
        else:
            if m['hostname'] not in retval[m['role']]:
                retval[m['role']].append(m['hostname'])
                retval['buildbot'].append(m['hostname'])
                retval[m['name']].append(m['hostname'])

    return retval


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--list", dest="action", action="store_const", const="list")
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    args = parser.parse_args()

    log.debug("Loading masters")
    masters = get_json(DEFAULT_URL)

    if args.action == "list":
        # Output a json list of all the masters
        print(json.dumps(list_all_masters(masters)))
    else:
        parser.error("--list required")

if __name__ == '__main__':
    main()
