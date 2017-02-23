Project Members:

* Alex Berberi
* Howard Cheung
* Bill Caruso
* Neil Locketz
* Daniel Russotto

## Installation:

For those of you who are using OSX or linux (or Cygwin) I've written a script to get you set up.
It depends on python2.7, virtualenv-2.7, and possibly pip2, and requires them to be on your PATH.

The script is "init.sh" and will set up your virtual environment and install the proper dependencies.
There is also a "test-app.py" which is the example web page given in the AWS example, so that you can make sure your stuff installed properly.

If you aren't able to use the script you will need to create a virtual environment named 'virtenv'
and install the requirements in 'requirements.txt' to it.

## Running the application:

To run a local version of the app you can run `./run-local.sh`.
To use the full functionality of the site, you'll need to install mongodb locally so you can use it with no username or password on `localhost:27017` (this is the default).
You'll also need a local smtp server, I'd recommend `sendmail` which is easy to get on linux & mac (the default installation works for this also).

## Running the tests:

To run the function & unit tests you can run the script `./run-tests.sh`. Running the tests doesn't require a local mongodb installation or a local mailserver.

## Common Problems:

1. If you see the error

```
Traceback (most recent call last):
  File "test-app.py", line 1, in <module>
    from flask import Flask
ImportError: No module named flask
```
You probably don't have the virtual env activated, in which case you should run 'source ./virtenv/bin/activate'


-- MORE COMING LATER --
