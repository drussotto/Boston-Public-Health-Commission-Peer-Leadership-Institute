#!/bin/bash
export PLI_SETTINGS=test_settings.cfg
exec python -m unittest discover -s tests -p "*test.py"
