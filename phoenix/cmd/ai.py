from colorama import init

from phoenix.conf import CONF
from phoenix.app.api import run as run_api
from phoenix.ai.service import launch_ai_service

init(autoreset=True)   

def main():    
    service = launch_ai_service(CONF)
    
    # run_api()
    
    service.wait()
        
if __name__ == '__main__':
    main()
        