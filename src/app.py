#!/usr/bin/env python3
import os
from exa import Interpreter


def main(file):
    p = Interpreter(file)
    return p.run()

if __name__ == '__main__':
    files = [file for file in os.listdir() if file.endswith('.exa')]
    files.sort()
    for index, file in enumerate(files):
        index += 1
        print(index, file)
    file = int(input('File No.> '))
    file = files[file-1]
    result = main(file)
    print(result)
