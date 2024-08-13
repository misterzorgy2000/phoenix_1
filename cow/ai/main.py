from colorama import init, Fore
from datetime import datetime
import time

init(autoreset=True)

def run_ai():
    msg = "Hello from AI service"
    print(Fore.RED + msg)

    while True:
        print("Текущая временная метка: " + str(datetime.now()))
        time.sleep(5)

if __name__ == '__main__':
    run_ai()