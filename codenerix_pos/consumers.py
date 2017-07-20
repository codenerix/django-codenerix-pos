import time
import json
import uuid
import pyotp
import base64
import hashlib
import threading
from channels import Channel


from channels.generic.websockets import JsonWebsocketConsumer

class POSConsumer(JsonWebsocketConsumer):

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        print("Connect")
        
        challenge = uuid.uuid4().hex
        message.channel_session["challenge"] = challenge
        message.reply_channel.send({
            
            # Accept the connection; this is done by default if you don't override the connect function.
            "accept":True,
            
            "text": json.dumps({
                "action": "authenticate",
                "version":"1.0",
                "challenge":challenge
                }
            )})


    def receive(self, message, **kwargs):
        """
        Called when a message is received with decoded JSON content
        """
        print("Receive:{}".format(message))
        
        action = message.get('action', None)
        if action == 'authenticate':
            cid = message.get('id', '')
            token = message.get('token', '')
            
            key = cid
            challenge = self.message.channel_session["challenge"]
            
            hashkey = "{}{}".format(challenge, key)
            hash32 = base64.b32encode(hashkey)
            totp = pyotp.TOTP(hash32).now()
            
            localtoken = hashlib.sha1("{}{}".format(hashkey,totp)).hexdigest()
            
            auth = localtoken == token
            self.send({"authenticated":auth})
            
        else:
            print("Unknown action")

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        print("Disconnect")
        pass

#def http_consumer(message):
#    # Make standard HTTP response - access ASGI path attribute directly
#    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#    # Encode that response into message format (ASGI)
#    for chunk in AsgiHandler.encode_response(response):
#        message.reply_channel.send(chunk)


def worker(reply_channel):
    def go():
        a=True
        while True:
            Channel(reply_channel).send({
                    "text": json.dumps({
                        "action": a and "hello dear" or "goodbye cocodrile",
                        "job_id": 'xyz',
                        # "job_name": job.name,
                        # "job_status": job.status,
                    })
                })
            a=not a
            time.sleep(1)
            break
    return go

def ws_receive(message):
    
    # Read message
    try:
        data = json.loads(message['text'])
    except ValueError:
        #log.debug("ws message isn't json text=%s", message['text'])
        return
    
    print(data)
    
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = None # parse_qs(message.content["query_string"])
    if None and "username" in params:
        # Set the username in the session
        message.channel_session["username"] = params["username"]
        # Add the user to the room_name group
        #Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})
    
    print(data)
    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "start_sec3":
            
            thread = threading.Thread(target = worker(reply_channel))
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

