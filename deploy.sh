#!/bin/bash

APP=test-app
FUNC=test-func
IMAGE=dummy:latest

fn use context default
fn create app "$APP"
fn create function "$APP" "$FUNC" "$IMAGE"
fn config function "$APP" "$FUNC" NODEPOOL_ID "ocid1.nodepool.oc19.eu-frankfurt-2.aaaaaaaa4nwnx5to6n2fqjgkabk6ohwo6c5sgizaaulwdl6kinodbkywhb2q"
fn config function "$APP" "$FUNC" DEFAULT_SIZE 1
fn config function "$APP" "$FUNC" CONFIG_FILE config.example.yaml
fn -v deploy --app "$APP" "$@"
