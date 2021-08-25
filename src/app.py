#!/usr/bin/env python3
import os
import subprocess
from exa import Interpreter


def main(file):
    program = Interpreter(file)
    return program.run()


if __name__ == '__main__':

    files = [file for file in os.listdir() if file.endswith('.exa')]
    files.sort()

    for index, file in enumerate(files):
        index += 1
        print(index, file)

    file = int(input('\n File No.> '))
    file = files[file-1]
    result = main(file)

    try:
        subprocess.run('clear')
    except Exception as e:
        # will log e later
        subprocess.run('cls')
    finally:
        pass
    
    print(file, '\n', result)
