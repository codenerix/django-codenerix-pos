import time
import json
import uuid
import pyotp
import base64
import hashlib
import threading

from channels import Channel
from channels.generic.websockets import JsonWebsocketConsumer

from codenerix.lib.debugger import Debugger
from codenerix_pos.models import POS


class POSConsumer(JsonWebsocketConsumer, Debugger):

    # We want sessions
    http_user = True

    # Set to True if you want it, else leave it out
    # strict_ordering = True

    def __init__(self, *args, **kwargs):

        # Initialize Debugger
        self.set_name("POSConsumer")
        self.set_debug()

        # Let it keep going normal
        super(POSConsumer, self).__init__(*args, **kwargs)

    @property
    def authenticated(self):
        return self.message.channel_session.get("POS", False)

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        self.debug("New connection", color="blue")
        self.request_to_authenticate()

    def receive(self, message, **kwargs):
        """
        Called when a message is received with decoded JSON content
        """
        self.debug("")
        self.debug("Receive:{} - {}".format(message, self.authenticated), color="cyan")
        self.debug("    session: {}".format(self.message.channel_session._session_cache), color='purple')

        # Get action
        if type(message) is dict:
            action = message.get('action', None)

            if action is not None:

                # Check the action that it is requesting
                if action == 'authenticate':
                    # User is requesting to be authenticated, let's do it
                    self.check_authentication_request(message)
                else:
                    # The user is requesting another action, if authenticated, let it go!
                    if self.authenticated:
                        # Choose the users action
                        if action in ['known']:
                            # Everything is fine, keep going!
                            self.debug("Keep going", color="green")
                        else:
                            # Unknown action
                            self.send_error("Unknown action '{}'".format(action))
                    else:
                        # Push the user to authenticate
                        self.request_to_authenticate()
            else:
                # No action
                self.send_error("No action specified")
        else:
            # Not a dictionary
            self.send_error("This server only accepts dictionaries")

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        self.warning("Client got disconnected")

    def send_error(self, msg):
        # Send the challenge
        self.error("ERROR: {}".format(msg))
        self.send({
                "action": "error",
                "error": msg,
            })

    def request_to_authenticate(self):
        self.warning("Request to authenticate")

        # Create a new challenge
        challenge = uuid.uuid4().hex

        # Remember it in out session
        print(getattr(self.message.session, "challenge", None))
        if self.message.channel_session.get("challenge", None) is None:
            self.message.session.challenge = challenge
            self.message.channel_session["challenge"] = challenge
            self.debug("CHALLENGE", color="red")
        else:
            self.debug("GO", color="green")

        # Send the challenge
        self.message.reply_channel.send({

            # Accept the connection; this is done by default if you don't override the connect function.
            "accept": True,

            "text": json.dumps({
                "action": "authenticate",
                "version": "1.0",
                "challenge": challenge
                }
            )})

    def check_authentication_request(self, message):
        # Prepare the basic answer for this service
        answer = {"action": "authenticated"}

        # Get data from the package
        cid = message.get('id', '')

        # Try to locate the POS in the database
        pos = POS.objects.filter(cid=cid).first()

        if pos:
            # If we found it, get the token from the package
            token = message.get('token', '')

            # Read the challenge key we sent to our client
            challenge = self.message.channel_session["challenge"]

            # Build a temporaly hash
            hashkey = "{}{}".format(challenge, pos.token)
            hash32 = base64.b32encode(bytes(hashkey, 'utf-8'))
            totp = pyotp.TOTP(hash32).now()
            localtoken = hashlib.sha1(bytes("{}{}".format(hashkey, totp), 'utf-8')).hexdigest()

            # Check if our hash match our client's hash
            auth = localtoken == token
        else:
            # Not found in the database, not authorized!
            auth = False

        # Write result
        answer['result'] = auth

        # Check if we should add some hardware information
        if auth:
            # Remember the POS
            self.message.channel_session["POS"] = pos
            # Get all the hardware connected to this POS
            answer['hardware'] = []
            for hw in pos.hardwares.all():
                # Prepare to send back the config
                answer['hardware'].append({'kind': hw.kind, 'config': hw.config})

            # Show authenticated answer
            self.debug("Send:{}".format(answer), color='green')
        else:
            # Show not authenticated answer
            self.debug("Send:{}".format(answer), color='red')

        # Send the authentication answer
        self.send(answer)


# def http_consumer(message):
#    # Make standard HTTP response - access ASGI path attribute directly
#    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#    # Encode that response into message format (ASGI)
#    for chunk in AsgiHandler.encode_response(response):
#        message.reply_channel.send(chunk)


def worker(reply_channel):
    def go():
        a = True
        while True:
            Channel(reply_channel).send({
                    "text": json.dumps({
                        "action": a and "hello dear" or "goodbye cocodrile",
                        "job_id": 'xyz',
                        # "job_name": job.name,
                        # "job_status": job.status,
                    })
                })
            a = not a
            time.sleep(1)
            break
    return go


def ws_receive(message):

    # Read message
    try:
        data = json.loads(message['text'])
    except ValueError:
        # log.debug("ws message isn't json text=%s", message['text'])
        return

    print(data)

    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = None  # parse_qs(message.content["query_string"])
    if None and "username" in params:
        # Set the username in the session
        message.channel_session["username"] = params["username"]
        # Add the user to the room_name group
        # Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

    print(data)
    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "start_sec3":

            thread = threading.Thread(target=worker(reply_channel))
            thread.start()

            # Tell client task has been started
            Channel(reply_channel).send({
                "text": json.dumps({
                    "action": "started",
                    "job_id": 'xyz',
                    # "job_name": job.name,
                    # "job_status": job.status,
                })
            })
