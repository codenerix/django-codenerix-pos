import json
import uuid
import pyotp
import base64
import hashlib

from channels import Group
from channels.sessions import channel_session

from codenerix_pos.models import POS


def send_error(message, msg, uid):
    # Send the challenge
    print("ERROR: {}".format(msg))
    Group("chat-{}".format(uid)).send({
            "text": json.dumps({
                "action": "error",
                "error": msg,
            })})


def request_to_authenticate(message, uid, base=False):
    print("Request to authenticate")

    # Create a new challenge
    challenge = uuid.uuid4().hex

    # Remember it in out session
    if message.channel_session.get("challenge", None) is None:
        message.channel_session["challenge"] = challenge
        print("NEW CHALLENGE: {}".format(challenge))
    else:
        challenge = message.channel_session["challenge"]
        print("GO WITH EXISTING CHALLENGE: {}".format(challenge))

    answer = json.dumps({
            "action": "authenticate",
            "version": "1.0",
            "challenge": challenge
            })

    # Send the challenge
    if base:
        # Accept the connection; this is done by default if you don't override the connect function.
        message.reply_channel.send({
                "accept": True,
        })
        message.channel_session["username"] = "JUJU"
        Group("chat-{}".format(uid)).add(message.reply_channel)
    Group("chat-{}".format(uid)).send({
            "text": answer
        })


def check_authentication_request(message, msg, uid):
    print("CHECK AUTH")
    # Prepare the basic answer for this service
    answer = {"action": "authenticated"}

    # Get data from the package
    cid = msg.get('id', '')

    # Try to locate the POS in the database
    pos = POS.objects.filter(cid=cid).first()

    if pos:
        # If we found it, get the token from the package
        token = msg.get('token', '')

        # Read the challenge key we sent to our client
        challenge = message.channel_session["challenge"]

        # Build a temporaly hash
        hashkey = "{}{}".format(challenge, pos.token)
        hash32 = base64.b32encode(bytes(hashkey, 'utf-8'))
        totp = pyotp.TOTP(hash32).now()
        localtoken = hashlib.sha1(bytes("{}{}".format(hashkey, totp), 'utf-8')).hexdigest()

        print("   > CHALLENGE: {}".format(challenge))
        print("   > KEY:       {}".format(pos.token))
        print("   > HASHKEY:   {}".format(hashkey))
        print("   > HASH32:    {}".format(hash32))
        print("   > TOTP:      {}".format(totp))
        print("   > TOKEN LOC: {}".format(localtoken))
        print("   > TOKEN REM: {}".format(token))

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
        message.channel_session["POS"] = pos
        # Get all the hardware connected to this POS
        answer['hardware'] = []
        for hw in pos.hardwares.all():
            # Prepare to send back the config
            answer['hardware'].append({'kind': hw.kind, 'config': hw.config})

        # Show authenticated answer
        print("Send:{}".format(answer))
        Group("chat-{}".format(uid)).send({
            'text': json.dumps(answer)
        })
    else:
        # Show not authenticated answer
        print("Send:{}".format(answer))

    # Send the authentication answer
    Group("chat-{}".format(uid)).send({
            "text": answer
        })


@channel_session
def ws_message(message, uid):
    """
    Called when a message is received with decoded JSON content
    """
    print("================================================")
    print("MESSAGE RECEIVED FROM {}: {}".format(uid, message.content))
    authenticated = None
    msg = json.loads(message.content.get('text'))
    print("Receive:{} - {}".format(msg, authenticated))
    print("    session: {}".format(message.channel_session._session_cache))
    print("    challenge: {}".format(message.channel_session.get("challenge", None)))

    # Get action
    if type(msg) is dict:
        action = msg.get('action', None)

        if action is not None:

            # Check the action that it is requesting
            if action == 'authenticate':
                # User is requesting to be authenticated, let's do it
                check_authentication_request(message, msg, uid)
            else:
                # The user is requesting another action, if authenticated, let it go!
                if authenticated:
                    # Choose the users action
                    if action in ['known']:
                        # Everything is fine, keep going!
                        print("Keep going")
                    else:
                        # Unknown action
                        send_error(message, "Unknown action '{}'".format(action), uid)
                else:
                    # Push the user to authenticate
                    request_to_authenticate(message, uid)
        else:
            # No action
            send_error(message, "No action specified", uid)
    else:
        # Not a dictionary
        send_error(message, "This server only accepts dictionaries", uid)


@channel_session
def ws_connect(message, uid):
    print("CONNECT FROM {}".format(uid))
    # Push the user to authenticate
    request_to_authenticate(message, uid, True)


@channel_session
def ws_disconnect(message, uid):
    print("DISCONNECT FROM {}".format(uid))
    Group("chat-{}".format(uid)).discard(message.reply_channel)
