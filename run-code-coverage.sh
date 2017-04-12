#!/bin/bash
export PLI_SETTINGS=test_settings.cfg
exec coverage run --omit "mongomock/*,tests/*,*.cfg,virtenv/*" -m unittest discover -s tests -p "*test.py"
