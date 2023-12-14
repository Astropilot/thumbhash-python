#!/usr/bin/env bash

set -e
set -x

mypy thumbhash
ruff check thumbhash tests
