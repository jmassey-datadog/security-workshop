import json

from routes import app

# # step 1 - enable this
# # only allow the following outcomes for authentication logs
# AUTH_OUTCOMES = ["success", "failure"]
#
def auth_log(outcome, user, client_ip, event_name="authentication", reason=None):
    """
    :param outcome: this is the outcome and is typically success or failure
    :param user: the username making the request
    :param client_ip: the IP address making the request
    :param reason: the reason the authentication failed. note: this is not available on SUCCESS
    :param event_name: The event name
    :return:
    """

    # we wrap everything within quotes so that we ensure that the grok parser can easily understand
    # where to start and stop parsing for the attribute in case there is a space in any of the values

    # todo: I should probably add additional information to the log, but I don't have time today. Will come back
    # tomorrow and add it
    s = 'network.client.ip="{client_ip}" evt.name="{event_name}"'.format(
        client_ip=client_ip,
        event_name=event_name,
    )
    """
    this will get processed as the following in Datadog
    {
      "evt": {
        "name":"authentication"
      }
      "network": {
        "client":{
          "ip":"1.2.3.4"
        }
      }
    }
    """
    app.logger.info(s)

def check_login(username, password, client_ip):
    # ensure username and password have values
    if not username:
        app.logger.info('Username must have a value')
        return False
    if not password:
        app.logger.info('Paassword must have a value')
        return False

    # check username and password against the user file
    with open('users.json') as f:
        users = json.load(f)

    # get user object from dictionary
    user = users.get(username, {})

    # username does not exist
    if not user:
        auth_log("failure", username, client_ip, reason="user does not exist")
        return False

    # username and password do not match
    if user.get('password') != password:
        auth_log("failure", username, client_ip, reason="incorrect password")
        return False

    # username and password match
    else:
        auth_log("success", username, client_ip)
        return user
