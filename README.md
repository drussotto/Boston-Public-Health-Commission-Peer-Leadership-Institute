## Project Members:

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
See the info about how our tests are set up [here](#about-our-testing-infrastructure).

## Common Problems:

1. If you see the error

```
Traceback (most recent call last):
  File "test-app.py", line 1, in <module>
    from flask import Flask
ImportError: No module named flask
```
or any version of this with flask replaced by another module, 
You probably don't have the virtual env activated, in which case you should run 'source ./virtenv/bin/activate'.
If you do have it activated you should install the required dependancies via `pip install -r requirements.txt`

# About our testing infrastructure

This will give a high level overview of the testing infrastructure we have, and how to extend it.
If you have further questions you should read the comments in the code, those will go more in depth.

### About test cases

All of the PLI site test cases extend from our base test case class `testlib.PliTestCase`.
That class provides the common functionality which lets users hook into the mocking process for the mongo db in order to supply a database matching their needs. When subclassing `testlib.PliTestCase` you must also implement the `mocked_db(self)` method. This method should return an instance of the mongomock database with all the data your test will need. `mocked_db` is run before every unit test, so changes made during other tests will not persist. For convinience there are two subclasses of `testlib.PliTestCase` that have been supplied: `testlib.PliUsersTestCase`, `testlib.PliQotdTestCase`. These are seeded with common users/questions from the `testlib` module. If your test needs users, you should extend from `testlib.PliUsersTestCase`, then when inside your unit test, you will have access to `testlib.user1`, `testlib.user2`, `testlib.user3` inside of the db (see [app globals section](#app-globals-location-info) for info on how to access the fake db in a test). For `testlib.PliQotdTestCase` you will get all the `question*` from `testlib`.

### Getting flask contexts during tests

Because flask only allows access to certain things when you are running code in certain contexts, we have features that allow easier access. There are two kinds of contexts that we care about in flask, the [application context](http://flask.pocoo.org/docs/0.12/appcontext/), and the [request context](http://flask.pocoo.org/docs/0.12/reqcontext/). In our test library two of our decorators are `testlib.with_app_ctxt` (with app context), and `testlib.with_req_ctxt` (with request context), which allow us to simulate these contexts. Any decorators from testlib must be applied to unit-test methods (methods that begin with `test` and are a member of a testcase class). These two decorators form the base of the other decorating functions inside the library. Decorating a method with `testlib.with_app_ctxt` just works and doesn't require any extra arguments, and any code within the test method will be run within a the pli app context. `testlib.with_req_ctxt` requires an additional argument `client` which is a [test client](http://flask.pocoo.org/docs/0.12/api/#flask.testing.FlaskClient) (No anchor to the documentation for `app.test_client()` but that is what you really want). You can make any http requests you need via this test client, and your test function will be in the same context as your request after it has been completed (this is important because it keeps the session, among other things; good for logins ... etc). `testlib.with_test_client` is the same as `testlib.with_req_ctxt` except it doesn't keep the context within the test method, it only provides a test client as an argument. `testlib.with_login` is a decorator which takes 2 arguments, an email address and password, and an optional keyword argument `to`. This decorator should be used in conjunction with `testlib.with_req_ctxt` to simulate a logged-in user during unit tests (see [this file](tests/session_auth_test.py) for examples).

### Testing for correct web page responses

`testlib` exports a few useful functions that check whether a reponse to an http call is a certain web page or not. By convention, there are always to for each page, `assert_*_page`, and `assert_not_*_page` (listed [here](tests/testlib.py#L115)). They take a unittest instance as their first argument (for assertions), a response request, or the response data.

# App globals location info

We are storing the database connection in the apps config under the key `db`. given the application object, `application`, you'd get the pli database with the code `application.config["db"]`. If you are in an application context, or a request context you can use the proxy `current_app` (from flask module), so you would do `current_app.config["db"]`

-- MORE COMING LATER --
