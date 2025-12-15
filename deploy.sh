#!/bin/bash

fn use context default
fn create app test-app
fn create function test-app test-func dummy:latest
fn config function test-app test-func NODEPOOL_ID "ocid1.nodepool.oc19.eu-frankfurt-2.aaaaaaaa4nwnx5to6n2fqjgkabk6ohwo6c5sgizaaulwdl6kinodbkywhb2q"
fn config function test-app test-func DEFAULT_SIZE 1
fn -v deploy --app test-app "$@"
