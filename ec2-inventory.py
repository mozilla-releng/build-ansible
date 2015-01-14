#!/usr/bin/env python
import boto.ec2
import json


def list_hosts():
    retval = {
        '_meta': {'hostvars': {}},
    }
    for r in 'us-east-1', 'us-west-2':
        conn = boto.ec2.connect_to_region(r)
        instances = conn.get_only_instances(filters={'instance-state-name': 'running'})

        for i in instances:
            moz_type = i.tags.get('moz-type')
            if not moz_type:
                moz_type = 'unknown'
            retval.setdefault(moz_type, []).append(i.private_ip_address)
            retval.setdefault(r, []).append(i.private_ip_address)
            retval['_meta']['hostvars'][i.private_ip_address] = {}

    return retval


def main():
    import sys
    if "--list" in sys.argv:
        print json.dumps(list_hosts())

if __name__ == '__main__':
    main()
