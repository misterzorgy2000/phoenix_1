import os
import time
import joblib
from pathlib import Path
import asyncio
import semantic_version

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from oslo_service import service
from oslo_log import log as logging

from phoenix.conf import CONF

from phoenix.notification import get_notifier

from phoenix.ai import MODEL_DIR, MODEL_VERSION_FILE
from phoenix.ai.scripts.data import save_metrics
from phoenix.ai.scripts.fit import fit_model
from phoenix.ai.scripts.evaluate import evaluate_model 

PUBLISHER_ID = "ai"
PROJECT = "ai"
EXCHANGE = "ai"

LOG = logging.getLogger(__name__)

class PhoenixAI(service.ServiceBase):
    def __init__(self, CONF=None):
        self.CONF = CONF

        self.version_file_dir = Path(MODEL_DIR)
        self.version_file_path = Path(MODEL_VERSION_FILE)

        # TODO: update to pbr.version_string after moving to monorepo
        self.DEFAULT_VERSION = "0.0.1"

        if not os.path.exists(MODEL_VERSION_FILE):
            self.version_file_dir.mkdir(parents=True, exist_ok=True)

        self.__instance__ = self
        
        super().__init__()
    
    def start(self):
        print("Starting Phoenix AI")
        
        cron_update = self.CONF.schedule.cron_update_metrics.split(" ")
        cron_fit = self.CONF.schedule.cron_fit_model.split(" ")

        self._schedule_update(cron_update, cron_fit)

    def wait(self):
        pass

    def stop(self):
        print("Stopping Phoenix AI")

    def reset(self):
        print("Resetting Phoenix AI service")

    def _save_metrics(self):
        save_metrics()

    def fit_save(self):
        print("Starting model fit")
        
        fit_model([self._save_versioned_model, self._notify_updates])        
        evaluate_model(self.__get_model_fullpath(self.version_file_path.read_text()))

    def evaluate(self):
        return evaluate_model(self.__get_model_fullpath(self.version_file_path.read_text()))
    
    @staticmethod
    def get_model_version(version):
        model = None
        with open(f"{MODEL_DIR}/model-v{version}.pkl", 'rb') as fd:
            model = joblib.load(fd) 
            
        return model
        
    @staticmethod
    def get_latest_version():
        return Path(MODEL_VERSION_FILE).read_text()
        
    def _notify_updates(self, model=None):
        notifier = get_notifier(self.CONF, PUBLISHER_ID, PROJECT, EXCHANGE)
        version = self.get_latest_version()

        payload = {
            "created_at": time.time(),
            version: version,
            "path": self.__get_model_fullpath(version),
        }

        notifier.info({}, "ai.model.update", payload)

    def _save_versioned_model(self, model):
        os.makedirs(MODEL_DIR, exist_ok=True, mode=0o777)

        new_version = self.DEFAULT_VERSION

        if os.path.exists(MODEL_VERSION_FILE):
            curr_version = self.get_latest_version()
            new_version = str(semantic_version.Version(curr_version).next_patch())
        else:
            self.version_file_path.write_text(self.DEFAULT_VERSION)

        with open(self.__get_model_fullpath(new_version), "wb") as fd:
            joblib.dump(model, fd)

        self.version_file_path.write_text(new_version)

    def _schedule_update(self, cron_update, cron_fit):
        scheduler = AsyncIOScheduler()
        self.__add_cron_job(scheduler, self._save_metrics, cron_update)
        # self.__add_cron_job(scheduler, self.fit_save, cron_fit)

        scheduler.start()

        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            scheduler.shutdown()

    def __add_cron_job(self, scheduler, job, cron_args):
        second, minute, hour, day, month, year = cron_args
        
        scheduler.add_job(
            # job, "cron", year=year, month=month, day=day, hour=hour, minute=minute, second=second,
            job, "cron", second="*/30"
        )

    def __get_model_fullpath(self, version):
        return f"{MODEL_DIR}/{self.__get_model_filename(version)}"

    def __get_model_filename(self, version):
        return f"model-v{version}.pkl"

def get_service():
    return PhoenixAI.get_instance()

def launch_ai_service(CONF):
    launcher = service.Launcher(CONF)
    launcher.launch_service(PhoenixAI(CONF))

    # TODO: create singleton
    # TODO: create interservice communication
    PhoenixAI.instance = launcher.services.services[0]
    return launcher
