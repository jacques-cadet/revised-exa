#!/usr/bin/env python3
import os
import subprocess
import platform
from exa import Interpreter, Log, EXAError


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
    try:
        result = main()
    except EXAError as e:
        logger = Log('EXA', 'logs', 'error')
        logger.log.error(e)
        quit()

    if platform.system() == "Linux" or platform.system() == "Darwin":
        subprocess.run("clear")
    elif platform.system() == "Windows":
        subprocess.run("cls")
    else:
        pass

    output_log = Log('OUTPUT')
    output_log.log.info(f'[{FILE}] - {result}')
