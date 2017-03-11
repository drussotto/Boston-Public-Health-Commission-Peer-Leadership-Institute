#!/bin/bash
export PLI_SETTINGS=test_settings.cfg
exec coverage html --omit "tests/*,*.cfg,virtenv/*"
