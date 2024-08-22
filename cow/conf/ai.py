from oslo_config import cfg

gnocchi_client = cfg.OptGroup(name='gnocchi_client',
                              title='Configuration Options for Gnocchi')

ai = cfg.OptGroup(name='ai', title='Configuration Options for AI')

AI_OPTS = [
    cfg.ListOpt('target', default=['node_disk_read_bytes_total']),
    cfg.StrOpt('one_hot_drop', default='if_binary'),
    cfg.StrOpt('auto_class_weights', default='Balanced'),
    cfg.IntOpt('n_splits', default=5),
    cfg.ListOpt('validation_metrics', default=['f1', 'roc_auc']),
    cfg.IntOpt('n_jobs', default=-1),
    cfg.ListOpt('metrics', default=['node_hwmon_temp_celsius', 'node_cpu_seconds_total', 'node_memory_MemTotal_bytes', 'node_memory_MemFree_bytes', 'node_disk_read_bytes_total'])   
]

def register_opts(conf):
    conf.register_group(ai)
    conf.register_opts(AI_OPTS, group=ai)


def list_opts():
    return [(ai, AI_OPTS)]