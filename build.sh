#!/usr/bin/env bash
set -e

# 1) Clean out docs/
rm -rf docs/*
mkdir -p docs

# 2) Build into public/ with the repo‐prefix
python3 src/main.py "/ssg_round2/"

# 3) Copy everything from public/ into docs/
cp -R public/* docs/

# (Optional) preview locally
cd docs && python3 -m http.server 8888
