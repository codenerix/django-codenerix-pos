import json
import logging
from channels import Channel
from channels.sessions import channel_session
#from .models import Job
from .tasks import sec3
#from example.celery import app

log = logging.getLogger(__name__)



from django.http import HttpResponse
from channels.handler import AsgiHandler

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session
def ws_connect(message):
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })


@channel_session
def ws_receive(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "start_sec3":
            start_sec3(data, reply_channel)


@channel_session
def ws_disconnect(message, room_name):
    # Group("chat-%s" % room_name).discard(message.reply_channel)
    pass

def start_sec3(data, reply_channel):
    job_id=data['job_id']
    log.debug("job ID=%s", job_id)
    # Save model to our database
#    job = Job(
#        name=data['job_name'],
#        status="started",
#    )
#    job.save()

    # Start long running task here (using Celery)
    # sec3_task = sec3.delay(job_id, reply_channel)
    sec3.delay(job_id, reply_channel)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    #job.celery_id = sec3_task.id
    #job.save()

    # Tell client task has been started
    Channel(reply_channel).send({
        "text": json.dumps({
            "action": "started",
            "job_id": job_id,
            # "job_name": job.name,
            # "job_status": job.status,
        })
    })
