#!/usr/bin/env bash

echo "Setting up ..." && echo

virtualenv virtenv > /dev/null
source ./virtenv/bin/activate

# Install flask to new virtualenv
pip install -r ./requirements.txt > /dev/null

cat <<EOF
You're all set!

Just run 'source ./virtenv/bin/activate' to activate the virtualenv.

To test that you have flask installed properly please run: 'python test-app.py'

This should print out a link telling you how to access the site in your browser.

To turn off the virtualenv just run the command: 'deactivate'
To turn on the virtualenv run (from the current directory): 'source ./virtenv/bin/activate'
EOF
