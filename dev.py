#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from novaclient.client import Client
import json
 
nova = Client(2, 'admin', 'pass', 'admin', "http://localhost:5000/v2.0")
 
servers = nova.servers.list(detailed=True, search_opts={'all_tenants':1})
 
# Get all instances flavors by compute
_infos={}
for server in servers:
    compute = server._info.get('OS-EXT-SRV-ATTR:host')
    instance = server._info.get('OS-EXT-SRV-ATTR:instance_name')
    flavor = nova.flavors.get(server.flavor.get('id'))
 
    if not compute in _infos:
        _infos[compute] = []
 
    _infos[compute].append((instance, flavor))
 
# Print some stats
for compute, content in sorted(_infos.iteritems(), key=(lambda(x,y): x)):
    print '--- %s' % compute
    used_ram = 0
    for instance, flavor in content:
        used_ram += flavor.ram/1024
    print 'Used ram %sG' % used_ram
