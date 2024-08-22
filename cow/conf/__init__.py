from oslo_config import cfg

from cow.conf import ai
from cow.conf import gnocchi_client
from cow.conf import notification

CONF = cfg.CONF

ai.register_opts(CONF)
gnocchi_client.register_opts(CONF)
notification.register_opts(CONF)