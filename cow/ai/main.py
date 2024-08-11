from colorama import init, Fore

init(autoreset=True)

def run_ai():
    msg = "Hello from AI service"
    print(Fore.RED + msg)

if __name__ == '__main__':
    run_ai()