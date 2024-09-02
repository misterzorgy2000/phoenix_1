from oslo_config import cfg

oslo_messaging_notifications = cfg.OptGroup(name='oslo_messaging_notifications',
                               title='Oslo messaging')

OSLO_NOTIFICATIONS_OPTS = [
    cfg.StrOpt('driver', default='messagingv2'),
    cfg.ListOpt('topics', default=['ai.notifications']),
]

def register_opts(conf):
    conf.register_group(oslo_messaging_notifications)
    conf.register_opts(OSLO_NOTIFICATIONS_OPTS, group=oslo_messaging_notifications)


def list_opts():
    return [(oslo_messaging_notifications, OSLO_NOTIFICATIONS_OPTS)]
