from oslo_config import cfg

gnocchi_client = cfg.OptGroup(name='gnocchi_client',
                              title='Configuration Options for Gnocchi')

GNOCCHI_CLIENT_OPTS = [
    cfg.StrOpt('api_version',
               default='1',
               help='Version of Gnocchi API to use in gnocchiclient.'),
    cfg.StrOpt('endpoint_type',
               default='public',
               help='Type of endpoint to use in gnocchi client. '
                    'Supported values: internal, public, admin. '
                    'The default is public.'),
    cfg.StrOpt('region_name',
               help='Region in Identity service catalog to use for '
                    'communication with the OpenStack service.'),
    cfg.StrOpt('endpoint',
               default='http://10.1.101.30:8041')
]

def register_opts(conf):
    conf.register_group(gnocchi_client)
    conf.register_opts(GNOCCHI_CLIENT_OPTS, group=gnocchi_client)


def list_opts():
    return [(gnocchi_client, GNOCCHI_CLIENT_OPTS)]