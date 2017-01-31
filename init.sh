#!/usr/bin/env bash

echo "Setting up ..." && echo

ask_install () {
    echo "Please install $1, or put it on your PATH" > /dev/stdout
    exit 1
}

# Check that python-2.7 & virtualenv-2.7 is installed and on PATH
[ which python2.7 > /dev/null 2>&1 ] && ask_install python2.7
[ which virtualenv-2.7 > /dev/null 2>&1 ] && ask_install virtualenv-2.7

virtualenv-2.7 virtenv > /dev/null
source ./virtenv/bin/activate

# Make sure we have pip2 too
[ which pip2 > /dev/null 2>&1 ] && ask_install pip2

# Install flask to new virtualenv
pip2 install -r ./requirements.txt > /dev/null

cat <<EOF
You're all set!

Just run 'source ./virtenv/bin/activate' to activate the virtualenv.

To test that you have flask installed properly please run: 'python2.7 test-app.py'

This should print out a link telling you how to access the site in your browser.

To turn off the virtualenv just run the command: 'deactivate'
To turn on the virtualenv run (from the current directory): 'source ./virtenv/bin/activate'
EOF
