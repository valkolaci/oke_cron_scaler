# -*- coding: UTF-8 -*-

# OCI Function to scale an OKE Node pool as a function of time according to a rule set

# Mandatory variables:
#   NODEPOOL_ID      OCI ID of the node pool (string)
#   DEFAULT_SIZE     Default size to use for the node pool (integer)
# Optional variables:
#   CONFIG_NAME      Name of config file containing the rules (string) [default: rules.yaml]

import os
import sys
import io
import logging
from fdk import response
import oci.identity

from logs import fatal_exception
from cfg import Config
import oke

logger = logging.getLogger(__name__)

class ServerError(Exception):
  def __init__(self, message):
    super().__init__(message)

class Server:
  def __init__(self):
    try:
      self.init_params()
    except ServerError as e:
      logger.error(e.args[0])
      sys.exit(1)
    except Exception as e:
      fatal_exception('error initializing server', e)

  def init_params(self):
    logger.info("== Env variables:")
    for key, value in os.environ.items():
      logger.info("%s=%s" % (key, value))

    self.nodepool_id = os.environ['NODEPOOL_ID'] if 'NODEPOOL_ID' in os.environ else None
    self.default_size = os.environ['DEFAULT_SIZE'] if 'DEFAULT_SIZE' in os.environ else None

    if self.nodepool_id is None or self.nodepool_id == '':
      raise ServerError("Missing NODEPOOL_ID environment parameter")
    if self.default_size is None or self.default_size == '':
      raise ServerError("Missing DEFAULT_SIZE environment parameter")
    try:
      self.default_size = int(self.default_size)
    except (ValueError) as ex:
      raise ServerError("Invalid non integer DEFAULT_SIZE environment parameter")

    logger.info("== Config file:")
    self.config = Config.read_config()
    logger.info(self.config.dump())

  def handler(ctx, data: io.BytesIO = None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = get_oke_node_pool(self.nodepool_id, signer=signer)
    np = resp["nodepool"]
    current = np["size"]
    logger.info("Requested node pool current size: %d" % (current))

    size = self.default_size
    if current == size:
      logger.info("No change needed")
    else:
      logger.info("Updating node pool '%s' to size: %d" % (self.nodepool_id, self.default_size))
      resp = set_oke_node_pool(self.nodepool_id, self.size, signer=signer)

    return resp
