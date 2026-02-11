# oke_cron_scaler

OCI Function to scale an OKE Node pool as a function of time according to a rule set

## Parameters

Mandatory:

| Env variable | Function |
| --- | --- |
| NODEPOOL_ID | OCI ID of the node pool (string) |
| DEFAULT_SIZE | Default size to use for the node pool (integer) |

Optional:

| Env variable | Function |
| --- | --- |
| CONFIG_NAME | Name of config file containing the rules (string) [default: rules.yaml] |

## Config file syntax

```
schedules:
  everyday:
    - start: "0 20 5 * *"
      end: "0 6 1 * *"
      size: 0
rules:
  - compartment: sandbox/devops
    cluster: oke-cl
    nodepool: oke-nodepool1
    schedule: everyday
exceptions:
  - comment: Weekend testing
    compartment: sandbox/devops
    start: 2025-12-19 18:00
    end: 2025-12-22 06:00
    size: ''
```
