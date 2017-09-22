import json
import uuid

from channels import Group
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

        # Set internal UUID
        self.uuid = None

        # Let it keep going normal
        super(POSConsumer, self).__init__(*args, **kwargs)

    def connect(self, message, **kwargs):
        # Accept connection
        self.message.reply_channel.send({
            # Accept the connection; this is done by default if you don't override the connect function.
            "accept": True,
            })

    def disconnect(self, message, **kwargs):
        poss = POS.objects.filter(channel=message.reply_channel)
        if poss.count():
            for pos in poss:
                pos.channel = None
                pos.save(doreset=False)
                self.warning("{} - Client got disconnected - {}".format(pos.name.encode('ascii', 'ignore'), pos.uuid))
        else:
            self.warning("Client got disconnected - REPLY CHANNEL NOT FOUND: {}".format(message.reply_channel))

    def send_error(self, msg, ref=None, pos=None):
        answer = {'action': 'error', 'error': msg}
        if pos is None:
            # Use basic send (unprotected)
            self.warning("Send '{}' to Anonymous".format(msg))
            super(POSConsumer, self).send({'message': json.dumps(answer)})
        else:
            # Use normal send (protected)
            self.warning("{} - Send '{}' to {} - {}".format(pos.name.encode('ascii', 'ignore'), msg, pos, pos.uuid))
            self.send(answer, ref, pos)

    def send(self, request, ref=None, pos=None):
        # Encode request
        msg = json.dumps({'request': request, 'ref': ref})

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
                        try:
                            msg = self.crypto.decrypt(message, pos.key)
                        except Exception:
                            msg = None

                        try:
                            query = json.loads(msg)
                        except Exception:
                            query = {}

                        if type(query) is not dict:
                            query = {}

                        request = query.get('request', None)
                        if request is not None:
                            ref = query.get('ref', None)
                            if request is not None and isinstance(request, dict):
                                pos.channel = str(self.message.reply_channel)
                                pos.save(doreset=False)
                                self.recv(request, ref, pos)
                            else:
                                if request is None:
                                    self.send_error("Message is not JSON or is None", ref, pos)
                                else:
                                    self.send_error("Message must be a Dictionary", ref, pos)
                        else:
                            self.send_error("Message doesn't belong to CODENERIX POS")
                    else:
                        # Not found in the database, not authorized!
                        self.send_error("Not authorized!")

                else:
                    self.send_error("Not authorized!")

            else:
                self.send_error("Missing 'message' or is None")

        else:
            self.send_error("This server only accepts dictionaries")

    def recv(self, message, ref, pos):
        """
        Called when a message is received with decoded JSON content
        """

        # Get action
        action = message.get('action', None)

        # Show the message we got
        if action != 'pingdog':
            self.debug("{} - Receive: {} (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), message, ref, pos.uuid), color="cyan")

        # Check the action that it is requesting
        if action == 'get_config':
            # Get all the hardware connected to this POS
            answer = {}
            answer['action'] = 'config'
            answer['commit'] = pos.commit
            answer['hardware'] = []
            for hw in pos.hardwares.filter(enable=True):
                # Prepare to send back the config
                answer['hardware'].append({'kind': hw.kind, 'config': hw.get_config(), 'uuid': hw.uuid.hex})
            self.debug(u"{} - Send: {} - {}".format(pos.name.encode('ascii', 'ignore'), answer, pos.uuid), color='green')
            self.send(answer, ref, pos)
        elif action == 'subscribe':
            # Get UUID
            uid = message.get('uuid', None)
            # Check if we got a valid UUID
            if uid:
                uid = uuid.UUID(uid)
                poshw = POSHardware.objects.filter(uuid=uid).first()
                if poshw:
                    if poshw.enable:
                        # Suscribe this websocket to group
                        self.debug("{} - Subscribed to '{}' - {}".format(pos.name.encode('ascii', 'ignore'), uid.hex, pos.uuid), color="purple")
                        Group(uid.hex).add(self.message.reply_channel)
                        self.send({'action': 'subscribed', 'uuid': uid.hex, 'key': poshw.key}, ref, pos)
                    else:
                        self.send_error("You cannot subscribe to a disabled Hardware!", ref, pos)
                else:
                    self.send_error("You cannot subscribe to a Hardware that is not available, UUID not found!", ref, pos)
            else:
                self.send_error("You have tried to subscribe to a UUID but didn't specify any or is invalid", ref, pos)
        elif action == 'msg':
            uid = message.get('uuid', None)
            msg = message.get('msg', None)
            if uid:
                origin = POSHardware.objects.filter(uuid=uuid.UUID(uid)).first()
                if origin:
                    self.debug("{} - Got a message from {}: {} (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), origin.uuid, msg, ref, pos.uuid), color='purple')
                    origin.recv(msg)
                else:
                    self.debug("{} - Got a message from UNKNOWN {}: {} (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), uid, msg, ref, pos.uuid), color='purple')
            else:
                self.debug("{} - Got a message from NO-UUID: {} (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), msg, ref, pos.uuid), color='purple')
        elif action == 'ping':
            super(POSConsumer, self).send({'message': json.dumps({'action': 'pong', 'ref': ref})})
        elif action == 'pong':
            self.debug("{} - Got PONG {} (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), message.get('ref', '-'), ref, pos.uuid), color='white')
        elif action == 'pingdog':
            super(POSConsumer, self).send({'message': json.dumps({'action': 'pongdog', 'ref': ref})})
        elif action == 'error':
            uid = message.get('uuid', None)
            msg = message.get('error', 'No error')
            if uid:
                self.error("{} - Got an error from {}: {} (UUID:{}) (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), pos.uuid, msg, uid, ref, pos.uuid))
            else:
                self.error("{} - Got an error from {}: {}) (ref:{}) - {}".format(pos.name.encode('ascii', 'ignore'), pos.uuid, msg, ref, pos.uuid))
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
            self.send_error("Unknown action '{}'".format(action), ref, pos)
