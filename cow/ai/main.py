from colorama import init

from cow.conf import CONF
from cow.ai.service import launch_ai_service

init(autoreset=True)   

def run_ai():    
    service = launch_ai_service(CONF)
    service.wait()
    
if __name__ == '__main__':
    run_ai()
        