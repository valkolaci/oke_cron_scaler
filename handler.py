# -*- coding: UTF-8 -*-

import io
import json

from server import Server

server = Server()

def handler(ctx, data: io.BytesIO = None):
  resp = server.handler(ctx, data)
  return response.Response(
    ctx,
    response_data=json.dumps(resp),
    headers={"Content-Type": "application/json"}
  )
