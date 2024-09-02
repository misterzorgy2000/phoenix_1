from oslo_config import cfg
import sys
from cow.conf import ai, gnocchi_client, notification, schedule

from oslo_messaging._drivers import impl_rabbit

cfg.CONF(sys.argv[1:], project="cow")

cfg.set_defaults(
    impl_rabbit.rabbit_opts,
    rabbit_qos_prefetch_count=100,
)

CONF = cfg.CONF

ai.register_opts(CONF)
gnocchi_client.register_opts(CONF)
schedule.register_opts(CONF)