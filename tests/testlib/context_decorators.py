import inspect
from application import application as pli
from post_utils import post_login

# This decorator takes a username and password to attempt a login with
# the optional 'to' argument specifies what the 'next' query argument of the login
# should be. If left empty next won't be given in the url.
# The function this decorates can take either 1 or 2 additional aguments (excluding self)
# if your test function takes one additional argument, a test_client is supplied
# which is logged in with the username and password. If your function takes 2 additional arguments
# the second one will be the response from the login call (will be the index page if you didn't)
# supply a 'to' keyword arg. The function that is being decorated is run inside the request context
# of the given client.
def with_login(username, passwd, to=None):
    def decorator(f):
        def actual_function(s):
            with pli.test_client() as client:
                n = ("?next="+to) if to is not None else ""
                r = post_login(client, username, passwd, url='/login'+n)
                p_len = len(inspect.getargspec(f).args)
                if p_len == 1:
                    f(s)
                elif p_len == 2:
                    f(s, client)
                elif p_len == 3:
                    f(s, client, r)
                else:
                    # TODO
                    pass
        return actual_function
    return decorator

# Supplies a test client to the function being decorated
def with_test_client(f):
    def run_test(s):
        f(s, pli.test_client())
    return run_test

# Runs the function being decorated inside the pli app context.
def with_app_ctxt(f):
    def run_test(s):
        with pli.app_context():
            f(s)
    return run_test
