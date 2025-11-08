#!/usr/bin/env bash

DIR=$(dirname $0)
command "$DIR/.venv/bin/python3" "$DIR/check.py"
