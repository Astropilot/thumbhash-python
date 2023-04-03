#!/bin/sh -e
set -x

ruff check thumbhash tests --fix
black thumbhash tests
isort thumbhash tests
