from oslo_config import cfg

notification = cfg.OptGroup(name='notification',
                               title='Defines the parameters of notifications')

NOTIFICATION_OPTS = {
    cfg.StrOpt('metering_topic',
               default='metering',
               help='The topic that ceilometer uses for metering '
               'notifications.',
               deprecated_for_removal=True),
    cfg.StrOpt('telemetry_driver',
               default='messagingv2',
               help='The driver that ceilometer uses for metering '
               'notifications.',
               deprecated_name='metering_driver'),
    cfg.IntOpt('workers',
               default=1,
               min=1,
               help='Number of workers for notification service, '
               'default value is 1.'),
}

EXCHANGES_OPTS = [
    cfg.MultiStrOpt('notification_control_exchanges',
                    default=['nova', 'keystone', 'ceilometer'],
                    help="Exchanges name to listen for notifications."),
]

def register_opts(conf):
    conf.register_group(notification)
    conf.register_opts(EXCHANGES_OPTS, group=notification)
    conf.register_opts(NOTIFICATION_OPTS, group=notification)


def list_opts():
    return [(notification, NOTIFICATION_OPTS)]
