from slackclient import SlackClient


class Slack:

    sc = None

    def __init__(self, token):
        self.sc = SlackClient(token)

    def send_message(self, to, message):
        self.sc.api_call(
            "chat.postMessage",
            channel=to,
            text=message,
            as_user=True
        )
