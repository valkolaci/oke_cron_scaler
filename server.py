# -*- coding: UTF-8 -*-
#
# server.py
#

import os
import sys
import io
import json
from fdk import response
import oci.identity

from cfg import Config
import oke

# Print env variables
for key, value in os.environ.items():
  print("%s=%s" % (key, value))

# Read and parse configuration
c = Config.read_config()
print(c.dump())

nodepool_id = os.environ['NODEPOOL_ID'] if 'NODEPOOL_ID' in os.environ else None
default_size = os.environ['DEFAULT_SIZE'] if 'DEFAULT_SIZE' in os.environ else None

if nodepool_id is None or nodepool_id == '':
  raise "Missing NODEPOOL_ID environment parameter"
if default_size is None or default_size == '':
  raise "Missing DEFAULT_SIZE environment parameter"
try:
  default_size = int(default_size)
except (ValueError) as ex:
  raise "Invalid non integer DEFAULT_SIZE environment parameter"

# Handle REST calls
def handler(ctx, data: io.BytesIO = None):
#    try:
#      body = json.loads(data.getvalue())
#      nodepool_id = body.get("nodepool_id")
#      if nodepool_id is None or nodepool_id == "":
#        raise "Missing nodepool_id parameter"
#      size = body.get("size")
#      if size is None or size == "":
#        raise "Missing size parameter"
#      try:
#        size = int(size)
#      except (ValueError) as ex:
#        raise "Invalid size parameter (not an integer)"
#    except (Exception, ValueError) as ex:
#      print(str(ex), flush=True)
#
#    print("Requested node pool '%s' change size: %d" % (nodepool_id, size))

    signer = oci.auth.signers.get_resource_principals_signer()
    resp = get_oke_node_pool(nodepool_id, signer=signer)
    np = resp["nodepool"]
    current = np["size"]
    print("Requested node pool current size: %d" % (current))

    size = default_size

    if current == size:
      print("No change needed")
    else:
      print("Updating node pool '%s' to size: %d" % (nodepool_id, size))
      resp = set_oke_node_pool(nodepool_id, size, signer=signer)

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
