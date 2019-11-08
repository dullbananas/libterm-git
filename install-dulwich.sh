#!/bin/sh
pip3.7 install -t . dulwich --global-option="--pure" --no-deps --upgrade
rm -rf bin docs *.egg-info
