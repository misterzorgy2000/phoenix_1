from colorama import init

import pprint

from cow.ai.scripts.data import save_metrics
from cow.ai.scripts.fit import fit_model

init(autoreset=True)

def run_ai():    
    save_metrics()
    fit_model()

if __name__ == '__main__':
    run_ai()