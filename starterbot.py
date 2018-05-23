import os
import time
import re

import json

import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
QUESTION_COMMAND = "How are you?"
MORE_COMMANDS = "help"
GIPHY_COMMAND = "giphy"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND, QUESTION_COMMAND, MORE_COMMANDS, GIPHY_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(QUESTION_COMMAND):
        response = "I'm fine, thanks. How are you?"
    elif command.startswith(MORE_COMMANDS):
        response = "How can I help you?"
    elif command.startswith(GIPHY_COMMAND):

        # create an instance of the API class
        api_instance = giphy_client.DefaultApi()
        api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
        command = command.split(" ")[1:]
        tag = " ".join(command) # str | Search query term or prhase.
        rating = 'g' # str | Filters results by specified rating. (optional)
        fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

        try:
            # Search Endpoint
            api_response = api_instance.gifs_random_get(api_key, tag=tag, rating=rating, fmt=fmt)

            #pull url from json file
            def url_pull(api_response):
                x = api_response.data.url
                return x

            response = url_pull(api_response)

        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
