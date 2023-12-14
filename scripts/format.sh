#!/bin/sh -e
set -x

ruff check thumbhash tests --fix
ruff format thumbhash tests
