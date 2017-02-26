
# Runs a POST against the login endpoint with the given user and password (pas).
# url is the url that we will post against.
def post_login(client, user, pas, url="/login"):
    return client.post(url, data=dict(
        email=user, 
        password=pas
    ), follow_redirects=True)

# Runs a POST against the qotd endpoint, answering the question with the given answer.
def post_qotd(client, answer, url="/question"):
    return client.post(url, data=dict(
        qotd=answer,
    ), follow_redirects=True)
