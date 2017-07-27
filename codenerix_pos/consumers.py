import json

from channels.generic.websockets import JsonWebsocketConsumer

from codenerix.lib.debugger import Debugger
from codenerix_pos.models import POS
from codenerix_extensions.lib.cryptography import AESCipher


class POSConsumer(JsonWebsocketConsumer, Debugger):

    def __init__(self, *args, **kwargs):

        # Initialize Debugger
        self.set_name("POSConsumer")
        self.set_debug()

        # Cryptography
        self.crypto = AESCipher()

        # Let it keep going normal
        super(POSConsumer, self).__init__(*args, **kwargs)

    def connect(self, message, **kwargs):
        # Accept connection
        self.message.reply_channel.send({
            # Accept the connection; this is done by default if you don't override the connect function.
            "accept": True,
            })

    def disconnect(self, message, **kwargs):
        self.warning("Client got disconnected")

    def send_error(self, msg, pos=None):
        answer = {'error': True, 'errortxt': msg}
        if pos is None:
            # Use basic send (unprotected)
            super(POSConsumer, self).send(json.dumps(answer))
        else:
            # Use normal send (protected)
            self.send(answer, pos)

    def send(self, request, pos):
        # Encode request
        msg = json.dumps(request)

        # Build query
        query = {
            'message': self.crypto.encrypt(msg, pos.key).decode('utf-8'),
        }

        # Send to remote
        super(POSConsumer, self).send(query)

    def receive(self, request, **kwargs):
        self.debug("New message arrived: {}".format(request), color='yellow')

        if isinstance(request, dict):
            # Check if we got msg
            message = request.get('message', None)
            if message is not None:

                # Get data from the package
                cid = request.get('id', '')

                # Try to locate the POS in the database
                pos = POS.objects.filter(cid=cid).first()

                if pos:
                    # Decrypt message
                    msg = self.crypto.decrypt(message, pos.key)
                    try:
                        query = json.loads(msg)
                    except Exception:
                        query = None
                    if query is not None and isinstance(query, dict):
                        self.recv(query, pos)
                    else:
                        if query is None:
                            self.send_error("Message is not JSON or is None", pos)
                        else:
                            self.send_error("Message must be a Dictionary", pos)
                else:
                    # Not found in the database, not authorized!
                    self.send_error("Not authorized!")

            else:
                self.send_error("Missing 'message' or is None")

        else:
            self.send_error("This server only accepts dictionaries")

    def recv(self, message, pos):
        """
        Called when a message is received with decoded JSON content
        """
        self.debug("")
        self.debug("Receive: {}".format(message), color="cyan")
        self.debug("    POS: {}".format(pos), color='purple')

        action = message.get('action', None)

        # Check the action that it is requesting
        if action == 'get_config':
            # Get all the hardware connected to this POS
            answer = {}
            answer['hardware'] = []
            for hw in pos.hardwares.all():
                # Prepare to send back the config
                answer['hardware'].append({'kind': hw.kind, 'config': hw.config})
            self.debug("Send:{}".format(answer), color='green')
            self.send(answer, pos)
        elif action == 'HOLA':
            print("HOLA")
        else:
            # Unknown action
            self.send_error("Unknown action '{}'".format(action), pos)
