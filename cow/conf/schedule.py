from oslo_config import cfg

schedule = cfg.OptGroup(name='schedule', title='Schedule Options for AI')

SHEDULE_OPTS = [
    cfg.StrOpt('cron_update_metrics', default='*/30 0 0 * * *'),
    cfg.StrOpt('cron_fit_model', default='*/30 0 2 * * *'), 
]

def register_opts(conf):
    conf.register_opts(SHEDULE_OPTS, group=schedule)
    
def list_opts():
    return [(schedule, SHEDULE_OPTS)]