#!/usr/bin/env python3
import os
import subprocess
from exa import Interpreter, set_logging


def main():
    program = Interpreter(FILE)
    return program.run()


if __name__ == '__main__':

    files = [file for file in os.listdir() if file.endswith('.exa')]
    files.sort()

    for index, file in enumerate(files):
        # index += 1
        print(index+1, file)

    file = int(input('\n File No.> '))
    FILE = files[file-1]
    result = main()

    logger = set_logging('EXA', 'logs', 'exa')
    try:
        subprocess.run('clear')
    except Exception as e:
        logger.warning(e)
        subprocess.run('cls')
    finally:
        logger.info(f"{FILE} - OK")
        print(result)
