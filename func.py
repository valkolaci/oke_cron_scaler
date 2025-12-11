#
# oci-list-compartments-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json

from fdk import response
import oci.identity

def handler(ctx, data: io.BytesIO = None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = list_compartments(signer)  # function defined below
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

# Calculate compartment path through parent links
def get_compartment_path(compartments_by_id, tenancy_id, c):
    name = c["name"]
    while True:
      parent_id = c["parent_id"]
      if parent_id == tenancy_id:
        break
      c = compartments_by_id[parent_id]
      name = "%s/%s" % (c["name"], name)
    return name

# List compartments
def list_compartments(config = {}, **kwargs):
    client = oci.identity.IdentityClient(config=config, **kwargs)
    # OCI API for managing users, groups, compartments, and policies
    try:
        signer = kwargs.get('signer', None)
        tenancy_id = signer.tenancy_id if signer is not None and 'tenancy_id' in signer else config['tenancy'] if config is not None and 'tenancy' in config else None
        # Returns a list of all compartments and subcompartments in the tenancy (root compartment)
        compartments = client.list_compartments(
            tenancy_id,
            compartment_id_in_subtree=True,
            access_level='ANY'
        )
        compartments_by_id = dict()
        compartments_by_path = dict()
        for c in compartments.data:
          compartments_by_id[c.id] = {
            "id": c.id,
            "name": c.name,
            "parent_id": c.compartment_id
          }
        for c in compartments_by_id.values():
          path = get_compartment_path(compartments_by_id, tenancy_id, c)
          c["path"] = path
          compartments_by_path[path] = c
        compartments = [compartments_by_id[c.id] for c in compartments.data]
    except Exception as ex:
        print("ERROR: Cannot access compartments", ex, flush=True)
        raise
    resp = {"compartments": compartments}
    return resp

# List OKE clusters
def list_oke_clusters(compartment_id, config = {}, **kwargs):
    client = oci.container_engine.ContainerEngineClient(config=config, **kwargs)
    try:

        clusters = client.list_clusters(
            compartment_id
        )
        # Create a list that holds a list of the clusters id and name next to each other
        clusters = [{ "id": c.id, "name": c.name, "object": c } for c in clusters.data]
    except Exception as ex:
        print("ERROR: Cannot access clusters", ex, flush=True)
        raise
    resp = {"clusters": clusters}
    return resp
