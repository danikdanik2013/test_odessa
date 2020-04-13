from config import THREADS_COUNT, DB_NAME, RANGE


def check():
    if not THREADS_COUNT or not DB_NAME:
        print('Please, setup config file')
        exit()
    if not RANGE or RANGE not in range(1, 4):
        print('Please, setup the range in config file. Value must be in the range from 1 to 3')
