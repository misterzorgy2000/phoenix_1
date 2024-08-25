from colorama import init

import pprint

from cow.ai.scripts.data import save_metrics
from cow.ai.scripts.fit import fit_model
import oslo_messaging
from oslo_messaging import get_notification_transport
from oslo_messaging import serializer as oslo_serializer
from oslo_config import cfg

init(autoreset=True)


NOTICE_MODEL_CREATED = {
    'created_at': '2012-05-08 20:23:41',
    'version': '1.0.2'
}

init(autoreset=True)

def run_ai():    
    # save_metrics()
    # fit_model()
    transport = get_notification_transport(cfg.CONF, 'rabbit://stackrabbit:secret@89.169.168.186:5672/')
    notifier = oslo_messaging.Notifier(transport=transport, serializer=oslo_serializer.JsonPayloadSerializer(), topics=['notifications'])
    notifier.prepare('compute.vagrant-precise')
    try: 
        notifier.info({}, 'compute.instance.create.end', NOTICE_MODEL_CREATED)
        print('ok')
    except Exception:
        print(Exception)
        
if __name__ == '__main__':
    run_ai()