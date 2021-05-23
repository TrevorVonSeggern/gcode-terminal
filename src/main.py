#!/usr/bin/env python3
import os
import sys
from program import Program
from container import Container

def main():
    container = Container().collection
    program = container.resolve(Program)
    program.Run()

if __name__ == '__main__':
    main()
    print('done')
