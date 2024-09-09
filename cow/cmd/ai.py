from colorama import init

from cow.conf import CONF
from cow.app.api import run as run_api
from cow.ai.service import launch_ai_service

init(autoreset=True)   

def main():    
    service = launch_ai_service(CONF)
    
    run_api()
    
    service.wait()
        
if __name__ == '__main__':
    main()
        