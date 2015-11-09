#!/usr/bin/env python
import boto.ec2
import json
import random


def list_hosts():
    retval = {
        '_meta': {'hostvars': {}},
    }
    for r in 'us-east-1', 'us-west-2':
        conn = boto.ec2.connect_to_region(r)
        instances = conn.get_only_instances(filters={'instance-state-name': 'running'})

        for i in instances:
            moz_type = i.tags.get('moz-type')
            name = i.tags.get('Name')
            if not moz_type:
                moz_type = 'unknown'
            retval.setdefault(moz_type, []).append(i.private_ip_address)
            retval.setdefault(r, []).append(i.private_ip_address)
            retval.setdefault(name, []).append(i.private_ip_address)
            retval['_meta']['hostvars'][i.private_ip_address] = {}
            #retval['_meta']['hostvars'][name] = {}

        for k in retval:
            if k == '_meta':
                continue
            random.shuffle(retval[k])

    return retval


def main():
    import sys, os, time
    cache = "ec2-inventory-cache.json"

    if "--list" in sys.argv:
        if os.path.exists(cache) and os.path.getmtime(cache) + 600 > time.time():
            print open(cache).read()
        else:
            result = list_hosts()
            open(cache, 'w').write(json.dumps(result))
            print json.dumps(result)

if __name__ == '__main__':
    main()
