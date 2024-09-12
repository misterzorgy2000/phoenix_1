import sys
import oslo_messaging
from oslo_messaging import get_notification_transport, Notifier, Target, get_notification_listener
from oslo_messaging import serializer as oslo_serializer

class NotificationEndpoint(object):
    pass

def get_notifier(CONF, EXCHANGE='ai', PROJECT='ai', PUBLISHER_ID='ai'):
    oslo_messaging.set_transport_defaults(control_exchange=EXCHANGE)
    
    CONF(sys.argv[1:], project=PROJECT)
    
    transport = get_transport(CONF)
    
    notifier = Notifier(transport=transport, serializer=oslo_serializer.JsonPayloadSerializer(), publisher_id=PUBLISHER_ID)
    notifier.prepare(PUBLISHER_ID)
    
    return notifier

def get_transport(CONF):
    return get_notification_transport(CONF)

def set_listener(CONF=None, EXCHANGE='ai', topic='ai.notifications'):
    endpoints = [NotificationEndpoint()]
    transport = get_notification_transport(CONF)

    targets = [Target(exchange=EXCHANGE, topic=topic)]
    server = get_notification_listener(
        transport,
        targets,
        endpoints,
        executor='threading'
    )
    server.start()