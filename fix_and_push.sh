#!/bin/bash
cd /home/solubrew/.arthr/workspace/projects/nchantrs
git add -A
git commit -m "fix: use safe getattr for has_pro access in browsers.py

Prevents AttributeError when user is not yet initialized"
git push origin gamma
echo "Done"
