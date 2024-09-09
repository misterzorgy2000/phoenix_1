from oslo_config import cfg

ai = cfg.OptGroup(name='ai', title='Configuration Options for AI')
schedule = cfg.OptGroup(name='schedule', title='Schedule Options for AI')

AI_OPTS = [
    cfg.ListOpt('target', default=['node_disk_read_bytes_total_y']),
    cfg.StrOpt('one_hot_drop', default='if_binary'),
    cfg.StrOpt('auto_class_weights', default='Balanced'),
    cfg.IntOpt('n_splits', default=5),
    cfg.ListOpt('scoring', default=['f1', 'roc_auc']),
    cfg.IntOpt('n_jobs', default=-1),
    cfg.ListOpt('metrics', default=['node_hwmon_temp_celsius', 'node_cpu_seconds_total', 'node_memory_MemTotal_bytes', 'node_memory_MemFree_bytes', 'node_disk_read_bytes_total_y'])   
]

def register_opts(conf):
    conf.register_group(ai)
    conf.register_group(schedule)
    conf.register_opts(AI_OPTS, group=ai)


def list_opts():
    return [(ai, AI_OPTS)]