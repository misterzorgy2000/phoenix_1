from oslo_config import cfg

api = cfg.OptGroup(name='api',
                   title='Options for the Phoenix API service')

API_SERVICE_OPTS = [
    cfg.PortOpt('port',
                default=5678,
                help='The port for the Phoenix API server'),
    cfg.HostAddressOpt('host',
                       default='127.0.0.1',
                       help='The listen IP address for the phoenix API server'
                       ),
    cfg.IntOpt('workers',
               min=1,
               help='Number of workers for Phoenix API service.'),
]


def register_opts(conf):
    conf.register_group(api)
    conf.register_opts(API_SERVICE_OPTS, group=api)


def list_opts():
    return [(api, API_SERVICE_OPTS)]
