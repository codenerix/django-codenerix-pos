import json
import uuid

from channels.generic.websockets import JsonWebsocketConsumer

from codenerix.lib.debugger import Debugger
from codenerix_pos.models import POS, POSHardware, POSLog
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
        answer = {'action': 'error', 'error': msg}
        if pos is None:
            # Use basic send (unprotected)
            self.warning("Send '{}' to Anonymous".format(msg))
            super(POSConsumer, self).send({'message': json.dumps(answer)})
        else:
            # Use normal send (protected)
            self.warning("Send '{}' to {}".format(msg, pos))
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
        # self.debug("New message arrived: {}".format(request), color='yellow')

        if isinstance(request, dict):
            # Check if we got msg
            message = request.get('message', None)
            if message is not None:

                # Get data from the package
                uuidtxt = request.get('uuid', None)

                if uuidtxt is not None:
                    uid = uuid.UUID(uuidtxt)

                    # Try to locate the POS in the database
                    pos = POS.objects.filter(uuid=uid).first()

                    if pos:
                        # Decrypt message
                        msg = self.crypto.decrypt(message, pos.key)
                        try:
                            query = json.loads(msg)
                        except Exception:
                            query = None
                        if query is not None and isinstance(query, dict):
                            pos.channel = str(self.message.reply_channel)
                            pos.save(doreset=False)
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
                    self.send_error("Not authorized!")

            else:
                self.send_error("Missing 'message' or is None")

        else:
            self.send_error("This server only accepts dictionaries")

    def recv(self, message, pos):
        """
        Called when a message is received with decoded JSON content
        """

        self.debug("Receive: {}".format(message), color="cyan")

        action = message.get('action', None)

        # Check the action that it is requesting
        if action == 'get_config':
            # Get all the hardware connected to this POS
            answer = {}
            answer['action'] = 'config'
            answer['hardware'] = []
            for hw in pos.hardwares.filter(enable=True):
                # Prepare to send back the config
                answer['hardware'].append({'kind': hw.kind, 'config': hw.config, 'uuid': hw.uuid.hex})
            self.debug("{} - Send: {}".format(pos, answer), color='green')
            self.send(answer, pos)
        elif action == 'msg':
            uid = message.get('uuid', None)
            msg = message.get('msg', None)
            if uid:
                origin = POSHardware.objects.filter(uuid=uuid.UUID(uid)).first()
                if origin:
                    self.debug("Got a message from {}: {}".format(origin.uuid, msg), color='purple')
                    origin.recv(msg)
                else:
                    self.debug("Got a message from UNKNOWN {}: {}".format(uid, msg), color='purple')
            else:
                self.debug("Got a message from NO-UUID: {}".format(msg), color='purple')
        elif action == 'ping':
            super(POSConsumer, self).send({'message': json.dumps({'action': 'pong'})})
        elif action == 'pong':
            self.debug("Got PONG {}".format(message.get('ref', '-')), color='white')
        elif action == 'error':
            uid = message.get('uuid', None)
            msg = message.get('error', 'No error')
            if uid:
                self.error("Got an error from {}: {} (UUID:{})".format(pos.uuid, msg, uid))
            else:
                self.error("Got an error from {}: {})".format(pos.uuid, msg))
            log = POSLog()
            log.pos = pos
            if uid:
                poshw = POSHardware.objects.filter(uuid=uid).first()
                if poshw:
                    log.poshw = poshw
                    log.uuid = poshw.uuid
            else:
                log.uuid = pos.uuid
            log.log = message.get('error', None)
            log.save()
        else:
            # Unknown action
            self.send_error("Unknown action '{}'".format(action), pos)
