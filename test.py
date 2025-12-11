#!/usr/bin/env python

import func
import oci

config = oci.config.from_file()
resp = func.list_compartments(config=config)  # function defined below
print(resp)
