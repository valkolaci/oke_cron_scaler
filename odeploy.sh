#!/bin/bash

APP=oke-cron-scaler
FUNC=oke-cron-scaler

fn create context eu-frankfurt-2 --provider oracle --api-url https://functions.eu-frankfurt-2.oci.oraclecloud.eu
fn use context eu-frankfurt-2
fn update context registry ocir.eu-frankfurt-2.oci.oraclecloud.eu/ax8libfuujx6/oke-cron-scaler
fn update context oracle.compartment-id ocid1.compartment.oc19..aaaaaaaazhwn2tlcuqs7zk6ld43aei444toald36apkbb4kpk2igz2ozoxaq
fn update context oracle.image-compartment-id ocid1.compartment.oc19..aaaaaaaazhwn2tlcuqs7zk6ld43aei444toald36apkbb4kpk2igz2ozoxaq

# enap-tst		ocid1.compartment.oc19..aaaaaaaazhwn2tlcuqs7zk6ld43aei444toald36apkbb4kpk2igz2ozoxaq
# sn-oke-tst-node	ocid1.subnet.oc19.eu-frankfurt-2.aaaaaaaazqcit2gjl6fc4gdknue7fx3klovbusmf3znvau6wmdxecbmlvkia	

fn create app "$APP" --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc19.eu-frankfurt-2.aaaaaaaazqcit2gjl6fc4gdknue7fx3klovbusmf3znvau6wmdxecbmlvkia"]'
#fn create function "$APP" "$FUNC" "$IMAGE"
fn -v deploy --app "$APP"
fn config function "$APP" "$FUNC" NODEPOOL_ID "ocid1.nodepool.oc19.eu-frankfurt-2.aaaaaaaa4nwnx5to6n2fqjgkabk6ohwo6c5sgizaaulwdl6kinodbkywhb2q"
fn config function "$APP" "$FUNC" DEFAULT_SIZE 1
fn config function "$APP" "$FUNC" CONFIG_FILE config.example.yaml
