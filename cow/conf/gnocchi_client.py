from oslo_config import cfg

gnocchi_client = cfg.OptGroup(name='gnocchi_client',
                              title='Configuration Options for Gnocchi')

GNOCCHI_CLIENT_OPTS = [
    cfg.StrOpt('api_version',
               default='1'),
    cfg.StrOpt('endpoint_type', default='public'),
    cfg.StrOpt('region_name', default='default'),
    cfg.StrOpt('timespan', default='1440'),
    cfg.StrOpt('endpoint', default='localhost:8041')
]

def register_opts(conf):
    conf.register_group(gnocchi_client)
    conf.register_opts(GNOCCHI_CLIENT_OPTS, group=gnocchi_client)


def list_opts():
    return [(gnocchi_client, GNOCCHI_CLIENT_OPTS)]