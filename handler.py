# -*- coding: UTF-8 -*-

import io
import json
import oci.identity

from server import Server

server = Server()

def handler(ctx, data: io.BytesIO = None):
  signer = oci.auth.signers.get_resource_principals_signer()
  resp = server.handler(signer, ctx, data)
  return response.Response(
    ctx,
    response_data=json.dumps(resp),
    headers={"Content-Type": "application/json"}
  )
