#!/usr/bin/env bash

set -e
set -x

mypy thumbhash
ruff check thumbhash tests
black thumbhash tests --check
isort thumbhash tests --check-only
