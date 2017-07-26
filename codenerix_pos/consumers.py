import json
import uuid
import pyotp
import base64
import hashlib

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
        self.debug("    session: {}".format(self.message.channel_session.__dict__), color='purple')
        self.debug("       user: {}".format(self.message.user), color='purple')

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

        # Remember it in out session
        challenge = self.message.channel_session.get("challenge", None)
        if challenge is None:
            # Create a new challenge
            challenge = uuid.uuid4().hex
            self.message.channel_session["challenge"] = challenge
            self.debug("NEW CHALLENGE: {}".format(challenge), color="red")
        else:
            self.debug("GO WITH EXISTING CHALLENGE: {}".format(challenge), color="green")

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
