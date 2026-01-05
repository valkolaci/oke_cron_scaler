#!/usr/bin/env python

import os
import json
import oci

from cfg import Config
import oke

# Read and parse configuration
c = Config.read_config()
print(c.dump())

nodepool_id = os.environ['NODEPOOL_ID'] if 'NODEPOOL_ID' in os.environ else None
default_size = os.environ['DEFAULT_SIZE'] if 'DEFAULT_SIZE' in os.environ else None

if nodepool_id is None or nodepool_id == '':
  raise Exception("Missing NODEPOOL_ID environment parameter")
if default_size is None or default_size == '':
  raise Exception("Missing DEFAULT_SIZE environment parameter")
try:
  default_size = int(default_size)
except (ValueError) as ex:
  raise Exception("Invalid non integer DEFAULT_SIZE environment parameter")

size = default_size
print("Parse arguments: %s: %d" % (nodepool_id, size))

config = oci.config.from_file()
oci.config.validate_config(config)
compartments = oke.list_compartments(config=config)  # function defined below
for compartment in compartments["compartments"]:
  print("%s: %s" % (compartment["path"], compartment["id"]))

found_compartment = None
for compartment in compartments["compartments"]:
  if compartment["path"] == "enap/cmp-tst":
    found_compartment = compartment
    break

clusters = oke.list_oke_clusters(compartment["id"], config=config)
for cluster in clusters["clusters"]:
  print("%s: %s" % (cluster["name"], cluster["id"]))

for cluster in clusters["clusters"]:
  nodepools = oke.list_oke_node_pools(compartment["id"], cluster["id"], config=config)
  for nodepool in nodepools["nodepools"]:
    print("%s: %s %d" % (nodepool["name"], nodepool["id"], nodepool["size"]))


n = oke.get_oke_node_pool(nodepool_id, config=config)
nodepool = n["nodepool"]
print("%s: %s %d" % (nodepool["name"], nodepool["id"], nodepool["size"]))
if nodepool["size"] != size:
  n = oke.set_oke_node_pool_size(nodepool_id, size, config=config)
  nodepool = n["nodepool"]
  print("%s: %s %d" % (nodepool["name"], nodepool["id"], nodepool["size"]))
