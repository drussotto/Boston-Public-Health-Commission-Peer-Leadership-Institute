Project Members

Alex Berberi

Howard Cheung

Bill Caruso

Neil Locketz

Daniel Russotto

## Installation:

For those of you who are using OSX or linux (or Cygwin) I've written a script to get you set up.
It depends on python2.7, virtualenv-2.7, and possibly pip2, and requires them to be on your PATH.

The script is "init.sh" and will set up your virtual environment and install the proper dependencies.
There is also a "test-app.py" which is the example web page given in the AWS example, so that you can make sure your stuff installed properly.

If you aren't able to use the script you will need to create a virtual environment named 'virtenv'
and install the requirements in 'requirements.txt' to it.


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