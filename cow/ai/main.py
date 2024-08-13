from colorama import init, Fore
from datetime import time, datetime

init(autoreset=True)

def run_ai():
    msg = "Hello from AI service"
    print(Fore.RED + msg)

    while True:
        with open("timestamp.txt", "a") as f:
            f.write("Текущая временная метка: " + str(datetime.now()))
            f.close()
        time.sleep(10)

if __name__ == '__main__':
    run_ai()