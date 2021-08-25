#!/usr/bin/env python3
import os
import logging
import subprocess
from exa import Interpreter


def main(file):
    program = Interpreter(file)
    return program.run()


def set_logging(filename=None):
    logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)8s %(name)12s %(levelname)-8s %(message)s')
    if filename:
        try:
            os.mkdir('logs')
        except FileExistsError:
            pass
    
    handlers = [
        logging.FileHandler(f'logs/{filename}.log'),
        logging.StreamHandler(),
    ] if filename else [logging.StreamHandler()]

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


if __name__ == '__main__':

    files = [file for file in os.listdir() if file.endswith('.exa')]
    files.sort()

    for index, file in enumerate(files):
        index += 1
        print(index, file)

    file = int(input('\n File No.> '))
    file = files[file-1]
    result = main(file)
    
    logger = set_logging()

    try:
        subprocess.run('clear')
    except Exception as e:
        logger.info(e)
        subprocess.run('cls')
    finally:
        pass
    logger.info(f"{file} - OK\n{result}")
    # print(result)
