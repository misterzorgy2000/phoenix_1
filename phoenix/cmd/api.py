from oslo_log import log

from phoenix.app.api import run

LOG = log.getLogger(__name__)

def main():
    run()

if __name__ == '__main__':
    main()